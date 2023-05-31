from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class Image(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000, default='')
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created_on = models.DateField(auto_now_add=True)
    users_like = models.ManyToManyField(get_user_model(), related_name='image_like', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['-created_on']),
            models.Index(fields=['-total_likes']),
        ]
        ordering = ['-created_on']
        
    def __str__(self) -> str:
        return self.title
    
    # Override the save method to automatically generate the slug for the image based on title field
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("images:detail", args=[self.id, self.slug])
    