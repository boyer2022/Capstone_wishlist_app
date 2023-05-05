from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Place(models.Model) :
    # Specify what happens if user is deleted-CASCADE means everything is deleted
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE) 
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def _str_(self):
        photo_str = self.photo.url if self.photo else 'no_photo'
        notes_str = self.notes[100:] if self.notes else 'no_notes'
        return f'{self.pk}: {self.name} visited? {self.visited} on {self.date_visited}. Notes: {notes_str}. Photo {photo_str}'
