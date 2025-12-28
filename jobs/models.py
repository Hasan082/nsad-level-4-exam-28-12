from django.db import models
from django.conf import settings

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class RecruiterProfile(TimeStampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recruiter_profile",
    )
    company_name = models.CharField(max_length=200, blank=True)
    company_website = models.URLField(blank=True, null=True)
    company_phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.TextField()

    def __str__(self):
        return self.user.display_name

class JobSeekerProfile(TimeStampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobseeker_profile",
    )
    title = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    skill = models.CharField(max_length=150, blank=True)
    years_of_experience = models.SmallIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.display_name


class JobPosting(TimeStampModel):
    recruiter = models.ForeignKey(
        RecruiterProfile, on_delete=models.CASCADE, related_name="job_postings"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    number_opening = models.PositiveSmallIntegerField(default=1)
    category = models.CharField(max_length=200, null=True, blank=True)
    skill_required = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:  # type: ignore
        ordering = ["-created_at"]
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"

    def __str__(self):
        return self.title
    

class JobApplication(models.Model):
    class StatusChoice(models.TextChoices):
        APPLIED = "applied", "Applied"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"

    applicant = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name="applications"
    )
    applied_at = models.DateField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to="applications/resumes/")
    status = models.CharField(
        max_length=30, choices=StatusChoice.choices, default=StatusChoice.APPLIED
    )

    class Meta:
        ordering = ["-applied_at"]
        unique_together = ("applicant", "job")
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return f"{self.applicant.user.display_name} -> {self.job.title}"