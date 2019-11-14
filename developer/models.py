from django.db import models
from django.utils import timezone


class tbltest(models.Model):
    Companyid_tblCompanies= models.AutoField(primary_key=True)
    companyname_tblcompanies= models.CharField(max_length=200,default='ss')
    def __str__(self):
        return self.companyname_tblcompanies