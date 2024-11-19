from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Admin_Home,Reset_AdminEmail,View_Profile,Profile_List,toggle_profile_status,View_Course,Course_List,Generate_Coupons,toggle_status,Add_CourseCategory,Edit_Category,Delete_Category,Add_Course,Add_Content,Edit_Content,Delete_Content,Edit_Course,Delete_Course,Review_List,Reset_Password,sign_out

app_name = 'adminpanel'

urlpatterns = [

    #Home Page
    path('',Admin_Home,name='admin_home'),

    #PROFILE SECTION
    path('reset_adminemail/<int:user_id>/',Reset_AdminEmail,name='reset_adminemail'),
    path('reset_password',Reset_Password,name='reset_password'),
    path('view_profile/<int:profile_id>/',View_Profile,name='view_profile'),
    path('profile_list/',Profile_List,name='profile_list'),
    path('toggle_profile_status/<int:profile_id>/', toggle_profile_status, name='toggle_profile_status'),
    path('sign_out/', sign_out, name='sign_out'),
    
    #COURSE SECTION
    path('add_course',Add_Course,name='add_course'),
    path('view_course/<int:course_id>/',View_Course,name='view_course'),
    path('course_list',Course_List,name='course_list'),
    path('toggle_status/<int:course_id>/', toggle_status, name='toggle_status'),
    path('edit_course/<int:course_id>/',Edit_Course,name='edit_course'),
    path('delete_course/<int:course_id>/',Delete_Course,name='delete_course'),
  
    #CATEGORY SECTION
    path('add_coursecategory',Add_CourseCategory,name='add_coursecategory'),
    path('edit_category/<int:category_id>/',Edit_Category,name='edit_category'),
    path('delete_category/<int:category_id>/', Delete_Category, name="delete_category"),
  
    #CONTENT SECTION
    path('add_content/<int:course_id>/',Add_Content,name='add_content'),
    path('edit_content/<int:content_id>/',Edit_Content,name='edit_content'),
    path('delete_content/<int:content_id>/', Delete_Content, name="delete_content"),


    path('generate_coupons/',Generate_Coupons,name='generate_coupons'),
    
    path('review_list/',Review_List,name='review_list'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)