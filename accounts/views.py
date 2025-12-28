from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserForm
from jobs.models import RecruiterProfile, JobSeekerProfile

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object #type: ignore
        if user.is_recruiter:
            RecruiterProfile.objects.get_or_create(user=user)
        else:
            JobSeekerProfile.objects.get_or_create(user=user)
        return response