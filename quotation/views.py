from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# import pdb; pdb.set_trace()
from .forms import quotationroweditForm
from collections import namedtuple


def docsearch(request):
        docs = tblDoc.objects.all()
        return render(request, 'quotation/docsearch.html', {'docs':docs})
def docform(request,pk):
        doc = get_object_or_404(tblDoc,pk=pk)
        docdetails = tblDoc_details.objects.filter(Docid_tblDoc_details=pk).order_by('firstnum_tblDoc_details','secondnum_tblDoc_details','thirdnum_tblDoc_details','fourthnum_tblDoc_details')

        return render(request, 'quotation/doc.html', {'doc':doc, 'docdetails':docdetails})
def welcome(request):
        return render(request, 'quotation/welcome.html', {})
def quotationrowedit(request, pk):
    quotationrow = get_object_or_404(tblDoc_details, pk=pk)
    if request.method == "POST":
        form = quotationroweditForm(request.POST, instance=quotationrow)
        if form.is_valid():
            quotationrow.save()

            from django.db import connection, transaction
            cursor = connection.cursor()

            cursor.execute("SELECT Docid_tblDoc_details_id FROM quotation_tbldoc_details WHERE Doc_detailsid_tblDoc_details=%s ", [pk])
            #import pdb;
            #pdb.set_trace()
            results = cursor.fetchall()

            for x in results:
                na=x[0]

            transaction.commit()

            return redirect('docform', pk=na)

    else:
        form = quotationroweditForm(instance=quotationrow)
    return render(request, 'quotation/quotationrowedit.html', {'form': form})
def quotationnewrow(request, pk):

                from django.db import connection, transaction

                cursor1 = connection.cursor()
                cursor1.execute("INSERT INTO quotation_tbldoc_details (Docid_tblDoc_details_id, Productid_tblDoc_details_id,Qty_tblDoc_details,firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details,Note_tblDoc_details) VALUES (%s, 1,1, 1,0,0,0,'Defaultnote')",[pk])
                #db.connections.close_all()
                transaction.commit()

                return redirect('docform', pk=pk)
def quotationrowremove(request, pk):
    from django.db import connection, transaction

    cursor2 = connection.cursor()
    cursor2.execute(
        "SELECT Docid_tblDoc_details_id FROM quotation_tbldoc_details WHERE Doc_detailsid_tblDoc_details=%s ", [pk])
    results = cursor2.fetchall()
    for x in results:
        na = x[0]
    transaction.commit()
    # db.connections.close_all()

    cursor1 = connection.cursor()
    cursor1.execute(
        "DELETE FROM quotation_tbldoc_details WHERE Doc_detailsid_tblDoc_details=%s ", [pk])
    # db.connections.close_all()
    transaction.commit()

    return redirect('docform', pk=na)