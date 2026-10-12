
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("resumes", "0004_skill_resume_skills"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RenameField(
                    model_name="resume",
                    old_name="Skills",
                    new_name="skills",
                ),
            ],
        ),
    ]
