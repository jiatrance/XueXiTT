import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render,render_to_response
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from util.email_send import send_register_email
from util.mixin_utils import LoginRequiredMixin
from .form import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm
from .models import UserProfile, EmailVerifyRecord
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from course.models import Course,Movie
from pure_pagination import Paginator,PageNotAnInteger


class LoginView(View):

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        login_form=LoginForm(request.POST)
        print('1')
        if login_form.is_valid():
            email=request.POST.get('username',None)
            password=request.POST.get('password',None)

            user=authenticate(username=email,password=password)

            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request,'login.html',{'msg':'用户密码错误','login_form':login_form })
        else:
            return render(request,'login.html',{ 'msg':'用户密码格式错误', 'login_form':login_form })


class LogoutView(View):
    '''用户登出'''
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            name=request.POST.get('username','name')
            user_name=request.POST.get('email',None)
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'msg':'用户已存在请登录邮箱激活'})
            pass_word=request.POST.get('password',None)
            re_password=request.POST.get('re_password',None)

            if pass_word == re_password:
                user_profile=UserProfile()
                user_profile.username=user_name
                user_profile.email=user_name
                user_profile.is_active=False
                user_profile.nick_name=name
                user_profile.password=make_password(pass_word)
                user_profile.save()
                send_register_email(user_name,'register')
                return render(request,'login.html',{'msg':'注册成功请登录邮箱激活'})
            else:
                return render(request, 'register.html', {'msg':'密码不一致'})
        else:
            return render(request,'register.html',{'register_form':register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        all_record=EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                email=record.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request,'active_fail.html')

        return render(request,'login.html')


class ForgetPwdView(View):
    def get(self,request):
        forget_form=ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form=ForgetPwdForm(request.POST)

        if forget_form.is_valid():
            email=request.POST.get('email',None)
            send_register_email(email,'forget')
            return render(request,'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})


class ResetView(View):
    def get(self,request,active_code):
        all_recodes=EmailVerifyRecord.objects.filter(code=active_code)
        if all_recodes:
            for record in all_recodes:
                email=record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')

        return render(request,'login.html')


class ModifyPwdView(View):
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1','')
            pwd2 = request.POST.get('password2', '')
            email=request.POST.get('email','')
            if pwd1!=pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致'})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()

            return render(request,'login.html')
        else:
            email=request.POST.get('email','')
            return render(request,'password_reset.html',{"email":email, "modify_form":modify_form })


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'my_info.html')


class UploadImageView(LoginRequiredMixin,View):
    '''用户图像修改'''
    def post(self,request):

#   上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        files=request.FILES.getlist('file_data')
        print(files)
        for file in files:
            image = file
            print(image)
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',  content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    '''发送邮箱修改验证码'''
    def get(self,request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')

        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''修改邮箱'''
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):

    '''我的课程'''
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "user_courses":user_courses,
        })


class MyFavOrgView(LoginRequiredMixin,View):
    '''我收藏的课程机构'''

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self,request):
        teacher_list=[]
        fav_teachers=UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id=fav_teacher.fav_id
            teacher=Teacher.objects.filter(id=teacher_id)
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin,View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list":course_list,})


class MyMessageView(LoginRequiredMixin, View):
    '''我的消息'''

    def get(self, request):
        all_message = UserMessage.objects.filter(user= request.user.id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4,request=request)
        messages = p.page(page)
        return  render(request, "usercenter-message.html", {
        "messages":messages,
        })


class Root(View):
    def get(self,request):
        return render(request, 'root.txt')

class IndexView(View):
    '''首页'''
    def get(self,request):
        #课程
        courses = Course.objects.exclude(is_open=True).order_by('-add_time')[:6]
        recommend=Course.objects.exclude(is_open=True).order_by('-click_nums')[:6]
        recent=Course.objects.exclude(is_open=True).order_by('-add_time')[:3]
        movie=Movie.objects.all().order_by('-add_time')[:6]
        #轮播课程
        banner_courses = Course.objects.filter(is_banner=True).order_by('-add_time')
        banner_first=banner_courses.first()
        list_banner=banner_courses[1:3]
        #课程机构
        open_courses = Course.objects.filter(is_open=True).order_by('-add_time')[:6]
        return render(request,'index.html',{
            'banner_first':banner_first,
            'courses':courses,
            'recent':recent,
            'list_banner':list_banner,
            'open_courses':open_courses,
            'recommend':recommend,
            'movie':movie,
        })


def page_not_found(request):
    response=render_to_response('404.html',{})
    response.status_code=404
    return response


def page_error(request):
    response=render_to_response('500.html',{})
    response.status_code=500
    return response
