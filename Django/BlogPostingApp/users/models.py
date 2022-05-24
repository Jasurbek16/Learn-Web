from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    # gets run after our model is saved
    def save(self, *args, **kwargs):
        # ^ When you are overriding model's save method 
        # in Django, you should also pass *args 
        # and **kwargs to overridden method
        
        # running the save method of our parent class
        super().save(*args, **kwargs)
        # would have been run when we save the profile instance anyways
        img = Image.open(self.image.path)
        # ^ would open the image of the current instance
        # Resizing
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) # <- overwrites the exising image

    