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
    var5 = models.CharField(max_length=200, editable=False)

    @property
    def property_field(self):
        return 'property field value'


# Copy of the TestModel1 to exam model with different key
class TestModel5(models.Model):
    var0 = models.AutoField(primary_key=True)
    var1 = models.CharField(max_length=200)
    var2 = models.TextField()
    var3 = models.IntegerField()
    var4 = models.ManyToManyField(TestModel0)


# Copy of the TestModel4 to exam model with different key
class TestModel6(models.Model):
    var0 = models.AutoField(primary_key=True)
    var1 = models.ForeignKey(TestModel1)
    var2 = models.CharField(max_length=200)
    var3 = models.TextField()
    var4 = models.IntegerField()