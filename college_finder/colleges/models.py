from django.db import models
from sign_in.models import User

class College(models.Model):
    name = models.CharField(max_length=200)
    average_cost = models.IntegerField()
    location = models.CharField(max_length=70)
    website = models.CharField(max_length=1000)
    image = models.ImageField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

	
class Apply(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.college.name} on {self.application_date}"