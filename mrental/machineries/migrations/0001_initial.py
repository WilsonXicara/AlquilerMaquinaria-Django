# Generated by Django 2.2.7 on 2019-11-22 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machinery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on wich the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on wich the object was last modified.', verbose_name='modified at')),
                ('code', models.SlugField(unique=True)),
                ('machinery_type', models.CharField(max_length=75, verbose_name='machinery type')),
                ('name', models.CharField(max_length=75, verbose_name='machinery name')),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='machineries/pictures/')),
                ('is_rented', models.BooleanField(default=False)),
                ('default_amount', models.FloatField(default=0.0, help_text='The default amount for renting this machinery')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
