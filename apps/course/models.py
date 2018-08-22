from django.db import models
from datetime import datetime
from organization.models import CourseOrg,Teacher
from DjangoUeditor.models import UEditorField
from users.models import UserProfile


class CourseCategory(models.Model):
    code=models.CharField('code',default='',max_length=10)
    desc=models.CharField('描述',default='',max_length=100)

    class Meta:
        verbose_name='课程类别'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.desc


class Course(models.Model):
    thumbnail=models.ImageField('缩略图', upload_to='img/%Y%M', default='img/default.png', max_length=100, null=True,
                              blank=True)
    degree_choice=(('junior','初级'),('high','中级'),('senior','高级'))
    name=models.CharField('课程名',max_length=50)
    desc=models.CharField('课程描述',max_length=500)
#    detail=models.TextField('课程详情')
    detail = models.TextField('课程详情',default='')
    degree=models.CharField('难度',choices=degree_choice,max_length=10)
    course_category=models.ForeignKey(CourseCategory,verbose_name='课程类别',null=True, blank=True, on_delete=models.CASCADE)
    students = models.IntegerField("学习人数", default=0)
    like_nums = models.IntegerField('收藏数', default=0)
    fav_nums=models.IntegerField('收藏数',default=0)
    image = models.ImageField('封面',upload_to='img/%Y%M',default='img/default.png', max_length=100, null=True, blank=True)
    click_nums=models.IntegerField('点击数',default=0)
    tag = models.CharField('课程标签', default='', max_length=10, null=True, blank=True)
    add_time=models.DateTimeField('添加时间',default=datetime.now)
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True, on_delete=models.CASCADE)
    is_banner = models.BooleanField('是否轮播', default=False)
    banner = models.ImageField('封面',upload_to='ban/%Y%M', max_length=100, null=True, blank=True)
    is_open=models.BooleanField('是否公开课', default=False)

    class Meta:
        verbose_name='课程'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

    def get_course_video(self):
        return self.video_set.all()

    def get_first_video(self):
        return self.get_course_video().first()

    def get_vd_nums(self):
        # 获取课程的章节数
        return self.video_set.all().count()

    get_vd_nums.short_description = '章节数'


class Video(models.Model):
    course=models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name=models.CharField('视频名',max_length=100)
    add_time=models.DateTimeField('添加时间',default=datetime.now)
    url = models.CharField('视频路径',max_length=1000)
    learn_times = models.IntegerField("学习时长(分钟数)", default=0)
    en_subtitle=models.FileField('英文字幕',upload_to='en_subtitle/%Y%M',null=True, blank=True)
    cn_subtitle = models.FileField('中文字幕', upload_to='cn_subtitle/%Y%M', null=True, blank=True)
    click_nums=models.IntegerField('点击数',default=0)

    class Meta:
        verbose_name='视频'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course=models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name=models.CharField('视频名',max_length=100)
    add_time=models.DateTimeField('添加时间',default=datetime.now)
    download=models.FileField('资源文件',upload_to='course/resource/%Y/%m',max_length=100)

    class Meta:
        verbose_name='课程资源'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class Movie(models.Model):
    thumbnail=models.ImageField('缩略图', upload_to='img/%Y%M', default='img/default.png', max_length=100, null=True,
                              blank=True)
    url=models.CharField('观看地址',max_length=500,default='')
    name = models.CharField('视频名', max_length=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    download = models.CharField('下载地址',max_length=500, null=True, blank=True)
    click_nums = models.IntegerField('点击数', default=0)

    class Meta:
        verbose_name='电影'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class MovieComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie, verbose_name='电影', on_delete=models.CASCADE)
    comments = models.CharField('评论', max_length=500)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name