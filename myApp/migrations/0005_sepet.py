# Generated by Django 4.0.5 on 2022-10-29 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myApp', '0004_usersave'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sepet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adet', models.IntegerField(verbose_name='Adet')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.post', verbose_name='Araba')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
        ),
    ]