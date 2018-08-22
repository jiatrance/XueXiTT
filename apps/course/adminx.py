import xadmin

from .models import Course, Video, CourseResource, Movie,CourseCategory


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    '''课程'''

    list_display = ['name', 'desc', 'detail', 'degree','get_vd_nums']  # 显示的字段
    search_fields = ['name', 'desc', 'detail', 'degree']  # 搜索
    list_filter = ['name', 'desc', 'detail', 'degree']  # 过滤
    model_icon = 'fa fa-book'  # 图标
    ordering = ['-click_nums']  # 排序
    readonly_fields = ['click_nums']  # 只读字段，不能编辑
    exclude = ['fav_nums']  # 不显示的字段
    list_editable = ['degree', 'desc']
    refresh_times = [3, 5]
    style_fields = {"detail": "ueditor"}

    def queryset(self):
        # 重载queryset方法，来过滤出我们想要的数据的
        qs = super(CourseAdmin, self).queryset()
        # 只显示is_banner=True的课程
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        # obj实际是一个course对象
        obj = self.new_obj
        # 如果这里不保存，新增课程，统计的课程数会少一个
        obj.save()
        # 确定课程的课程机构存在。
        if obj.course_org is not None:
            # 找到添加的课程的课程机构
            course_org = obj.course_org
            # 课程机构的课程数量等于添加课程后的数量
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class VideoAdmin(object):
    '''视频'''

    list_display = [ 'name', 'add_time']
    search_fields = [ 'name']
    list_filter = ['name', 'add_time','course']


class MovieAdmin(object):
    '''电影'''

    list_display = ['name', 'add_time']
    search_fields = ['name']
    list_filter = ['name', 'add_time']


class CourseCategoryAdmin(object):
    '''电影'''

    list_display = ['desc']
    search_fields = ['desc']
    list_filter = ['desc']


class CourseResourceAdmin(object):
    '''课程资源'''

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(Movie, MovieAdmin)
xadmin.site.register(CourseCategory,CourseCategoryAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)