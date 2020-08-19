from django.db import models


class RegistrationModel(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    aadharno = models.IntegerField()
    vehicleno = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        db_table = "registration"


class ComplaintModel(models.Model):

    vehicleno=models.CharField(max_length=100)
    photo =models.ImageField(upload_to="pictures")
    complaintdate= models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.description

    class Meta:
        db_table = "detection"