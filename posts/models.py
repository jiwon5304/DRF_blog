from django.db  import models
from conf.models import BaseModel, SoftDeleteModel

class Post(BaseModel, SoftDeleteModel, models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    contents = models.TextField()
    
    class Meta:
        db_table = 'post'