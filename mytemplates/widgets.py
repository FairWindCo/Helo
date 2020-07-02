from django.forms import DateTimeInput
from django_filters.fields import RangeField
from django_filters.widgets import DateRangeWidget


class BootstrapDateTimePickerInput(DateTimeInput):
    template_name = 'mytemplates/bootstrap_datetimepicker.html'

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        return context

    class Media:
        css = {
            'all': ('assets/js/plugins/bootstrap-datepicker/css/bootstrap-datepicker.css',)
        }
        js = ('assets/js/plugins/bootstrap-datepicker/js/bootstrap-datepicker.js',)


class FlatPickerInput(DateTimeInput):
    template_name = 'mytemplates/flatpickr_datetime.html'

    def __init__(self, attrs=None, show_time=True, show_24=True):
        super().__init__(attrs)
        self.show_time = show_time
        self.show_24 = show_24


    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimepicker-input'
        if 'format' not in attrs:
            attrs['format'] = 'd-m-Y H:i:S'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        context['widget']['format'] = attrs['format']
        context['widget']['show_24'] = self.show_24
        context['widget']['show_time'] = self.show_time
        return context

    class Media:
        css = {
            'all': ('assets/js/plugins/flatpickr/flatpickr.css',)
        }
        js = ('assets/js/plugins/flatpickr/flatpickr.js',)


class FlatPickerRangeWidget(DateRangeWidget):
    # template_name = 'django_filters/widgets/multiwidget.html'
    template_name = 'mytemplates/flatpickr_datetime_range.html'

    def __init__(self, attrs=None, format='d-m-Y H:i:S'):
        self.format_datetime = format
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if attrs is None:
            attrs = dict()
        if 'format' not in attrs:
            attrs['format'] = self.format_datetime
        context['picker_datetime'] = {}
        context['picker_datetime']['format'] = attrs['format']
        return context

    class Media:
        css = {
            'all': ('assets/js/plugins/flatpickr/flatpickr.css',)
        }
        js = ('assets/js/plugins/flatpickr/flatpickr.js',)

class FlatPickerRangeInput(RangeField):
    widget = FlatPickerRangeWidget
