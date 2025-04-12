from django.db import migrations

def disable_constraint(apps, schema_editor):
    schema_editor.execute("""
        ALTER TABLE accounts_unite 
        DISABLE CONSTRAINT DJANGO_AD_USER_ID_C564EBA6_F
    """)

def enable_constraint(apps, schema_editor):
    schema_editor.execute("""
        ALTER TABLE accounts_unite 
        ENABLE CONSTRAINT DJANGO_AD_USER_ID_C564EBA6_F
    """)

class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('accounts', '0003_unite_created_by'), 
    ]
    
    operations = [
        migrations.RunPython(disable_constraint, enable_constraint),
    ]