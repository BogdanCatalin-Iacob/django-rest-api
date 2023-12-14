from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    '''
    Follower model
    \'owner\' is a User following another User
    \'followed\' is a User followed by another User
    \'related_name\' attribute is needed for django to differentiate
    between \'owner\' and \'followed\' who are both User model instances
    '''
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(
        User, related_name='followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

        def __str__(self):
            return f'{self.owner} {self.followed}'
