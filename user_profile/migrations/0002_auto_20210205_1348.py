# Generated by Django 3.1.6 on 2021-02-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_referral_code',
            field=models.CharField(default='7azeJF', max_length=6),
        ),
    ]
