from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind
# from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# import pdb; pdb.set_trace()

#def quotation(request):
#        quotations = tblDoc.objects.all()#.filter(Pcd_tblDoc=5555)
#        return render(request, 'quotation/quotation.html', {'quotations': quotations})
def docsearch(request):
        docs = tblDoc.objects.all()
        return render(request, 'quotation/docsearch.html', {'docs':docs})
def docform(request,pk):
        doc = get_object_or_404(tblDoc,pk=pk)
        return render(request, 'quotation/doc.html', {'doc':doc})
def welcome(request):
        return render(request, 'quotation/welcome.html', {})
   
