# Generated by Django 4.0.2 on 2022-02-19 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredient_measurement_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='is_favorited',
            field=models.BooleanField(default=False, verbose_name='В избранном'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_in_shopping_cart',
            field=models.BooleanField(default=False, verbose_name='В списке покупок'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.FloatField(null=True, verbose_name='Количество'),
        ),
    ]
