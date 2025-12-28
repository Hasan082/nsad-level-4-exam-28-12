from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'display_name',
            'email',
            'user_type',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'password'  
        self.fields['password2'].label = 'Confirm password'  
        self.fields['username'].help_text = ''  
        self.fields['password1'].help_text = ''  
        self.fields['password2'].help_text = ''  
        self.fields['email'].required = True