from django.db import models

class CreateJob(models.Model):
    JOB_TYPE = (
        ("full-time", "Full Time"),
        ("part-time", "Part Time"),
        ("internship", "Internship"),
        ("co-op", "Co-op")
    )
    LOCATION = (
        ("remote", "Remote"),
        ("in-person", "In Person")
    )
    title = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    companyName = models.CharField(max_length=100)
    jobType = models.CharField(max_length=50, default="", choices=JOB_TYPE)
    location = models.CharField(max_length=50, default="",choices=LOCATION)
    applicationDeadline = models.DateField()
    description = models.TextField()
    posted_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class ApplyJob(models.Model):
    PENDING = 'pending'
    IN_REVIEW = 'under_review'
    INTERVIEW = 'inteview'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    JOB_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (IN_REVIEW, 'Under Review'),
        (INTERVIEW, 'Selected for interview'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )
    job = models.ForeignKey(CreateJob, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=12)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/")
    availability_start_date = models.DateField()
    availability_end_date = models.DateField()
    applied_on = models.DateTimeField(auto_now_add=True)
    job_status = models.CharField(max_length=100, choices=JOB_STATUS_CHOICES, default=PENDING)

    class Meta:
        unique_together = ('user', 'job')


