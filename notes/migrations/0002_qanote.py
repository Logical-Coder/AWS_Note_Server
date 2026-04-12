# Generated migration — QANote model replacing Note
# Run on EC2: python manage.py migrate

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        # Create the new QANote model
        migrations.CreateModel(
            name='QANote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField(blank=True)),
                ('question_type', models.CharField(
                    choices=[
                        ('dsa', 'DSA'),
                        ('system_design', 'System Design'),
                        ('os', 'Operating System'),
                        ('dbms', 'DBMS'),
                        ('networking', 'Networking'),
                        ('oop', 'OOP'),
                        ('sql', 'SQL'),
                        ('javascript', 'JavaScript'),
                        ('python', 'Python'),
                        ('java', 'Java'),
                        ('react', 'React'),
                        ('behavioral', 'Behavioral'),
                        ('other', 'Other'),
                    ],
                    default='other',
                    max_length=50,
                )),
                ('attachment', models.FileField(blank=True, null=True, upload_to='notes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        # Remove old Note model
        migrations.DeleteModel(
            name='Note',
        ),
    ]
