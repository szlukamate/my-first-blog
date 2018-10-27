from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class tblDoc(models.Model):
    Docid_tblDoc= models.AutoField(primary_key=True)
    Pcd_tblDoc= models.CharField(max_length=200)
    Town_tblDoc = models.CharField(max_length=200, default='Szeged')

    def __str__(self):
        return self.Pcd_tblDoc

class tblDoc_details(models.Model):
    Doc_detailsid_tblDoc_details= models.AutoField(primary_key=True)
    Docid_tblDoc_details= models.ForeignKey('blog.tblDoc', on_delete=models.CASCADE, related_name='tblDoc')
    Productid_tblDoc_details= models.ForeignKey('blog.tblProduct', on_delete=models.CASCADE, related_name='tblProduct')
    Qty_tblDoc_details= models.IntegerField(default=1)
#    def __str__(self):
#        return self.Product_description_tblDoc_details

class tblProduct(models.Model):
    Productid_tblProduct= models.AutoField(primary_key=True)
    Product_price_tblProduct= models.IntegerField(default=1)
    Product_description_tblProduct= models.CharField(max_length=200, default='Something')
    def __str__(self):
        return self.Product_description_tblProduct

