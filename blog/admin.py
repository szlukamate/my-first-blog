from django.contrib import admin
from .models import Post, Comment
#, tblDoc, tblDoc_details, tblProduct

from quotation.models import tblDoc
#class a(admin.TabularInline):
#    model = tblDoc_details


#class DocAdmin(admin.ModelAdmin):
#    readonly_fields = ('Docid_tblDoc',)
#    fields = ('Docid_tblDoc', 'Pcd_tblDoc', 'Town_tblDoc')
#    list_display = ('Docid_tblDoc','Pcd_tblDoc', 'Town_tblDoc')
#    inlines = [a]


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(tblDoc)
#admin.site.register(tblDoc_details)
#admin.site.register(tblProduct)
