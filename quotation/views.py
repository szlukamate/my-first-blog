from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# import pdb; pdb.set_trace()
from .forms import quotationroweditForm

def docsearch(request):
        docs = tblDoc.objects.all()
        return render(request, 'quotation/docsearch.html', {'docs':docs})
def docform(request,pk):
        doc = get_object_or_404(tblDoc,pk=pk)
        docdetails = tblDoc_details.objects.filter(Docid_tblDoc_details=pk).order_by('firstnum_tblDoc_details','secondnum_tblDoc_details')

        return render(request, 'quotation/doc.html', {'doc':doc, 'docdetails':docdetails})
def welcome(request):
        return render(request, 'quotation/welcome.html', {})
def quotationrowedit(request, pk):
    quotationrow = get_object_or_404(tblDoc_details, pk=pk)
    if request.method == "POST":
        form = quotationroweditForm(request.POST, instance=quotationrow)
        if form.is_valid():
            #post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            quotationrow.save()
            #return redirect('docform', pk=tblDoc_details.objects.filter(Doc_detailsid_tblDoc_details=pk)
    else:
        form = quotationroweditForm(instance=quotationrow)
    return render(request, 'quotation/quotationrowedit.html', {'form': form})
