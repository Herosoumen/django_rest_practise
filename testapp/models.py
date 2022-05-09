from django.db import models

# Create your models here.

class Actor(models.Model):
    actor_name=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.actor_name
    
    class Meta:
        ordering = ['created_at']
    

class Movie(models.Model):
    actor=models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie_name=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie_name
    
    class Meta:
        ordering = ['created_at']