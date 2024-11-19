from django.urls import path
from .views import Student_Home,Explore_Course,Buy_Course,View_Course,View_Profile,Edit_Profile,Delete_Review,Delete_Comment,Reset_Password,sign_out

app_name = 'studentpanel'

urlpatterns = [
    path('',Student_Home,name='student_home'),
    path('explore_course',Explore_Course,name='explore_course'),
    path('buy_course/<int:course_id>/',Buy_Course,name='buy_course'),
    path('view_profile/<int:user_id>/',View_Profile,name='view_profile'),
    path('edit_profile/<int:user_id>/',Edit_Profile,name='edit_profile'),
    path('reset_password',Reset_Password,name='reset_password'),
    path('sign_out/', sign_out, name='sign_out'),

    path('view_course/<int:course_id>/',View_Course,name='view_course'),
    path('course/<int:course_id>/content/<int:content_id>/', View_Course, name='view_course_content'),
    path('delete_review/<int:review_id>/',Delete_Review, name='delete_review'),
    path('delete_comment/<int:comment_id>/',Delete_Comment, name='delete_comment'),

]