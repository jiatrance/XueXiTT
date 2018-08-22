from django.urls import path,re_path
from .views import CourseListView, CourseDetailView,CommentsView,AddCommentsView,VideoView,MoviePlay,MovieCommentsView,\
    PublicCourseView,UnityListView,UnrealListView,MachineLearningListView,DataScienceListView,MovieListView,PublicCourseListView
app_name = "course"

urlpatterns = [
    path('course_list/',CourseListView.as_view(),name='course_list'),
    re_path('course/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    re_path('video/(?P<video_id>\d+)/', VideoView.as_view(),name='video_info'),
    re_path('course_public/(?P<course_id>\d+)/', PublicCourseView.as_view(),name='course_public'),
    path('public_list/', PublicCourseListView.as_view(),name='public_list'),
    path('movie_list/', MovieListView.as_view(),name='movie_list'),
    path('unity_list/', UnityListView.as_view(),name='unity_list'),
    path('unreal_list/', UnrealListView.as_view(),name='unreal_list'),
    path('machine_learning/', MachineLearningListView.as_view(),name='machine_learning'),
    path('data_science/', DataScienceListView.as_view(),name='data_science'),
    path('video_comments/', CommentsView.as_view(), name="video_comments"),
    re_path('movie/(?P<movie_id>\d+)/', MoviePlay.as_view(), name="movie_play"),
    path('add_comment/', AddCommentsView.as_view(), name="add_comment"),
    path('movie/comment',MovieCommentsView.as_view(),name='movie_comment'),
]
