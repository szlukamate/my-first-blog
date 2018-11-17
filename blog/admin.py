from django.contrib import admin
from .models import Post, Comment

from quotation.models import tblDoc, tblDoc_kind, tblDoc_details, tblProduct, tblCompanies, tblContacts




admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(tblDoc)
admin.site.register(tblDoc_kind)

admin.site.register(tblDoc_details)
admin.site.register(tblProduct)
admin.site.register(tblContacts)
admin.site.register(tblCompanies)
