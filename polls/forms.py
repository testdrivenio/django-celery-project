from django import forms


class YourForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # add class to make the fields work with Bootstrap
        # In real projects, you can check https://django-crispy-forms.readthedocs.io/en/latest/
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

