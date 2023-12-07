from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PersonalInfo(models.Model):
    first_name = models.CharField(max_length = 40, null= False, blank=False)
    last_name = models.CharField(max_length = 40, null= False, blank=False)
    avatar = models.URLField()
    title = models.CharField(max_length = 40, blank=False)
    description = models.TextField(null = True)
    linkedin_url = models.URLField(null = True)
    github_url = models.URLField(null = True)
    personal_url = models.URLField(null = True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def create(self, validated_data, username = None):
        user_id = User.objects.get(username = username)
        
        pi = PersonalInfo()
        pi.first_name = validated_data['first_name']
        pi.last_name = validated_data['last_name']
        pi.avatar = validated_data['avatar']
        pi.title = validated_data['title']
        pi.description = validated_data['description']
        pi.linkedin_url = validated_data['linkedin_url']
        pi.github_url = validated_data['github_url']
        pi.personal_url = validated_data['personal_url']
        pi.users = user_id
        
        pi.save()
        
        return pi
        
    class Meta:
        unique_together = ('users',)