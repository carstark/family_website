# Generated by Django 4.2.4 on 2023-11-28 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0008_alter_blog_title_vote"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vote",
            old_name="hunter",
            new_name="author",
        ),
    ]
