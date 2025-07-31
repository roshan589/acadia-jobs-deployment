from django import forms
from .models import CreateJob, ApplyJob
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CreateParentForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'parent_expiry_date']


class JobPost(forms.ModelForm):
    class Meta:
        model = CreateJob
        fields = ['title', 'position', 'companyName','jobType', 'location', 'applicationDeadline', 'description']



class JobApplyForm(forms.ModelForm):
    class Meta:
        model = ApplyJob
        fields = ['first_name', 'last_name', 'email','address','city','state', 'phone_no', 'availability_start_date', 'availability_end_date', 'resume']
        resume = forms.FileField(required=True)


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = ApplyJob
        fields = ['job_status']




class JobFilterForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label='Search by Job Title')
    posted_on = forms.DateField(required=False, widget=forms.SelectDateWidget, label='Date Posted')
