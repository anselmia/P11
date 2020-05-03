# Generated by Django 3.0.4 on 2020-05-03 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Famille',
            },
        ),
        migrations.CreateModel(
            name='Substitute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family', to='substitute.Family')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='home.Product')),
                ('substitute_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substitute', to='home.Product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Favoris',
                'verbose_name_plural': 'Favoris',
            },
        ),
        migrations.AddConstraint(
            model_name='substitute',
            constraint=models.UniqueConstraint(fields=('product_id', 'substitute_id', 'user_id'), name='unique_relation'),
        ),
        migrations.AddConstraint(
            model_name='family',
            constraint=models.UniqueConstraint(fields=('name', 'user_id'), name='unique'),
        ),
    ]
