from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
# import pdb;
# pdb.set_trace()

def orderform(request,pk):
    if request.method == "POST":
        firstnum_tblDoc_details = request.POST['firstnum_tblDoc_details']
        Doc_detailsid_tblDoc_details = request.POST['Doc_detailsid_tblDoc_details']
        cursor2 = connection.cursor()
        cursor2.execute(
            "UPDATE quotation_tbldoc_details "
            "SET firstnum_tblDoc_details = %s "
            "WHERE  Doc_detailsid_tblDoc_details = %s", [firstnum_tblDoc_details, Doc_detailsid_tblDoc_details])
        # import pdb;
        # pdb.set_trace()

    doc = get_object_or_404(tblDoc, pk=pk)
    cursor3 = connection.cursor()
    cursor3.execute("SELECT  * "
                    "FROM quotation_tbldoc_details "
                    "WHERE docid_tbldoc_details_id=%s "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [pk])

    docdetails = cursor3.fetchall()

    return render(request, 'quotation/order.html', {'doc': doc, 'docdetails': docdetails})
