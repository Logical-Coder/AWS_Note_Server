from django.db import models


class QANote(models.Model):
    QUESTION_TYPE_CHOICES = [
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
    ]

    question = models.TextField()
    answer = models.TextField(blank=True)
    question_type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPE_CHOICES,
        default='other'
    )
    attachment = models.FileField(upload_to='notes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_question_type_display()}] {self.question[:80]}"
