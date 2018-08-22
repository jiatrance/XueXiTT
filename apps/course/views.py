import json
from django.shortcuts import render
from django.views.generic import View
from .models import Course,CourseResource,Video,Movie,MovieComments,CourseCategory
from operation.models import UserFavorite,VideoComments
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from util.mixin_utils import LoginRequiredMixin
from django.db.models import Q
from XueXiTT.settings import MEDIA_URL
from datetime import datetime


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.exclude(is_open=True).order_by('-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name_icontains=search_keywords) |
                                             Q(desc_icontains=search_keywords) | Q(detail_icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,9 , request=request)
        courses = p.page(page)
        return render(request, "all-course.html", {
            "all_courses":courses,
            'sort': sort,
            'hot_courses':hot_courses,
        })


class PublicCourseListView(View):
    def get(self, request):
        all_courses = Course.objects.filter(is_open=True).order_by('-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.filter(is_open=True).order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name_icontains=search_keywords) |
                                             Q(desc_icontains=search_keywords) | Q(detail_icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,9 , request=request)
        courses = p.page(page)
        return render(request, "all-course.html", {
            "all_courses":courses,
            'sort': sort,
            'hot_courses':hot_courses,
        })


class UnityListView(View):
    def get(self, request):
        all_courses = Course.objects.filter(course_category=CourseCategory.objects.get(code='unity')).order_by('-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name_icontains=search_keywords) |
                                             Q(desc_icontains=search_keywords) | Q(detail_icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,9 , request=request)
        courses = p.page(page)
        return render(request, "all-course.html", {
            "all_courses":courses,
            'sort': sort,
            'hot_courses':hot_courses,
        })


class UnrealListView(View):
    def get(self, request):
        all_courses = Course.objects.filter(course_category=CourseCategory.objects.get(code='unreal')).order_by(
            '-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name_icontains=search_keywords) |
                                             Q(desc_icontains=search_keywords) | Q(detail_icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,9 , request=request)
        courses = p.page(page)
        return render(request, "all-course.html", {
            "all_courses":courses,
            'sort': sort,
            'hot_courses':hot_courses,
        })


class MachineLearningListView(View):
    def get(self, request):
        all_courses = Course.objects.filter(course_category=CourseCategory.objects.get(code='ML')).order_by(
            '-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name_icontains=search_keywords) |
                                             Q(desc_icontains=search_keywords) | Q(detail_icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,9 , request=request)
        courses = p.page(page)
        return render(request, "all-course.html", {
            "all_courses":courses,
            'sort': sort,
            'hot_courses':hot_courses,
        })


class DataScienceListView(View):
    def get(self, request):
        all_courses = Course.objects.filter(course_category=CourseCategory.objects.get(code='DS')).order_by(
            '-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name_icontains=search_keywords) |
                                             Q(desc_icontains=search_keywords) | Q(detail_icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,9 , request=request)
        courses = p.page(page)
        return render(request, "all-course.html", {
            "all_courses":courses,
            'sort': sort,
            'hot_courses':hot_courses,
        })


class MovieListView(View):
    def get(self, request):
        all_courses = Movie.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = Movie.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name_icontains=search_keywords) |
                                             Q(desc_icontains=search_keywords) | Q(detail_icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,18 , request=request)
        courses = p.page(page)
        return render(request, "movie_list.html", {
            "all_courses":courses,
            'sort': sort,
            'hot_courses':hot_courses,
        })


class CourseDetailView(View):
    '''课程详情'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        videos=course.get_course_video().order_by('name')
        # 课程的点击数加1
        course.click_nums += 1
        course.save()
        # 课程标签
        # 通过当前标签，查找数据库中的课程
        has_fav_course = False
        has_fav_org = False

        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            # 需要从1开始不然会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        return  render(request, "course-detial.html", {
            'videos':videos,
            'course':course,
            'relate_courses':relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class VideoView(View):

    '''课程章节信息'''
    def get(self,request,video_id):
        video=Video.objects.get(id=video_id)
        video.click_nums=+1
        video.save()
        course=video.course
        videos=course.get_course_video().order_by('name')
        comments=VideoComments.objects.filter(video=video)
        return render(request,'video-list.html',{
            'comments':comments,
            'course':course,
            'video':video,
            'videos':videos,
        })


class PublicCourseView(View):

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        videos = course.get_course_video()
        video = videos.first()
        course.students += 1
        course.save()

        return render(request, 'public-course.html', {
            'video': video,
            'videos': videos,
            'course': course,
        })


class CommentsView(View):
    def post(self,request):
        video_id = request.POST.get('video_id', 0)
        comment=request.POST.get('comment', '')

        if int(video_id) > 0 and comment:
            video_comment = VideoComments()
            video = Video.objects.get(id=int(video_id))
            video_comment.video = video
            video_comment.comments=comment
            video_comment.user=request.user
            video_comment.add_time=datetime.now()
            video_comment.save()

            data={
                "status": "success",
                'img':MEDIA_URL+video_comment.user.image.path,
                'name':video_comment.user.nick_name,
                'comments':video_comment.comments,
                'add_time':video_comment.add_time.strftime('%Y-%m-%d %H:%M:%S')
            }

            return HttpResponse(json.dumps(data), content_type='application/json')

        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class AddCommentsView(LoginRequiredMixin,View):
    def get(self,request):
        course_id=request.POST.get('course_id', 0)
        comments=request.POST.get('comments', '')

        if int(course_id) > 0 and comments:
            movie_comments = MovieComments()
            course = Course.objects.get(id=int(course_id))
            movie_comments.course = course
            movie_comments.comments=comments
            movie_comments.user=request.user
            movie_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


class MovieCommentsView(LoginRequiredMixin,View):
    def post(self,request):
        movie_id = request.POST.get('movie_id', 0)
        comment=request.POST.get('comment', '')

        if int(movie_id) > 0 and comment:
            user_comment = MovieComments()
            movie = Movie.objects.get(id=int(movie_id))
            user_comment.movie = movie
            user_comment.comments=comment
            user_comment.user=request.user
            user_comment.add_time=datetime.now()
            user_comment.save()

            data={
                "status": "success",
                'img':MEDIA_URL+user_comment.user.image.path,
                'name':user_comment.user.nick_name,
                'comments':user_comment.comments,
                'add_time':user_comment.add_time.strftime('%Y-%m-%d %H:%M:%S')
            }

            return HttpResponse(json.dumps(data), content_type='application/json')

        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class MoviePlay(View):
    def get(self,request,movie_id):
        movie=Movie.objects.get(id=movie_id)
        movie.click_nums+=1
        movie.save()
        comments=MovieComments.objects.filter(movie=movie).order_by('-add_time')
        return render(request,'movie.html',{
            'movie':movie,
            'comments':comments,
        })