from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
#from .forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from array import *
import simplejson as json
from django.http import HttpResponse

# import pdb;
# pdb.set_trace()
@login_required
def accountentryform(request, pk):
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
                        "pretag_tbldockind, "
                        "debitaccountid_tbldoc, "
                        "creditaccountid_tbldoc, "
                        "accountvalue_tbldoc, "
                        "accountduedate_tbldoc "
                        "FROM quotation_tbldoc "
                        "JOIN quotation_tbldoc_kind "
                        "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                        "WHERE docid_tbldoc=%s ",
                        [pk])

        doc = cursor1.fetchall()
        for x in doc:
                creatorid = x[11]
                debitaccountid = x[25]
                creditaccountid = x[26]

        cursor10 = connection.cursor()
        cursor10.execute("SELECT id, "
                         "first_name, "
                         "last_name, "
                         "email, "
                         "subscriptiontext_tblauth_user "
                         "FROM auth_user "
                         "WHERE id=%s ", [creatorid])
        creatordata = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT accountid_tblchartofaccounts, "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts")
        chartofaccounts = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts "
                         "WHERE accountid_tblchartofaccounts=%s",
                         [debitaccountid])
        debitaccountname = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts "
                         "WHERE accountid_tblchartofaccounts=%s",
                         [creditaccountid])
        creditaccountname = cursor10.fetchall()


        return render(request, 'quotation/accountentry.html', {'doc': doc,
                                                        'chartofaccounts': chartofaccounts,
                                                        'debitaccountname': debitaccountname,
                                                        'creditaccountname': creditaccountname,
                                                        'creatordata': creatordata})
@login_required
def accountentryuniversalselections (request):

    fieldvalue = request.POST['fieldvalue']
    docid = request.POST['entrydocid']
    fieldnameto = request.POST['fieldnameto'] # i.e. defaultprefaceidforquotation_tblcompanies

    cursor22 = connection.cursor()
    cursor22.callproc("spentryuniversalselections",[fieldnameto,fieldvalue,docid])
    results23 = cursor22.fetchall()
    print(results23)

    json_data = json.dumps(results23)

    return HttpResponse(json_data, content_type="application/json")
@login_required
def accountincomestatement (request):
    def accountsum(accountnumberinitial):
        cursor22 = connection.cursor()
        cursor22.execute("SELECT "
                         "sum(accountvalue_tbldoc) "
                         "FROM quotation_tbldoc "
                         "WHERE `Doc_kindid_tblDoc_id`=6 and obsolete_tbldoc=0 and debitaccountid_tbldoc LIKE '" + accountnumberinitial + "%'")
        results23 = cursor22.fetchall()
        for x in results23:
            sum = x[0]
     #       import pdb;
     #       pdb.set_trace()

        return sum


    #Income Statement preparetion

    cursor22 = connection.cursor()
    cursor22.execute("SELECT "
                     "rowid_tblincomestatement, "
                     "order_tblincomestatement, "
                     "rowname_tblincomestatement "
                     "FROM quotation_tblincomestatement ")

    incomestatementrows = cursor22.fetchall()
    incomestatementrowslist = []
    incomestatementrowslen = len(incomestatementrows)

    for i in range(incomestatementrowslen):
        cursor32 = connection.cursor()
        cursor32.execute("SELECT "
                         "rowid_tblincomestatementdetails, "
                         "operationsign_tblincomestatementdetails, "
                         "operationkind_tblincomestatementdetails, "
                         "side_tblincomestatementdetails, "
                         "generalledgeraccount_tblincomestatementdetails "
                         "FROM quotation_tblincomestatementdetails "
                         "WHERE incomestatementrowid_tblincomestatementdetails=%s ", [incomestatementrows[i][0]])

        incomestatementdetailsrows = cursor32.fetchall()
        incomestatementdetailsrowslen = len(incomestatementdetailsrows)

        firstfield = incomestatementrows[i][0]
        secondfield = incomestatementrows[i][1]
        thirdfield = incomestatementrows[i][2]
        fourthfieldappendable = ''
        fifthfieldappendable = 0.0
        for j in range(incomestatementdetailsrowslen):

            if incomestatementdetailsrows[j][1] == '+':
                    operationsigntoform='+'
                    fifthfieldappendable = fifthfieldappendable + accountsum(incomestatementdetailsrows[j][4])

            elif incomestatementdetailsrows[j][1] == '-':
                operationsigntoform = '-'
            if incomestatementdetailsrows[j][2] == 'Account':
                operationkindtoform = 'GL'
            elif incomestatementdetailsrows[j][2] == 'Row':
                operationkindtoform = 'ISROW'
            if incomestatementdetailsrows[j][3] == 'Debit':
                sidetoform = 'DB'
            elif incomestatementdetailsrows[j][3] == 'Credit':
                sidetoform = 'CB'
            generalledgeraccounttoform = incomestatementdetailsrows[j][4]
            fourthfieldappendable = fourthfieldappendable + "(" + operationsigntoform + operationkindtoform + sidetoform + generalledgeraccounttoform + ")"
        fifthfield = fifthfieldappendable
        fourthfield = fourthfieldappendable
        appendvar = (firstfield, secondfield, thirdfield, fourthfield, fifthfield)
        incomestatementrowslist.append(appendvar)
    incomestatementrows2 = tuple (incomestatementrowslist)


    return render(request, 'quotation/accountincomestatement.html', {'incomestatementrows2': incomestatementrows2})
