from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='capacity',
            field=models.PositiveSmallIntegerField(default=2),
        ),
    ]