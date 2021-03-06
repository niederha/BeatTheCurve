# Generated by Django 3.0.3 on 2020-04-05 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20200405_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutingReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('GROCERY_SHOPPING', 'Grocery shopping'), ('MEDICAL', 'Medical reasons'), ('FRIENDS', 'Meet friends'), ('DOG', 'Walk your dog (alone)'), ('EXERCISE', 'Exercise (alone)')], default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Entry date')),
                ('hand_wash_frequency', models.CharField(choices=[('L', 'Less than 3 times'), ('M', 'More than 3 times, but less than 6'), ('H', '6 times or more')], default='M', max_length=1)),
                ('leave', models.BooleanField(choices=[('n', 'No'), ('y', 'yes')])),
                ('crowded_places', models.BooleanField(blank=True, default=None, null=True)),
                ('hand_wash_after_leave', models.BooleanField(blank=True, default=None, null=True)),
                ('reason', models.ManyToManyField(blank=True, default=None, to='main.OutingReason')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
