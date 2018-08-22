import xadmin
from .models import EmailVerifyRecord
from xadmin import views


class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True


class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']


class GlobalSettings(object):
    site_title='Unity教育网后台'
    site_footer='佳佳的公司'
    menu_style='accordion'


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)