# Generated by Django 3.1.5 on 2021-03-05 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0008_delete_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='books/pdfs/')),
            ],
        ),
    ]
