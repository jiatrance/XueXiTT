from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg,CityDict,Teacher
from course.models import Course
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from .form import UserAskForm
from django.http import HttpResponse
from operation.models import UserFavorite
from django.db.models import Q


class OrgView(View):
    def get(self,request):
        all_orgs=CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name_icontains=search_keywords) |
                                             Q(desc_icontains=search_keywords) | Q(detail_icontains=search_keywords))

        category=request.GET.get('ct','')
        if category:
            all_orgs=all_orgs.filter(category=category)

        all_cities=CityDict.objects.all()

        city_id=request.GET.get('city','')
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))

        sort=request.GET.get('sort','')
        if sort:
            if sort=='students':
                all_orgs=all_orgs.order_by('-students')
            elif sort=='courses':
                all_orgs=all_orgs.order_by('-course_nums')
        try:
            page=request.GET.get('page',1)
        except PageNotAnInteger:
            page=1
        org_onums = all_orgs.count()
        p=Paginator(all_orgs,5,request=request)
        orgs=p.page(page)
        return render(request,'org-list.html',
                          {
                             'all_orgs':orgs,
                              'all_cities':all_cities,
                              'org_onums':org_onums,
                              'city_id':city_id,
                              'category':category,
                              'hot_orgs':hot_orgs,
                              'sort':sort,
                          }
                      )


class AddUserAskView(View):
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask=userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}",content_type='application/jason')
        else:
            return HttpResponse("{'status':'fail','msg':'添加出错'}",content_type='application/jason')


class OrgHomeView(View):
    def get(self,request,org_id):
        current_page = 'home'
        course_org=CourseOrg.objects.get(id=int(org_id))
        all_courses=course_org.course_set.all()[:4]
        all_teacher=course_org.teacher_set.all()[:2]
        return  render(request,'org-detail-homepage.html',{
            'course_org':course_org,
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'current_page':current_page,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id= int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_courses = course_org.course_set.all()

        return render(request, 'org-detail-course.html',{
           'all_courses':all_courses,
            'course_org': course_org,
            'current_page':current_page,
        })


class OrgTeacherView(View):

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id= int(org_id))
        all_teacher = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html',{
           'all_teacher':all_teacher,
            'course_org': course_org,
            'current_page':current_page,
        })


class OrgDescView(View):
    '''机构介绍页'''
    def get(self, request, org_id):
        current_page = 'desc'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id= int(org_id))
        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page':current_page,
        })


class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self, request):
        id = request.POST.get('fav_id', 0)         # 防止后边int(fav_id)时出错
        type = request.POST.get('fav_type', 0)     # 防止int(fav_type)出错

        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_record:
            # 如果记录已经存在，表示用户取消收藏
            exist_record.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(type) == 3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        # 总共有多少老师使用count进行统计
        teacher_nums = all_teachers.count()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_teachers = all_teachers.filter(name__icontains=search_keywords)
        # 人气排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        #讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 9, request=request)
        teachers = p.page(page)
        return render(request, "all-teacher.html", {
            "all_teachers": teachers,
            "teacher_nums": teacher_nums,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = Course.objects.filter(teacher=teacher)
        open_course=Course.objects.filter(Q(is_open=True)&Q(teacher=teacher))
        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {
            'open_course':open_course,
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teacher': sorted_teacher,
        })