from django import forms
from .models import Profile,Course,CourseCategory,CourseContent,Review,Enrollment,Coupon,Comment
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .utils import generate_unique_coupon_code


class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Image',required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
    }))
    phone = forms.CharField(label='Phone',max_length=13,required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Enter phone number'
    }))
    class Meta:
        model = Profile
        fields =['profile_image','phone']


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your First Name'
    }))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Last Name'
    }))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Username'
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Email'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Password'
    }))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Re-enter Your Password'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    username = forms.CharField(label = 'Usename',
                               max_length = 100,
                               required = True,
                               widget = forms.TextInput(attrs={
        'class':'form-control','placeholder':'Enter Your Username'
    }))
    password = forms.CharField(label = 'Password',
                               max_length = 100,
                               required = True,
                               widget = forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Password'
    })) 

class EmailResetForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={ 
        'class': 'form-control', 
        'placeholder': 'Enter Your email address'
    }))

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your old password'
        })
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password'
        })
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

class CourseCategoryForm(forms.ModelForm):
    category = forms.CharField(label='Category Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter The Category Name'
    }))
    class Meta:
        model = CourseCategory
        fields ='__all__'

class CourseForm(forms.ModelForm):
    course_name = forms.CharField(label='Course Name',widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Enter Course Name'
    }))
    course_description = forms.CharField(label='Course Description', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Course Description'
    }))
    course_price = forms.DecimalField(label='Course Price', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Course Price'
    }))
    course_image = forms.ImageField(label='Course Image', widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
    }))
    course_category = forms.ModelChoiceField(label='Category', queryset = CourseCategory.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',     
    }))
    status = forms.ChoiceField(label='Status', choices=[
        ('hidden', 'Hidden'),
        ('visible', 'Visible')
    ], widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    class Meta:
        model = Course
        fields = ['course_name','course_description','course_price','course_image','course_category','status']

class ContentForm(forms.ModelForm):
    content_name = forms.CharField(label='Content Name',widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Enter Content Name'
    }))
    # course = forms.ModelChoiceField(label='Course', queryset = Course.objects.all(), widget=forms.Select(attrs={
    #     'class': 'form-control',     
    # }))
    course_video = forms.FileField(label='Course Video', widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
    }), required=False)
    note = forms.FileField(label='Note (PDF)', widget=forms.ClearableFileInput(attrs={
        'class': 'form-control-file',
    }), required=False)
    class Meta:
        model = CourseContent
        fields = ['content_name','course_video','note']

    def clean_note(self):
        note = self.cleaned_data.get('note')
        if note and not note.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed for the curriculum.")
        return note


class CouponForm(forms.Form):
    code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Coupon Code'
    }))
    class Meta:
        model = Coupon
        fields =['code']


class GenerateCouponForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    def generate_coupon(self):
        course = self.cleaned_data['course']
        code = generate_unique_coupon_code()
        coupon = Coupon.objects.create(course=course, code=code)
        return coupon


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = []

