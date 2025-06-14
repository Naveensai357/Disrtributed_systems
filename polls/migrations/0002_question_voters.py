from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='voters',
            field=models.ManyToManyField(blank=True, related_name='voted_questions', to=settings.AUTH_USER_MODEL),
        ),
    ]