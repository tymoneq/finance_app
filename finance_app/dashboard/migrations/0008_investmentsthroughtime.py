# Generated by Django 5.2.3 on 2025-06-21 06:40

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_investment_category_name_delete_investmentcategory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentsThroughTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1000000.0)])),
                ('date', models.DateField()),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments_over_time', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
