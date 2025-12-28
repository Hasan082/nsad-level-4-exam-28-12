from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import RecruiterProfile, JobSeekerProfile, JobPosting, JobApplication
from .forms import RecruiterEditForm, JobSeekerEditForm, JobPostingForm, JobApplicationForm
from functools import wraps

def get_user_profile(user):
    if user.is_recruiter:
        return get_object_or_404(RecruiterProfile, user=user)
    return get_object_or_404(JobSeekerProfile, user=user)

def get_form_class(user):
    if user.is_recruiter:
        return RecruiterEditForm
    return JobSeekerEditForm

def recruiter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_recruiter:
            messages.warning(request, "Only recruiter access this page")
            return redirect("recruiter_job")
        return view_func(request, *args, **kwargs)
    return wrapper

def jobseeker_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_jobseeker:
            messages.warning(request, "Only recruiter access this page")
            return redirect("my_applications")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def profile_view(request):
    profile = get_user_profile(request.user)
    return render(
        request,
        "view-profile.html",
        {
            "profile": profile,
            "is_recruiter": request.user.is_recruiter,
            "is_jobseeker": request.user.is_jobseeker,
        },
    )
    
    
@login_required
def edit_profile_view(request):
    profile = get_user_profile(request.user)
    FormClass = get_form_class(request.user)
    if request.method == "POST":
        form = FormClass(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("edit_profile")
        else:
            messages.error(request, "Please correct the error!")
    else:
        form = FormClass(instance=profile)
    return render(request, "profileform.html", {"form": form})


@login_required
@recruiter_required
def create_job_view(request):
    if request.method == "POST":
        form = JobPostingForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiter_profile
            job.save()
            messages.success(request, "Job Successfully created!")
            return redirect("recruiter_job")
        else:
            messages.error(request, "Please correct the error!")
    else:
        form = JobPostingForm()
    context = {"form": form, "create_job": True}
    return render(request, "jobform.html", context)


@login_required
@recruiter_required
def recruiter_only_job(request):
    recruietr_job = (
        JobPosting.objects.filter(recruiter=request.user.recruiter_profile)
        .annotate(applicant_count=Count("applications"))
        .order_by("-id")
    )

    context = {
        "my_jobs": recruietr_job,
    }
    return render(request, "recruiterjob.html", context)


@login_required
@recruiter_required
def edit_job_view(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, recruiter=request.user.recruiter_profile)
    if request.method == "POST":
        form = JobPostingForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiter_profile
            job.save()
            messages.success(request, "Job Updated successfully!")
            return redirect("recruiter_job")
        else:
            messages.error(request, "Please correct the error!")
    else:
        form = JobPostingForm(instance=job)
    context = {"form": form}
    return render(request, "jobform.html", context)


@login_required
@recruiter_required
def delete_job_view(request, job_id):
    job = get_object_or_404(
        JobPosting, id=job_id, recruiter=request.user.recruiter_profile
    )
    if request.method == "POST":
        job.delete()
        messages.error(request, "Job deleted successfully.")
        return redirect("recruiter_job")
    else:
        messages.error(request, "Please correct the error!")
    messages.warning(request, "Invalid request method.")
    return redirect("recruiter_job")


def job_list_view(request):
    user = request.user
    job_lists = JobPosting.objects.filter(is_active=True).order_by("-id")
    already_applied_ids = []
    if user.is_authenticated and user.is_jobseeker:
        seeker = get_user_profile(user)
        already_applied_ids = JobApplication.objects.filter(applicant=seeker).values_list("job_id", flat=True)
    context = {"jobs": job_lists, "already_applied_ids": already_applied_ids}
    return render(request, "joblist.html", context)



@login_required
@recruiter_required
def job_applicants_view(request):
    filter_type = request.GET.get("filter", "all")  # matched / all
    status_filter = request.GET.get(
        "status", "all"
    )  # applied / shortlisted / rejected / all

    applicants = JobApplication.objects.filter(
        job__recruiter=request.user.recruiter_profile
    ).select_related("applicant", "applicant__user", "job")

    if status_filter != "all":
        applicants = applicants.filter(status=status_filter)

    result = []

    for app in applicants:
        job_skills = {s.strip().lower() for s in app.job.skill_required.split(",") if s.strip()}  # type: ignore
        seeker_skills = {
            s.strip().lower() for s in app.applicant.skill.split(",") if s.strip()
        }

        common = job_skills & seeker_skills
        app.match_percent = int(len(common) / len(job_skills) * 100) if job_skills else 0  # type: ignore

        if filter_type == "matched" and app.match_percent == 0:  # type: ignore
            continue

        result.append(app)

    context = {
        "applicants": result,
        "filter_type": filter_type,
        "status_filter": status_filter,
    }
    return render(request, "applicant-list.html", context)


@login_required
@jobseeker_required
def job_detail_view(request, job_id):

    job = get_object_or_404(JobPosting, id=job_id)
    seeker = get_user_profile(request.user)

    application = None
    already_applied = False

    if not job.is_active:  # type: ignore
        messages.error(request, "Job is no longer active")
        return redirect("job_lists")

    try:
        application = JobApplication.objects.get(applicant=seeker, job=job)
        already_applied = True
    except JobApplication.DoesNotExist:
        application = None
        already_applied = False

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():

            if already_applied:
                messages.warning(request, "You already applied this job")
                return redirect("job_lists")

            job_applicant = form.save(commit=False)
            job_applicant.applicant = request.user.jobseeker_profile
            job_applicant.job = job
            job_applicant.save()
            return redirect("my_applications")
        else:
            messages.error(request, "Please correct the error!")
    else:
        form = JobApplicationForm()

    context = {
        "form": form,
        "job": job,
        "already_applied": already_applied,
        "application": application,
    }

    return render(request, "job-apply.html", context)


@login_required
@jobseeker_required
def my_applicantion(request):
    applicant = get_user_profile(request.user)
    own_jobs = JobApplication.objects.filter(applicant=applicant)
    context = {"own_jobs": own_jobs}
    return render(request, "my-application.html", context)


@login_required
@jobseeker_required
def seeker_skill_mathing_job(request):
    user = request.user
    context = {}

    if user.is_jobseeker:
        seeker = user.jobseeker_profile
        seeker_skills = [
            s.strip().lower() for s in seeker.skill.split(",") if s.strip()
        ]

        skill_query = Q()
        for skill in seeker_skills:
            skill_query |= Q(skill_required__icontains=skill)

        seeker_applied_job = JobApplication.objects.filter(applicant=seeker)
        jobs_ids = seeker_applied_job.values_list("job_id", flat=True)

        matching_jobs = JobPosting.objects.filter(skill_query, is_active=True).exclude(
            id__in=jobs_ids
        )

        context = {"jobs": matching_jobs, "matching": True}

    return render(request, "joblist.html", context)

