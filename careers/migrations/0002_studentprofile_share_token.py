import uuid
from django.db import migrations, models


def populate_share_tokens(apps, schema_editor):
    """Give every existing profile its own unique UUID."""
    StudentProfile = apps.get_model('careers', 'StudentProfile')
    for profile in StudentProfile.objects.all():
        profile.share_token = uuid.uuid4()
        profile.save(update_fields=['share_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0001_initial'),
    ]

    operations = [
        # Step 1 — add the column with a placeholder default, NOT unique yet
        migrations.AddField(
            model_name='studentprofile',
            name='share_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),

        # Step 2 — fill every existing row with its own unique UUID
        migrations.RunPython(populate_share_tokens, migrations.RunPython.noop),

        # Step 3 — now it's safe to add the unique constraint
        migrations.AlterField(
            model_name='studentprofile',
            name='share_token',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
    ]
