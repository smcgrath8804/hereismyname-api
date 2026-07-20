from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "display_name",
            "local_language_name",
            "email",
            "phone",
            "job_title",
            "company",
            "bio",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs["class"] = "form-control"

        self.fields["bio"].widget.attrs["rows"] = 5