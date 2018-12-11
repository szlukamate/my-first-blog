from django.db import models
from django.utils import timezone


class tblDoc(models.Model):
    Docid_tblDoc= models.AutoField(primary_key=True)
    Pcd_tblDoc= models.CharField(max_length=201)
    Town_tblDoc = models.CharField(max_length=200, default='Szeged')
    Doc_kindid_tblDoc = models.ForeignKey('quotation.tblDoc_kind', on_delete=models.CASCADE, related_name='tblDoc_kin',default=1)
    Contactid_tblDoc = models.ForeignKey('quotation.tblContacts', on_delete=models.CASCADE, related_name='tblDoc_kinx',default=1)
    def __str__(self):
        return self.Town_tblDoc

class tblDoc_details(models.Model):
    Doc_detailsid_tblDoc_details= models.AutoField(primary_key=True)
    Docid_tblDoc_details= models.ForeignKey('quotation.tblDoc', on_delete=models.CASCADE, related_name='tblDoc')
    Productid_tblDoc_details= models.ForeignKey('quotation.tblProduct', on_delete=models.CASCADE, related_name='tblProduct',default=1)
    Qty_tblDoc_details= models.IntegerField(default=1)
    firstnum_tblDoc_details= models.IntegerField(default=1)
    secondnum_tblDoc_details= models.IntegerField(default=0)
    thirdnum_tblDoc_details= models.IntegerField(default=0)
    fourthnum_tblDoc_details= models.IntegerField(default=0)
    Note_tblDoc_details = models.CharField(max_length=200, default='Defaultnote')
    creationtime_tblDoc_details = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.Note_tblDoc_details

class tblProduct(models.Model):
    Productid_tblProduct= models.AutoField(primary_key=True)
    Product_price_tblProduct= models.IntegerField(default=1)
    Product_description_tblProduct= models.CharField(max_length=200, default='Something')
    def __str__(self):
        return self.Product_description_tblProduct

class tblDoc_kind(models.Model):
    Doc_kindid_tblDoc_kind= models.AutoField(primary_key=True)
    Doc_kind_name_tblDoc_kind= models.CharField(max_length=200)
    def __str__(self):
        return self.Doc_kind_name_tblDoc_kind
class tblContacts(models.Model):
    Contactid_tblContacts= models.AutoField(primary_key=True)
    Companyid_tblContacts= models.ForeignKey('quotation.tblCompanies', on_delete=models.CASCADE, related_name='tbl',default=1)
    firstname_tblcontacts= models.CharField(max_length=200,default='s')
    lastname_tblcontacts= models.CharField(max_length=200,default='s')
    def __str__(self):
        return self.firstname_tblcontacts
class tblCompanies(models.Model):
    Companyid_tblCompanies= models.AutoField(primary_key=True)
    companyname_tblcompanies= models.CharField(max_length=200,default='ss')
    def __str__(self):
        return self.companyname_tblcompanies