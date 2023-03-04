from django.db import models
from django.contrib.auth.models import User 
from team.models import Team

# Create your models here.
class Lead(models.Model):
    LOW = 'low'
    MEDIUM = 'medimum'
    HIGH = 'high'

    CHOICES = (
        (LOW, 'Low'),
        (MEDIUM,'Medium'),
        (HIGH, 'High')
    )

    NEW = 'new'
    CONTACTED = 'contaced'
    DONE = 'done'
    LOST = 'lost'

    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (DONE, 'Done'),
        (LOST, 'Lost'),
    )

    team = models.ForeignKey(Team, related_name='leads', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=12, choices=CHOICES, default=HIGH)
    status = models.CharField(max_length=12, choices=CHOICES_STATUS, default=NEW)
    converted_to_client = models.BooleanField(default=False)
    created_by= models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class LeadFile(models.Model):
    team = models.ForeignKey(Team, related_name='lead_files', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='leadfiles', blank=True, null=True)
    created_by= models.ForeignKey(User, related_name='lead_files_createdby', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.created_by



class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='lead_comments', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by= models.ForeignKey(User, related_name='lead_comments_createdby', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.created_by
