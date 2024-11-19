from django.contrib import admin
from .models import Profile,CourseCategory,Course,CourseContent,Review,Enrollment,Coupon

# Register your models here.

admin.site.register(Profile)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CourseContent)
admin.site.register(Review)
admin.site.register(Enrollment)
admin.site.register(Coupon)
