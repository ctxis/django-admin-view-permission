from __future__ import unicode_literals

from django.db import models


class TestModel0(models.Model):
    var1 = models.CharField(max_length=200)
    var2 = models.TextField()
    var3 = models.IntegerField()


class TestModel1(models.Model):
    var1 = models.CharField(max_length=200)
    var2 = models.TextField()
    var3 = models.IntegerField()
    var4 = models.ManyToManyField(TestModel0)


class TestModel2(models.Model):
    var1 = models.ForeignKey(TestModel1)
    var2 = models.CharField(max_length=200)
    var3 = models.TextField()
    var4 = models.IntegerField


class TestModel3(models.Model):
    var1 = models.ForeignKey(TestModel1)
    var2 = models.CharField(max_length=200)
    var3 = models.TextField()
    var4 = models.IntegerField()


class TestModel4(models.Model):
    var1 = models.ForeignKey(TestModel1)
    var2 = models.CharField(max_length=200)
    var3 = models.TextField()
    var4 = models.IntegerField()
