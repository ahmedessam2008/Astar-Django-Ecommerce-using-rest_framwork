# Generated by Django 4.0.4 on 2022-05-30 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userprofile_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.IntegerField(blank=True, max_length=50, null=True),
        ),
    ]