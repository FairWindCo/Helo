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

class FlatPickerInput(DateTimeInput):
    template_name = 'mytemplates/flatpickr_datetime.html'

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
        return context



class FlatPickerRangeWidget(DateRangeWidget):
    #template_name = 'django_filters/widgets/multiwidget.html'
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

class FlatPickerRangeInput(RangeField):
    widget = FlatPickerRangeWidget