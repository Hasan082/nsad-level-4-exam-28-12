from django import forms
from .models import RecruiterProfile, JobSeekerProfile, JobPosting, JobApplication


class RecruiterEditForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = [
            "company_name",
            "company_name",
            "company_website",
            "company_phone",
            "location",
        ]


class JobSeekerEditForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ["skill", "title", "phone", "skill", "years_of_experience", "bio"]


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            "title",
            "description",
            "number_opening",
            "category",
            "skill_required",
        ]


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            "cover_letter",
            "resume",
        ]

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        if not resume:
            raise forms.ValidationError("resume is required for the job")
        return resume
