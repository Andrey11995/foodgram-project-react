# Generated by Django 4.0.2 on 2022-02-27 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_subscriptions_subscriptions_unique_subscription'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscriptions',
            new_name='Subscription',
        ),
    ]