# Generated by Django 3.1.5 on 2021-05-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SoftWord', '0003_comment_like_networks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like', max_length=10),
        ),
    ]