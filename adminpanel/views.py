from django.shortcuts import render, redirect,get_object_or_404
from .forms import CourseForm,CourseCategoryForm,ContentForm,EmailResetForm
from .models import CourseCategory, Course ,Profile,CourseContent,Enrollment,Review
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomPasswordChangeForm,GenerateCouponForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



# Create your views here.

#Displaying Home Contents
@login_required(login_url='/404/')
@never_cache
def Admin_Home(request):
    total_course = Course.objects.count()
    total_category = CourseCategory.objects.count()
    total_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_reviews = Review.objects.count()
    
    latest_profiles = Profile.objects.filter(user__is_staff=False, user__is_superuser=False).order_by('-user__date_joined')[:5]
    latest_courses = Course.objects.order_by('-created_at')[:5]
    latest_reviews = Review.objects.order_by('-created_at')[:5]
    
    context = {
        'total_course': total_course,
        'total_category': total_category,
        'total_users': total_users,
        'total_reviews': total_reviews,
        'latest_profiles':latest_profiles,
        'latest_courses':latest_courses,
        'latest_reviews': latest_reviews,
    }
    return render(request,'adminpanel/admin_home.html',context)

#Reseting Email of Admin
@login_required(login_url='/404/')
@never_cache
def Reset_AdminEmail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EmailResetForm(request.POST) 
        if form.is_valid(): 
            user.email = form.cleaned_data['email'] 
            user.save() 
            messages.success(request, "Email Updated Successfully") 
            return redirect('adminpanel:admin_home') 
    else: 
        form = EmailResetForm(initial={'email': user.email}) 
        return render(request, 'adminpanel/reset_adminemail.html', {'form': form, 'user':user})

#Displaying specific user Profile
@login_required(login_url='/404/')
@never_cache
def View_Profile(request, profile_id): 
    profile = get_object_or_404(Profile, id=profile_id) 
    enrollments = Enrollment.objects.filter(student=profile.user)
    return render(request, 'adminpanel/view_profile.html', {'profile':profile,'enrollments':enrollments})

#Displaying Profiles
@login_required(login_url='/404/')
@never_cache
def Profile_List(request): 
    profiles = Profile.objects.filter(user__is_staff=False, user__is_superuser=False) 
    return render(request, 'adminpanel/profile_list.html',{'profile_list': profiles})

#Blocking and UnBlocking Profiles
@login_required(login_url='/404/')
@never_cache
def toggle_profile_status(request, profile_id): 
    profile = get_object_or_404(Profile, id=profile_id) 
    profile.is_blocked = not profile.is_blocked 
    profile.save() 
    messages.success(request, f'{profile.user.username} has been {"unblocked" if not profile.is_blocked else "blocked"}.') 
    return redirect('adminpanel:profile_list')

#Adding course category
@login_required(login_url='/404/')
@never_cache
def Add_CourseCategory(request):
    categories = CourseCategory.objects.all().order_by('-id')
    if request.method=='POST':
        form=CourseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('adminpanel:add_coursecategory')
    else:
        form=CourseCategoryForm()
    return render(request,'adminpanel/add_coursecategory.html',{'form':form,'categories':categories})

