from django.contrib import admin
from .models import RecruiterProfile, JobSeekerProfile, JobPosting, JobApplication


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "company_website", "company_phone", "location")


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "phone", "skill", "years_of_experience", "bio")


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "number_opening",
        "category",
        "skill_required",
        "is_active",
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant", "job", "cover_letter", "resume")
