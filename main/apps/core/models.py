from uuid_extensions import uuid7
from django.db.models import UUIDField, Model


def uuid():
    return uuid7()

class UUID_Model(Model):
    """ Base model with UUID primary key. """ 
    id = UUIDField(primary_key=True, default=uuid, editable=False)

    class Meta:
        abstract = True
