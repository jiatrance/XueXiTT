from django.urls import path,re_path
from . import views

app_name='users'

urlpatterns=[
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
    re_path('active/(?P<active_code>.*)/',views.ActiveUserView.as_view(),name='user_active'),
    re_path('reset/(?P<active_code>.*)/',views.ResetView.as_view(),name='reset'),
    path('forget/',views.ForgetPwdView.as_view(),name='forget_pwd'),
    path('modify_pwd',views.ModifyPwdView.as_view(),name='modify_pwd'),
    path('users/info/',views.UserInfoView.as_view(),name='user_info'),
    path('image/upload',views.UploadImageView.as_view(),name='image_upload'),
    path("update/pwd/", views.UpdatePwdView.as_view(),name='update_pwd'),
    path("sendemail_code/", views.SendEmailCodeView.as_view(), name='sendemail_code'),
    path("update_email/", views.UpdateEmailView.as_view(), name='update_email'),
    path("users/mycourse/", views.MyCourseView.as_view(),name='my_course'),
    path('users/my_message/', views.MyMessageView.as_view(), name="my_message"),
    path('myfav/org/', views.MyFavOrgView.as_view(), name="myfav_org"),
    path('myfav/teacher/',views.MyFavTeacherView.as_view(),name='myfav_teacher'),
    path('myfav/course/', views.MyFavCourseView.as_view(), name="myfav_course"),
]