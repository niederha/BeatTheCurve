# Generated by Django 3.0.3 on 2020-04-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200406_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outingreason',
            name='name',
            field=models.CharField(choices=[('NOT_OUT', 'Did not go out'), ('GROCERY_SHOPPING', 'Grocery shopping'), ('MEDICAL', 'Medical reasons'), ('FRIENDS', 'Meet friends'), ('DOG', 'Walk your dog (alone)'), ('EXERCISE', 'Exercise (alone)')], default='NOT_OUT', max_length=200),
        ),
    ]