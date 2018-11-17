from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from .forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
# import pdb;
# pdb.set_trace()

def welcome(request):
        return render(request, 'quotation/welcome.html', {})

def docsearch(request):
        docs = tblDoc.objects.all()
        return render(request, 'quotation/docsearch.html', {'docs': docs})


def docadd(request):

    cursor = connection.cursor()
    cursor.execute("SELECT doc_kind_name_tbldoc_kind FROM quotation_tbldoc_kind")
    # db.connections.close_all()
    dockinds = cursor.fetchall()
    transaction.commit()
    #import pdb;
    #pdb.set_trace()
    #return redirect('quotationform', pk=pk)
    return render(request, 'quotation/docadd.html', {'dockinds': dockinds})

def docselector(request, pk):

        cursor = connection.cursor()
        cursor.execute("SELECT  quotation_tbldoc_kind.Doc_kindid_tbldoc_kind "
                       "FROM quotation_tbldoc "
                       "JOIN quotation_tbldoc_kind "
                       "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                       "WHERE quotation_tbldoc.docid_tbldoc=%s ", [pk])
        results = cursor.fetchall()
        for x in results:
            dockind = x[0]
        transaction.commit()

        if dockind==1: #Quotation
            return redirect('quotationform', pk=dockind)
        elif dockind==2: #Order
            return redirect('orderform', pk=dockind)

def quotationform(request,pk):
        doc = get_object_or_404(tblDoc,pk=pk)
        docdetails = tblDoc_details.objects.filter(Docid_tblDoc_details=pk).order_by('firstnum_tblDoc_details','secondnum_tblDoc_details','thirdnum_tblDoc_details','fourthnum_tblDoc_details')

        return render(request, 'quotation/quotation.html', {'doc':doc, 'docdetails':docdetails})

def quotationrowedit(request, pk):
        quotationrow = get_object_or_404(tblDoc_details, pk=pk)
        if request.method == "POST":
            form = quotationroweditForm(request.POST, instance=quotationrow)
            if form.is_valid():
                quotationrow.save()

                cursor = connection.cursor()

                cursor.execute("SELECT Docid_tblDoc_details_id FROM quotation_tbldoc_details WHERE Doc_detailsid_tblDoc_details=%s ", [pk])
                results = cursor.fetchall()

                for x in results:
                    na=x[0]

                transaction.commit()

                return redirect('quotationform', pk=na)

        else:
            form = quotationroweditForm(instance=quotationrow)
        return render(request, 'quotation/quotationrowedit.html', {'form': form})
def quotationnewrow(request, pk):
        cursor1 = connection.cursor()
        cursor1.execute("INSERT INTO quotation_tbldoc_details (Docid_tblDoc_details_id, Productid_tblDoc_details_id,Qty_tblDoc_details,firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details,Note_tblDoc_details) VALUES (%s, 1,1, 1,0,0,0,'Defaultnote')",[pk])
        #db.connections.close_all()
        transaction.commit()

        return redirect('quotationform', pk=pk)
def quotationrowremove(request, pk):

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

        return redirect('quotationform', pk=na)