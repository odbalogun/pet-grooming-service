from django.db import models


class BaseModel(models.Model):
    """
    Base model. Other models will inherit from this
    """
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)
    is_active = models.BooleanField('active', default=True)
    delete_status = models.BooleanField('deleted', default=False)

    class Meta:
        abstract = True
