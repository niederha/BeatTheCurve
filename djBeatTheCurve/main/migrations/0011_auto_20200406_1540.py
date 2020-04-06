# Generated by Django 3.0.3 on 2020-04-06 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_merge_20200406_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='crowded_places',
            field=models.CharField(choices=[('n', 'No'), ('y', 'Yes')], default='n', max_length=1),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='hand_wash_after_leave',
            field=models.CharField(choices=[('n', 'No'), ('y', 'Yes')], default='y', max_length=1),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='leave',
            field=models.CharField(choices=[('n', 'No'), ('y', 'Yes')], default='n', max_length=1),
        ),
    ]
