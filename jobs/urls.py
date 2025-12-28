from django.urls import path
from .views import (
    profile_view,
    edit_profile_view,
    job_list_view,
    create_job_view,
    edit_job_view,
    delete_job_view,
    recruiter_only_job,
    job_applicants_view,
    job_detail_view,
    my_applicantion,
    seeker_skill_mathing_job
)

urlpatterns = [
    path('profile/', profile_view, name='view_profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('jobs/create/', create_job_view, name='create_job'),
    path('jobs/<int:job_id>/edit/', edit_job_view, name='edit_job'),
    path('jobs/<int:job_id>/delete/', delete_job_view, name='delete_job'),
    path('recruiter/jobs/', recruiter_only_job, name='recruiter_job'),
    path("", job_list_view, name="job_lists"),
    path('recruiter/jobs/', recruiter_only_job, name='recruiter_job'),
    path('recruiter/applicants/', job_applicants_view, name='my_applicants'),
    path('jobs/<int:job_id>/', job_detail_view, name='job_detail'),
    path('my-applications/', my_applicantion, name='my_applications'),
    
    # Job Apply
    path("apply/job/<int:job_id>", job_detail_view, name="apply_job"),
    path("my-application/", my_applicantion, name="seeker_job"),
    path("seeker-matching-jobs/", seeker_skill_mathing_job, name="seeker_matching_job"),
]






































