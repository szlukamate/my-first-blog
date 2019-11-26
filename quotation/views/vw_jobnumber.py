from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required, user_passes_test
#from .forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from array import *
import simplejson as json
from django.http import HttpResponse

# import pdb;
# pdb.set_trace()
def group_required(group_name, login_url=None):
    """
    Decorator for views that checks whether a user belongs to a particular
    group, redirecting to the log-in page if necessary.
    """
    def check_group(user):
        # First check if the user belongs to the group
        if user.groups.filter(name=group_name).exists():
            return True
    return user_passes_test(check_group, login_url=login_url)

@group_required("manager")
@login_required
def jobnumberform(request, pk):
        if request.method == "POST":
                fieldvalue = request.POST['fieldvalue']
                rowid = request.POST['rowid']
                docid = request.POST['docid']
                fieldname = request.POST['fieldname']
                tbl = request.POST['tbl']

                if tbl == "tblDoc_details":
                        # not possible
                        nop
                elif tbl == "tblDoc":
                        cursor8 = connection.cursor()
                        sqlquery = "UPDATE quotation_tbldoc SET " + fieldname + "= '" + fieldvalue + "' WHERE Docid_tblDoc =" + docid
                        cursor8.execute(sqlquery)

                        cursor9 = connection.cursor()
                        cursor9.execute("SELECT " + fieldname + " "
                                                                "FROM quotation_tbldoc "
                                                                "WHERE Docid_tblDoc = %s ", [docid])
                        results = cursor9.fetchall()
                        #import pdb;
                        #pdb.set_trace()

                        json_data = json.dumps(results)

                        return HttpResponse(json_data, content_type="application/json")

        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tblDoc, "
                        "Contactid_tblDoc_id, "
                        "Doc_kindid_tblDoc_id, "
                        "companyname_tblcompanies_ctbldoc, "
                        "firstname_tblcontacts_ctbldoc, "
                        "lastname_tblcontacts_ctbldoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbldoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbldoc, "
                        "prefacespecforquotation_tbldoc, "
                        "subject_tbldoc, "
                        "docnumber_tbldoc, "
                        "creatorid_tbldoc, "
                        "creationtime_tbldoc, "
                        "title_tblcontacts_ctbldoc, "
                        "mobile_tblcontacts_ctbldoc, "
                        "email_tblcontacts_ctbldoc, "
                        "pcd_tblcompanies_ctbldoc, "
                        "town_tblcompanies_ctbldoc, "
                        "address_tblcompanies_ctbldoc, "
                        "total_tbldoc, "
                        "deliverydays_tbldoc, "
                        "paymenttextforquotation_tblpayment_ctbldoc, "
                        "currencycodeinreport_tbldoc, "
                        "currencyrateinreport_tbldoc, "
                        "pretag_tbldockind "
                        "FROM quotation_tbldoc "
                        "JOIN quotation_tbldoc_kind "
                        "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                        "WHERE docid_tbldoc=%s ",
                        [pk])

        doc = cursor1.fetchall()
        for x in doc:
                creatorid = x[11]

        cursor10 = connection.cursor()
        cursor10.execute("SELECT id, "
                         "first_name, "
                         "last_name, "
                         "email, "
                         "subscriptiontext_tblauth_user "
                         "FROM auth_user "
                         "WHERE id=%s ", [creatorid])
        creatordata = cursor10.fetchall()

        return render(request, 'quotation/jobnumber.html', {'doc': doc,
                                                            'creatordata': creatordata})
