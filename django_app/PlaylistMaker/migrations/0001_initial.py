# Generated by Django 4.2.2 on 2024-08-26 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='video_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoid', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('channel', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('views', models.PositiveBigIntegerField()),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('is_selected', models.BooleanField(default=False)),
            ],
        ),
    ]
