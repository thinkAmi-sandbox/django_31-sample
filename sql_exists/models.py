from django.db import models


class Color(models.Model):
    name = models.CharField('名前', max_length=20)


class Apple(models.Model):
    name = models.CharField('名前', max_length=20)
    color = models.ForeignKey('Color', on_delete=models.PROTECT)
