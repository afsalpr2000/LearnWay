from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='media',blank=True,null=True)
    phone = models.CharField(max_length = 13,blank=True, null=True)
    course_enrolled = models.ManyToManyField('Course',blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class CourseCategory(models.Model):
    category = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.category


class Course(models.Model):
    STATUS_CHOICES = [
        ('hidden','Hidden'),
        ('visible','Visible')
    ]
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()
    course_price = models.DecimalField(max_digits=8, decimal_places=2,default=0.00)
    course_image = models.ImageField(upload_to='course_imgs',blank=True, null=True)
    admin = models.ForeignKey(User,on_delete=models.CASCADE)
    course_category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Visible')
    time_limit = models.DurationField(default=timedelta(days=30))

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ['-created_at']


class CourseContent(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    content_name = models.CharField(max_length=40)
    course_video = models.FileField(upload_to='videos/', blank=True, null=True)
    note = models.FileField(upload_to='pdfs/', blank=True, null=True)
    completed_by = models.ManyToManyField(User, related_name='completed_contents', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_completed(self, user): 
        return self.completed_by.filter(id=user.id).exists()

    # def __str__(self):
    #     return self.content_name


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.course_name}'


class Comment(models.Model):
    course = models.ForeignKey(Course, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.course_name}'





class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('on_progress','On_progress'),
        ('completed','Completed')
    ]
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)  # Represents percentage (0-100)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='On_progress')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.course_name}"


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code




