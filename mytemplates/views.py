from django.db import models
from django.forms import model_to_dict, fields_for_model
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import get_template
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView


def show_test(request):
    return render(request, 'mytemplates/mytemplate.html')


def show_admin(request):
    return render(request, 'mytemplates/mybacktemplate.html')


class DetailAjaxViewMixin(SingleTableMixin):
    ajax_refral = 'AJAX_TABLE'
    ajax_detail_refral = 'AJAX_TABLE_DETAIL'
    my_absolute_url = ''
    my_table_template = 'mytemplates/filtered/bootstrap4.html'
    my_detail_template = 'mytemplates/filtered/ajax_detail_wrapper.html'
    my_detail_data_template = 'mytemplates/filtered/ajax_detail_content.html'
    my_template = 'mytemplates/filtered/ajax_wrapper.html'
    my_data_template = 'mytemplates/filtered/ajax_content.html'
    use_special_url_for_detail = None
    default_template = True
    use_ajax = True
    csrf_token = None
    create_filter = True
    table_pagination = {'per_page': 5}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'table' in context:
            setattr(context['table'], 'use_special_url_for_detail', self.use_special_url_for_detail)
        context['ajax_divname'] = self.ajax_refral
        context['ajax_tableurl'] = self.my_absolute_url
        context['ajax_detail_refral'] = self.ajax_detail_refral
        context['need_ajax'] = self.use_ajax
        context['csrf_token'] = self.csrf_token
        context['use_special_url_for_detail'] = self.use_special_url_for_detail
        if self.default_template:
            context['table_template'] = self.my_table_template
        return context

    def render_to_response(self, context, template=None, **response_kwargs):
        if template is None:
            template = self.template_name,

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def form_detail_record_info(self, record):
        data = model_to_dict(record)
        if isinstance(record, models.Model):
            data['fields_meta_info'] = fields_for_model(record)
            data['fields_meta_record'] = record
        return data

    def get_record_datas(self, record_id):
        data = self.get_table_data()
        records = data.filter(pk=record_id).all()
        data = [self.form_detail_record_info(record) for record in records]
        return data

    def get_record_data(self, record_id):
        data = self.get_table_data()
        record = get_object_or_404(data, pk=record_id)
        # data = self.form_detail_record_info(record)
        return record

    def render_detail_record(self, record_id, is_ajax, request, *args, **kwargs):
        data = self.get_record_data(record_id)

        if is_ajax:
            template = self.my_detail_data_template
            context = {'detail_content': data, 'ajax_divname': self.ajax_refral,
                       'ajax_tableurl': self.my_absolute_url, 'ajax_detail_refral': self.ajax_detail_refral}
            response = self.render_to_response(
                context=context,
                template=template
            )
        else:
            template = self.my_detail_template
            template = get_template(template)
            context = {'detail_content': data, 'ajax_divname': self.ajax_refral,
                       'ajax_tableurl': self.my_absolute_url, 'ajax_detail_refral': self.ajax_detail_refral}
            new_context = template.render(context=context, request=request)

            context = {'view_content': new_context, 'ajax_divname': self.ajax_refral,
                       'ajax_tableurl': self.my_absolute_url, 'ajax_detail_refral': self.ajax_detail_refral}

            response = self.render_to_response(context, self.template_name)
        return response

    def render_table_records(self, is_ajax, request, *args, **kwargs):
        data = self.get_table_data()
        if is_ajax:
            context = self.get_context_data(object_list=data)
            response = self.render_to_response(context, self.my_data_template)
        else:
            context = self.get_context_data(object_list=data)
            template = get_template(self.my_template)
            new_context = template.render(context=context, request=request)
            response = self.render_to_response({'view_content': new_context})
        return response

    def get(self, request, *args, **kwargs):
        self.csrf_token = get_token(request)
        self.my_absolute_url = request.build_absolute_uri
        is_ajax = request.GET.get('is_ajax', False)
        if 'record_id' in request.GET:
            record_id = request.GET.get('record_id')
            response = self.render_detail_record(record_id, is_ajax, request, *args, **kwargs)
        else:
            response = self.render_table_records(is_ajax, request, *args, **kwargs)
        return response


class DetailAjaxView(DetailAjaxViewMixin, SingleTableView):
    pass


class FilterListDetailAjaxView(DetailAjaxViewMixin, FilterView):

    def render_table_records(self, is_ajax, request, *args, **kwargs):
        if not self.create_filter:
            return DetailAjaxViewMixin.render_table_records(self, is_ajax, request, *args, **kwargs)
        if is_ajax:
            self.template_name = self.my_data_template
            response = FilterView.get(self, request, *args, **kwargs)
        else:
            filterset_class = self.get_filterset_class()
            self.filterset = self.get_filterset(filterset_class)

            if not self.filterset.is_bound or self.filterset.is_valid() or not self.get_strict():
                self.object_list = self.filterset.qs
            else:
                self.object_list = self.filterset.queryset.none()
            context = self.get_context_data(filter=self.filterset,
                                            object_list=self.object_list)
            template = get_template(self.my_template)
            new_context = template.render(context=context, request=request)
            response = self.render_to_response({'view_content': new_context})
        return response

    def render_to_response(self, context, template=None, **response_kwargs):
        if not self.create_filter:
            return DetailAjaxViewMixin.render_to_response(self, context, template, **response_kwargs)
        if template is None:
            return FilterView.render_to_response(self, context, **response_kwargs)
        else:
            response_kwargs.setdefault('content_type', self.content_type)
            return self.response_class(
                request=self.request,
                template=template,
                context=context,
                using=self.template_engine,
                **response_kwargs
            )
