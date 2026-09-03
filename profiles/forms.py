from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [

            # ==== Identity ====
            "profile_picture",
            "display_name",
            "display_name_2",
            "display_name_3",
            "local_language_name",
            "date_of_birth",
            "nationality",
            "languages_spoken",

            # ==== Location ====
            "country",
            "city",

            # ==== Contact ====
            "email",
            "phone",
            "website",

            # ==== Professional ====
            "job_title",
            "company",
            "industry",
            "skills",
            "years_experience",

            # ==== About ====
            "bio",
            "interests",
            "hobbies",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs["class"] = "form-control"

        self.fields["bio"].widget.attrs["rows"] = 5
        self.fields["skills"].widget.attrs["rows"] = 3
        self.fields["interests"].widget.attrs["rows"] = 3
        self.fields["hobbies"].widget.attrs["rows"] = 3
        self.fields["date_of_birth"].widget = forms.DateInput(
            attrs={"type": "date",}, format="%Y-%m-%d",
        )
        self.fields["date_of_birth"].input_formats = ["%Y-%m-%d",]