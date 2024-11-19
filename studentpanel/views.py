from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from adminpanel.models import Course,CourseContent,Profile,Enrollment,Coupon,Review,Comment
from django.contrib.auth.models import User
from adminpanel.forms import CustomPasswordChangeForm,ProfileForm,RegistrationForm,EnrollmentForm,CouponForm,ReviewForm,CommentForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.db.models import Avg
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


#Displaying Ongoing and Completed Courses
@login_required(login_url='/404/')
@never_cache
def Student_Home(request):
    ongoing_courses = Enrollment.objects.filter(student=request.user, status='on_progress')
    completed_courses = Enrollment.objects.filter(student=request.user, status='completed')
    
    def get_remaining_time_str(remaining_time):
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days} days, {hours} hours, {minutes} minutes"

    # Calculate remaining time for each course based on enrollment date
    for enrollment in ongoing_courses:
        elapsed_time = now() - enrollment.start_date
        remaining_time = enrollment.course.time_limit - elapsed_time
        if remaining_time.total_seconds() <= 0:
            enrollment.status = 'completed'
            enrollment.save()
        else:
            enrollment.remaining_time_str = get_remaining_time_str(remaining_time)
    
    context = {
        'ongoing_courses': ongoing_courses,
        'completed_courses': completed_courses,
    }
    return render(request, 'studentpanel/student_home.html', context)




#Displaying All Courses
@login_required(login_url='/404/')
@never_cache
def Explore_Course(request):
    all_courses = Course.objects.filter(status='visible').annotate(average_rating=Avg('review__rating'))  # Fetch courses with status 'visible' 
    context = { 
        'all_courses': all_courses, 
        } 
    return render(request, 'studentpanel/explore_course.html',context)

#Details and Enrollment Of Course
@login_required(login_url='/404/')
@never_cache
def Buy_Course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # Check if the user is already enrolled in the course
    is_enrolled = Enrollment.objects.filter(student=user, course=course).exists()

    if request.method == 'POST' and not is_enrolled:
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                coupon = Coupon.objects.get(code=code, course=course, is_active=True)

                # Enroll the user in the course
                Enrollment.objects.create(student=user, course=course, status='on_progress')
                messages.success(request, f'Successfully enrolled in {course.course_name} using the coupon code!')
                coupon.is_active = False  # Deactivate the coupon after use
                coupon.save()

                return redirect('studentpanel:student_home')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid or expired coupon code.')
    else:
        form = CouponForm()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'form': form
    }
    return render(request, 'studentpanel/buy_course.html', context)

#Displaying specific user Profile
@login_required(login_url='/404/')
@never_cache
def View_Profile(request, user_id): 
    user = get_object_or_404(User, id=user_id) # Assuming you have a Profile model associated with User 
    profile = user.profile 
    context = { 
        'user': user, 
        'profile': profile, 
    } 
    return render(request, 'studentpanel/view_profile.html', context)

#Editing Profile
@login_required(login_url='/404/')
@never_cache
def Edit_Profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()

            messages.success(request, 'Profile Updated Successfully')
            return redirect('studentpanel:view_profile', user_id=user_id)
        else:
            messages.error(request, 'Failed to Update Profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    
    return render(request, 'studentpanel/edit_profile.html', context)


#Course Contents,Comments,Review
@login_required(login_url='/404/')
@never_cache
def View_Course(request, course_id, content_id=None):
    course = get_object_or_404(Course, id=course_id)
    contents = course.coursecontent_set.all()
    has_content = contents.exists()

    if content_id:
        selected_content = get_object_or_404(CourseContent, id=content_id, course=course)
    else:
        selected_content = contents.first() if has_content else None

    user_review = Review.objects.filter(course=course, user=request.user).first()
    review_form = ReviewForm(request.POST or None, instance=user_review)
    comment_form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(course=course).order_by('-created_at')

    if request.method == 'POST':
        if 'submit_review' in request.POST and review_form.is_valid():
            review = review_form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('studentpanel:view_course', course_id=course.id)
        elif 'submit_comment' in request.POST and comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.course = course
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('studentpanel:view_course', course_id=course.id)

    context = {
        'course': course,
        'contents': contents,
        'selected_content': selected_content,
        'review_form': review_form,
        'comment_form': comment_form,
        'comments': comments,
        'has_content': has_content,
        'user_review': user_review,
    }
    return render(request, 'studentpanel/view_course.html', context)

#Deleting Review
@login_required(login_url='/404/')
@never_cache
def Delete_Review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    course_id = review.course.id
    review.delete()
    messages.success(request, 'Your review has been deleted.')
    return redirect('studentpanel:view_course', course_id=course_id)

#Deleting Comment
@login_required(login_url='/404/')
@never_cache
def Delete_Comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    course_id = comment.course.id
    comment.delete()
    messages.success(request, 'Your comment has been deleted.')
    return redirect('studentpanel:view_course', course_id=course_id)

#Resetting Password
@login_required(login_url='/404/')
@never_cache
def Reset_Password(request, id=Profile.user):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('studentpanel:student_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'studentpanel/reset_password.html', {'form': form})

#Signing Out
@login_required(login_url='/404/')
@never_cache
def sign_out(request):
    # Log out the user and redirect to the home page
    logout(request)
    return redirect('homepanel:home')