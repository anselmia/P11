# Generated by Django 3.0.4 on 2020-04-24 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0004_auto_20200424_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='substitute',
            name='family_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family', to='substitute.Family'),
        ),
    ]
