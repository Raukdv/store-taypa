from django import forms
import django_filters as filters
from django_filters import fields, widgets


class DateTimeInput(forms.DateTimeInput):
    class Media:
        css = {
            'all': (
                (
                    'tempusdominus-bootstrap-4/build/css'
                    '/tempusdominus-bootstrap-4.min.css'
                ),
            )
        }
        js = (
            'moment/min/moment-with-locales.js',
            (
                'tempusdominus-bootstrap-4/build/js'
                '/tempusdominus-bootstrap-4.js'
            ),
            'panel/js/datetimepicker.js'
        )


class DateRangeWidget(widgets.SuffixedMultiWidget):
    template_name = 'panel/widgets/daterangewidget.html'
    suffixes = ['after', 'before']

    def __init__(self, attrs=None):
        widgets = (DateTimeInput, DateTimeInput)
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]


class DateTimeRangeField(fields.DateTimeRangeField):
    widget = DateRangeWidget


class DateTimeFromToRangeFilter(filters.RangeFilter):
    field_class = DateTimeRangeField
