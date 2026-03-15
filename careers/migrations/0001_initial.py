from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=50, blank=True)),
                ('cgpa', models.FloatField(default=7.0)),
                ('year', models.CharField(max_length=20, blank=True)),
                ('leetcode', models.IntegerField(default=0)),
                ('github', models.IntegerField(default=0)),
                ('skills', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CareerRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('career', models.CharField(max_length=100)),
                ('score', models.IntegerField()),
                ('skills_have', models.JSONField(default=list)),
                ('skills_missing', models.JSONField(default=list)),
                ('avg_salary', models.CharField(max_length=50)),
                ('demand_trend', models.CharField(max_length=50)),
                ('rank', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='careers.studentprofile')),
            ],
            options={
                'ordering': ['rank'],
            },
        ),
    ]
