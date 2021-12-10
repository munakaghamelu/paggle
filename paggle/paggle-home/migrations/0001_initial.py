# Generated by Django 2.2.24 on 2021-12-08 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('num_of_images', models.IntegerField()),
                ('date_added', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('dataset', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paggle-home.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('model', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paggle-home.Model')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paggle-home.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paggle-home.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='HAM10000_Metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesion_id', models.CharField(max_length=50)),
                ('dx', models.CharField(max_length=10)),
                ('dx_type', models.CharField(max_length=10)),
                ('age', models.DecimalField(decimal_places=1, max_digits=5)),
                ('sex', models.CharField(max_length=50)),
                ('localization', models.CharField(max_length=50)),
                ('image_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paggle-home.Image')),
            ],
        ),
    ]