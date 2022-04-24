# Generated by Django 4.0.1 on 2022-04-24 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
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
            name='HAM10000_Metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesion_id', models.TextField(null=True)),
                ('image_id', models.TextField(null=True)),
                ('dx', models.TextField(null=True)),
                ('dx_type', models.TextField(null=True)),
                ('age', models.TextField(null=True)),
                ('sex', models.TextField(null=True)),
                ('localization', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ML_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_link', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confusion_matrix', models.FileField(null=True, upload_to='')),
                ('metric_results', models.FileField(null=True, upload_to='')),
                ('model', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paggle_home.ml_model')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='HAM10000_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paggle_home.dataset')),
            ],
        ),
    ]
