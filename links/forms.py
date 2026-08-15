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


    def clean(self):

        cleaned_data = super().clean()

        platform = cleaned_data.get("platform")
        platform_name = cleaned_data.get("platform_name")

        if platform == "other" and not platform_name:

            self.add_error(
                "platform_name",
                "Please enter a platform name.",
            )

        elif platform != "other":

            cleaned_data["platform_name"] = ""

        return cleaned_data
