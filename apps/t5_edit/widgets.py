from django.forms import widgets


class Datepicker(widgets.DateInput):
    class Media:
        css = {'all': ('css/jquery-ui.css',)}
        js = (
            'js/jquery-1.10.2.js',
            'js/jquery-ui.js',
        )

    def __init__(self, attrs={'class': 'datepicker'}, *args, **kwargs):
        super(Datepicker, self).__init__(*args, attrs=attrs, **kwargs)
