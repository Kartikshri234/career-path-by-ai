# Generated migration for resume_screener models
import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ScreeningSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('job_description', models.TextField()),
                ('jd_word_count', models.IntegerField(default=0)),
                ('resume_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ResumeResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('score', models.FloatField()),
                ('strength_label', models.CharField(max_length=50)),
                ('strength_color', models.CharField(max_length=30)),
                ('strength_emoji', models.CharField(max_length=10)),
                ('strength_tier', models.CharField(max_length=5)),
                ('resume_skills', models.JSONField(default=list)),
                ('matched_keywords', models.JSONField(default=list)),
                ('missing_keywords', models.JSONField(default=list)),
                ('matched_skills', models.JSONField(default=list)),
                ('missing_skills', models.JSONField(default=list)),
                ('kw_score', models.IntegerField(default=0)),
                ('skill_score', models.IntegerField(default=0)),
                ('word_count', models.IntegerField(default=0)),
                ('ats_score', models.IntegerField(default=0)),
                ('ats_details', models.JSONField(default=dict)),
                ('rank', models.IntegerField(default=1)),
                ('session', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='results',
                    to='resume_screener.screeningsession',
                )),
            ],
            options={
                'ordering': ['rank'],
            },
        ),
    ]
