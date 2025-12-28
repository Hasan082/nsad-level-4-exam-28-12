from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    class UserType(models.TextChoices):
        RECRUITER = 'recruiters', 'Recruiters'
        JOBSEEKER = 'jobseekers', 'Jobseekers'

    display_name = models.CharField(max_length=120)
    email = models.EmailField()
    user_type = models.CharField(
        choices=UserType.choices, max_length=15, default=UserType.JOBSEEKER
    )

    def __str__(self):
        return f'{self.display_name}'

    @property
    def is_recruiter(self):
        return self.user_type == self.UserType.RECRUITER

    @property
    def is_jobseeker(self):
        return self.user_type == self.UserType.JOBSEEKER