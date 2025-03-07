from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100) # Plain text password is stored here

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # for a secure implementation, use django's built in User model
    # user = models.OneToOneField(User, on_delete=models.CASCADE
    bio = models.TextField(default='No bio')
    def __str__(self):
        return self.user.username
    
