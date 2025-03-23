from tortoise import fields
from tortoise.models import Model


class FileDB(Model):
    id = fields.IntField(pk=True)
    filename = fields.CharField(min_length=3, max_length=100)
    path = fields.CharField(min_length=3, max_length=200)
    owner = fields.IntField()
    desc = fields.CharField(min_length=3, max_length=400)
    number_of_pages = fields.IntField()
