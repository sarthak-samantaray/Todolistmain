from django.db import models

# This will take care of the user's information like , username, password. It handle the authetication.
from django.contrib.auth.models import User


# MODELS
class Task(models.Model):

    # This is many to one relationship, user is an object of User class imported
    # It makes a table of user with name, email and password.
    # on_delete , The table of that user will be erased if the user is erased.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField(null=True,blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


    # Any complete task must be sent to the bottom  of the list. 
    class Meta:
        ordering = ['complete']
