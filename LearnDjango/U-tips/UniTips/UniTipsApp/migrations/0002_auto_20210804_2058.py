# Generated by Django 3.2.5 on 2021-08-04 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UniTipsApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='subj_content',
        ),
        migrations.AddField(
            model_name='subjects',
            name='uni_related',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('on_topic', models.CharField(max_length=50)),
                ('subj_content', models.TextField()),
                ('subj_prof', models.CharField(max_length=50)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniTipsApp.subjects')),
            ],
        ),
    ]
