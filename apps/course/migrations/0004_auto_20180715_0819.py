# Generated by Django 2.0.6 on 2018-07-15 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20180715_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='cn_subtitle',
            field=models.FileField(blank=True, null=True, upload_to='cn_subtitle/%Y%M', verbose_name='中文字幕'),
        ),
        migrations.AddField(
            model_name='video',
            name='en_subtitle',
            field=models.FileField(blank=True, null=True, upload_to='en_subtitle/%Y%M', verbose_name='英文字幕'),
        ),
    ]