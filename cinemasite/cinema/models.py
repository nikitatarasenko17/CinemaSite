from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db import models

class MyUser(AbstractUser):
    spent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
    
class Hall(models.Model):
    name = models.CharField(max_length=50, unique=True)
    size = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Halls"

    def __str__(self):
        return f'Hall {self.name} of size {self.size}'  

class Movies(models.Model):
    title = models.CharField(max_length=50)
    duration = models.PositiveSmallIntegerField(blank=True, null=True)
    release_year = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Movies"

    def __str__(self):
        return f'{self.title}'   


class Sessions(models.Model):
    movie_title = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='movie_title')
    hall_name = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='hall_name')
    start_session_time = models.TimeField(blank=True, null=True)
    end_session_time = models.TimeField(blank=True, null=True)
    date_start_show = models.DateTimeField(blank=True, null=True)
    date_end_show = models.DateTimeField(blank=True, null=True)
    free_seats = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Sessions"
    
    def check_status(self):
        if self.start_session_time <datetime.now().time() < self.end_session_time:
            self.is_active = False
        return self.is_active    

    def save(self, *args, **kwargs):
        self.check_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Session {self.movie_title} in the hall {self.hall_name}'  

class Purchase(models.Model):
    сonsumer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='consumer_purchase', blank=True)
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE, related_name='purchase_session', blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Purchases"

    def __str__(self):
        return f'Consumer {self.сonsumer} buy {self.quantity} ticket\'s for {self.session}' 
