import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def copy_old_users(apps, schema_editor):
    OldUser = apps.get_model('balenciaga_app', 'User')
    AuthUser = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])
    Profile = apps.get_model('balenciaga_app', 'Profile')
    for old in OldUser.objects.all():
        if AuthUser.objects.filter(username=old.nickname).exists():
            continue
        new = AuthUser.objects.create(
            username=old.nickname,
            email=old.email,
            password='!', 
        )
        Profile.objects.create(user=new, telephone=old.telephone)


class Migration(migrations.Migration):

    dependencies = [
        ("balenciaga_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telephone", models.CharField(blank=True, max_length=50)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль",
                "verbose_name_plural": "Профили",
            },
        ),
        migrations.RunPython(copy_old_users, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="commission",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
