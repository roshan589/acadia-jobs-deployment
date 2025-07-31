from django.urls import path, include
from . import views

urlpatterns = [

    path('edit/', views.edit_profile, name='edit_profile'),
    path("dashboard/", views.test, name='test'),
    path('faculty/create-parent', views.create_parent_account, name='parent_account'),
    path("faculty/create-job", views.post_job, name="post_job"),
    path('faculty/jobs/', views.facultyJobList, name="faculty_job_list"),
    path('faculty/job/<int:job_id>/applications', views.jobApplicationDBFaculty, name='job_applications'),
    path('student/apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('detail/<int:job_id>/', views.jobDetail, name='job_detail'),
    path('student/job-status/', views.jobApplicationStatus, name='job_status'),
    path('faculty/edit-status/<int:application_id>/', views.updateApplicationStatus, name='edit_status'),
    path('faculty/manage-jobs/', views.deleteJobList, name='manage_jobs'),
    path('faculty/delete-job/<int:job_id>/', views.deleteJobPost, name='delete_job'),
    path('job-list', views.jobList, name='job_list'),
    path('jobsearch/', views.job_search, name='job-search'),
    path('jobs/edit/<int:job_id>/', views.editJob, name='edit_job')

]