# Generated by Django 2.0.6 on 2018-07-15 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180715_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('female', '女'), ('male', '男')], default='female', max_length=10, verbose_name='性别'),
        ),
    ]
