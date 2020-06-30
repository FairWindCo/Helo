# Create your views here.
# -*- coding: utf-8 -*-
import logging

from django.db.models import Q
from django.utils.html import escape, format_html

from .mixins import JSONJTableResponseView

logger = logging.getLogger(__name__)


class JTableMixin(object):
    """ JSON data for datatables
    """
    model = None
    columns = []
    _columns = []  # internal cache for columns definition
    order_columns = []
    max_display_length = 100  # max limit of records returned, do not allow to kill our server by huge sets of data
    none_string = ''
    escape_values = True  # if set to true then values returned by render_column will be escaped
    paging = True
    columns_data = []
    is_data_list = False

    FILTER_ISTARTSWITH = 'istartswith'
    FILTER_ICONTAINS = 'icontains'

    @property
    def _querydict(self):
        if self.request.method == 'POST':
            return self.request.POST
        else:
            return self.request.GET

    def get_filter_method(self):
        """ Returns preferred filter method """
        return self.FILTER_ISTARTSWITH

    def initialize(self, *args, **kwargs):
        pass

    def get_order_columns(self):
        """ Return list of columns used for ordering.
            By default returns self.order_columns but if these are not defined it tries to get columns
            from the request using the columns[i][name] attribute. This requires proper client side definition of
            columns, eg:
                columns: [
                    {
                        name: 'username',
                        data: 'username',
                        orderable: true,
                    },
                    {
                        name: 'email',
                        data: 'email',
                        orderable: false
                    }
                ]
        """
        if self.order_columns:
            return self.order_columns

        # try to build list of order_columns using request data
        order_columns = []
        for column_def in self.columns_data:
            if column_def['name'] or not self.is_data_list:
                # if self.is_data_list is False then we have a column name in the 'data' attribute, otherwise
                # 'data' attribute is an integer with column index
                if column_def['orderable']:
                    if self.is_data_list:
                        order_columns.append(column_def['name'])
                    else:
                        order_columns.append(column_def.get('data'))
                else:
                    order_columns.append('')
            else:
                # fallback to columns
                order_columns = self._columns
                break

        self.order_columns = order_columns
        return order_columns

    def get_columns(self):
        """ Returns the list of columns to be returned in the result set.
            By default returns self.columns but if these are not defined it tries to get columns
            from model.
        """
        if self.columns:
            return self.columns
        elif self.is_data_list:
            raise NotImplementedError("Need to provide a model or define columns!")
        columns = [e.name for e in self.model._meta.get_fields()]
        self.columns = columns

        return columns

    @staticmethod
    def _column_value(obj, key):
        """ Returns the value from a queryset item
        """
        if isinstance(obj, dict):
            return obj.get(key, None)

        return getattr(obj, key, None)

    def _render_column(self, row, column):
        """ Renders a column on a row. column can be given in a module notation eg. document.invoice.type
        """
        # try to find rightmost object
        obj = row
        parts = column.split('.')
        for part in parts[:-1]:
            if obj is None:
                break
            obj = getattr(obj, part)

        # try using get_OBJECT_display for choice fields
        if hasattr(obj, 'get_%s_display' % parts[-1]):
            value = getattr(obj, 'get_%s_display' % parts[-1])()
        else:
            value = self._column_value(obj, parts[-1])

        if hasattr(value, 'target_field'):
            value = [str(rec) for rec in value.all()]
            if value is None:
                value = self.none_string
        else:
            if value is None:
                value = self.none_string

            if self.escape_values:
                value = escape(value)

        return {column: value}

    def render_column(self, row, column):
        """ Renders a column on a row. column can be given in a module notation eg. document.invoice.type
        """
        value = self._render_column(row, column)
        if value and hasattr(row, 'get_absolute_url'):
            return format_html('<a href="{}">{}</a>', row.get_absolute_url(), value)
        return value

    def ordering(self, qs):
        """ Get parameters from the request and prepare order by clause
        """

        # Number of columns that are used in sorting
        sorting_cols = 0
        sorting = self._querydict.get('jtSorting', '')

        if not sorting:
            return qs

        order = []
        sort_key, direction = sorting.split(' ')
        if direction == 'DESC':
            sort_dir = '-'
        else:
            sort_dir = ''
        order.append('{0}{1}'.format(sort_dir, sort_key.replace('.', '__')))

        if order:
            return qs.order_by(*order)
        return qs

    def paging(self, qs):
        """ Paging
        """
        # totally disable paging for view
        if not self.paging:
            return qs

        limit = min(int(self._querydict.get('jtStartIndex', 10)), self.max_display_length)
        start = int(self._querydict.get('jtPageSize', 0))

        # if pagination is disabled ("paging": false)
        if limit == -1:
            return qs

        offset = start + limit

        return qs[start:offset]

    def get_initial_queryset(self):
        if not self.model:
            raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")
        return self.model.objects.all()

    def filter_queryset(self, qs):
        """ If search['value'] is provided then filter all searchable columns using filter_method (istartswith
            by default).

            Automatic filtering only works for Datatables 1.10+. For older versions override this method
        """
        columns = self._columns
        q = Q()
        filter_method = self.get_filter_method()
        # get global search value
        for column in columns:
            search = self._querydict.get('search[{}]'.format(column), None)
            if search:
                column = column.replace('.', '__')
                qs = qs.filter(**{
                    '{0}__{1}'.format(column, filter_method): search})

        qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        data = []
        for item in qs:
            data.append([self.render_column(item, column) for column in self._columns])
        return data

    def handle_exception(self, e):
        logger.exception(str(e))
        raise e

    def get_context_data(self, *args, **kwargs):
        try:
            self.initialize(*args, **kwargs)

            # determine the response type based on the 'data' field passed from JavaScript
            # https://datatables.net/reference/option/columns.data
            # col['data'] can be an integer (return list) or string (return dictionary)
            # we only check for the first column definition here as there is no way to return list and dictionary
            # at once
            # prepare list of columns to be returned
            self._columns = self.get_columns()

            # prepare initial queryset
            qs = self.get_initial_queryset()

            # store the total number of records (before filtering)
            total_records = qs.count()

            # apply filters
            qs = self.filter_queryset(qs)

            # number of records after filtering
            total_display_records = qs.count()

            # apply ordering
            qs = self.ordering(qs)

            # apply pagintion
            qs = self.paging(qs)

            # prepare output data

            data = self.prepare_results(qs)

            ret = {'TotalRecordCount': total_records,
                   'RecordsFiltered': total_display_records,
                   'Records': data
                   }
            return ret
        except Exception as e:
            return self.handle_exception(e)


class BaseDatatableView(JTableMixin, JSONJTableResponseView):
    pass
