from django import forms


class BootStrapForm(forms.Form):

    def __init__(self, exclude_names=(), *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name not in exclude_names:
                field.widget.attrs['class'] = 'form-control'
