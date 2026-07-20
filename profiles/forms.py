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