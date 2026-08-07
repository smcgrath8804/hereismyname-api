from django import forms

from .models import ProfileLink


class ProfileLinkForm(forms.ModelForm):

    class Meta:

        model = ProfileLink

        fields = [
            "platform",
            "platform_name",
            "label",
            "url",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs["class"] = "form-control"