import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_atestados_numero_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atestados',
            name='data_emissao',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