#Editing Course Category
@login_required(login_url='/404/')
@never_cache
def Edit_Category(request, category_id):
    category = get_object_or_404(CourseCategory, id = category_id)
    if request.method =='POST':
        form = CourseCategoryForm(request.POST,instance = category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('adminpanel:add_coursecategory')
    else:
        form = CourseCategoryForm(instance = category)
    return render(request,'adminpanel/edit_category.html',{'form':form})

#Deleting Course Category
@login_required(login_url='/404/')
@never_cache
def Delete_Category(request,category_id):   
    category = get_object_or_404(CourseCategory, id = category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
    return redirect('adminpanel:add_coursecategory')

#Showing all courses
@login_required(login_url='/404/')
@never_cache
def Course_List(request):
    course_list = Course.objects.all()
    return render(request,'adminpanel/course_list.html',{'course_list':course_list})

#For hiding and showing courses
@login_required(login_url='/404/')
@never_cache
def toggle_status(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.status == 'visible':
        course.status = 'hidden'
    else:
        course.status = 'visible'
    course.save()
    return redirect('adminpanel:course_list')

#Adding Course
@login_required(login_url='/404/')
@never_cache
def Add_Course(request):
    if request.method=='POST':
        form=CourseForm(request.POST, request.FILES)
        if form.is_valid():
            courses = form.save(commit=False)
            courses.admin = request.user
            courses.save()
            messages.success(request,"Course Added Successfully!")
            return redirect('adminpanel:course_list')
    else:
        form=CourseForm()
    return render(request,'adminpanel/add_course.html',{'form':form})

#Editing Course
@login_required(login_url='/404/')
@never_cache
def Edit_Course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course Updated Successfully!")
            return redirect('adminpanel:view_course',course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'adminpanel/edit_course.html', {'form': form, 'course': course})

#Deleting Course
@login_required(login_url='/404/')
@never_cache
def Delete_Course(request, course_id): 
    course = get_object_or_404(Course, id=course_id) 
    if request.method == 'POST': 
        course.delete() 
        messages.success(request, "Course Deleted Successfully!") 
        return redirect('adminpanel:course_list') 
    return redirect('adminpanel:view_course', course_id=course.id)

#Adding Content to specific course
@login_required(login_url='/404/')
@never_cache
def Add_Content(request, course_id): 
    course = get_object_or_404(Course, id=course_id) 
    if request.method == 'POST': 
        form = ContentForm(request.POST, request.FILES) 
        if form.is_valid(): 
            if form.cleaned_data.get('course_video') or form.cleaned_data.get('note'): 
                content = form.save(commit=False) 
                content.course = course # Associate content with the course 
                content.save() 
                messages.success(request, "Content Added Successfully!") 
                return redirect('adminpanel:view_course', course_id=course.id) 
            else: 
                messages.error(request, "Please add either a video or a PDF note.") 
    else: 
        form = ContentForm(initial={'course': course}) 
    return render(request, 'adminpanel/add_content.html', {'form': form, 'course':course})

#Editing Content
@login_required(login_url='/404/')
@never_cache
def Edit_Content(request, content_id): 
    content = get_object_or_404(CourseContent, id=content_id) 
    if request.method == 'POST': 
        form = ContentForm(request.POST, request.FILES, instance=content) 
        if form.is_valid(): 
            form.save() 
            messages.success(request, "Content updated successfully.") 
            return redirect('adminpanel:view_course', course_id=content.course.id) 
    else: form = ContentForm(instance=content) 
    return render(request, 'adminpanel/edit_content.html', {'form': form, 'content':content})

#Deleting Content
@login_required(login_url='/404/')
@never_cache
def Delete_Content(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    course_id = content.course.id
    if request.method == 'POST':
        content.delete()
        messages.success(request, "Content Deleted Successfully!")
        return redirect('adminpanel:view_course', course_id=course_id)
    return redirect('adminpanel:view_course', course_id=course_id)

#Displaying Contents in a specific Course
@login_required(login_url='/404/')
@never_cache
def View_Course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_contents = CourseContent.objects.filter(course=course)
    context = {
        'course': course,
        'course_contents': course_contents,
    }
    return render(request, 'adminpanel/view_course.html',context)

#Generating Coupon to Specific Courses
@login_required(login_url='/404/')
@never_cache
def Generate_Coupons(request):
    coupon_code = None
    if request.method == 'POST':
        form = GenerateCouponForm(request.POST)
        if form.is_valid():
            coupon = form.generate_coupon()
            coupon_code = coupon.code
            messages.success(request, f'Successfully generated a coupon.')
            # We don't redirect here to keep the generated coupon in the context
    else:
        form = GenerateCouponForm()
    
    return render(request, 'adminpanel/generate_coupons.html', {'form': form, 'coupon_code': coupon_code})


#Displaying all Reviews
@login_required(login_url='/404/')
@never_cache
def Review_List(request):
    reviews = Review.objects.all().select_related('user', 'course')
    context = {
        'reviews': reviews
    }
    return render(request, 'adminpanel/review_list.html', context)



#Reseting Password
@login_required(login_url='/404/')
@never_cache
def Reset_Password(request, id=Profile.user):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('adminpanel:admin_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'adminpanel/reset_password.html', {'form': form})

#Signing Out
@login_required(login_url='/404/')
@never_cache
def sign_out(request):
    # Log out the user and redirect to the home page
    logout(request)
    return redirect('homepanel:home')