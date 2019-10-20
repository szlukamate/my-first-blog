from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction, connections
from array import *
import simplejson as json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
import subprocess
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as x12
# import pdb;
# pdb.set_trace()
@login_required
def timemanager(request):
        # filtering options to Addfilter selectbox begin
        # Creates a list containing #h lists, each of #w items, all set to 0
        w, h = 3, 3;
        addfilterselectvaluesandoptions = [[0 for x in range(w)] for y in range(h)]

        addfilterselectvaluesandoptions[0][0] = 'Project Name'
        addfilterselectvaluesandoptions[0][1] = 'projectid'

        addfilterselectvaluesandoptions[1][0] = 'Listprice'
        addfilterselectvaluesandoptions[1][1] = 'listprice'

        addfilterselectvaluesandoptions[2][0] = 'Supplier'
        addfilterselectvaluesandoptions[2][1] = 'supplier'
        # filtering options to Addfilter selectbox end

        # import pdb;
        # pdb.set_trace()

        return render(request, 'quotation/timemanager.html', {'addfilterselectvaluesandoptions': addfilterselectvaluesandoptions})
@login_required
def timemanagersearchcontent(request):
    filteritemlistraw = request.POST['filteritemlist']
    filteritemlist = json.loads(filteritemlistraw)

    filteritemname = ''
    filteritemoperator = ''
    filteritemfirstinput = ''
    filteritemsecondinput = ''

    customerdescriptionphrase = ""
    listpricephrase = ""
    supplierphrase = ""

    for x in range(0,len(filteritemlist),4):

        filteritemname = filteritemlist[(x+0)]
        filteritemoperator = filteritemlist[x+1]
        filteritemfirstinput = filteritemlist[x+2]
        filteritemsecondinput = filteritemlist[x+3]

        if filteritemname == 'customerdescription':
            if filteritemoperator == 'contains':
                customerdescriptionphrase = "and customerdescription_tblProduct  LIKE '%" + filteritemfirstinput + "%' "
            if filteritemoperator == 'doesntcontain':
                customerdescriptionphrase = "and customerdescription_tblProduct NOT LIKE '%" + filteritemfirstinput + "%' "

        if filteritemname == 'listprice':
            if filteritemoperator == 'gteq':
                listpricephrase = "and purchase_price_tblproduct >= " + filteritemfirstinput + " "
            if filteritemoperator == 'lteq':
                listpricephrase = "and purchase_price_tblproduct <= " + filteritemfirstinput + " "

        if filteritemname == 'supplier':
            if filteritemoperator == 'is':
                supplierphrase = "and suppliercompanyid_tblproduct = " + filteritemfirstinput + " "

    searchphraseformainresults = (customerdescriptionphrase + listpricephrase + supplierphrase + " ")
#                                  datephraseformainresults + companyformainresults + usernameformainresults +
#                                  activitynameformainresults + quoteddocnumberformainresults + " ")
    searchphraseforrowsources = searchphraseformainresults
    cursor = connection.cursor()
    cursor.execute("SELECT timedoneid_tbltimedone, "
                   "hours_tbltimedone, "
                   "projectid_tbltimedone, "
                   "name_tblprojects_redmine_ctbltimedone "

                   "FROM quotation_tbltimedone "

                   "WHERE timedoneid_tbltimedone is not null " + searchphraseformainresults + ""
                    )
    timedones = cursor.fetchall()
    numberofitems = len(timedones)

    cursor23 = connections['redmine'].cursor()
    cursor23.execute("SELECT "
                     "projects.name "

                     "FROM time_entries as T "

                     "LEFT JOIN custom_values as quoteddocdetailsidtable "
                     "ON T.id = quoteddocdetailsidtable.customized_id and quoteddocdetailsidtable.custom_field_id = 4 "

                     "LEFT JOIN custom_values as quoteddocnumbertable "
                     "ON T.id = quoteddocnumbertable.customized_id and quoteddocnumbertable.custom_field_id = 6 "

                     "JOIN projects "
                     "ON T.project_id = projects.id "

                     "JOIN enumerations "
                     "ON T.activity_id = enumerations.id "

                     "JOIN users "
                     "ON T.user_id = users.id "

                     "WHERE T.id is not null " + searchphraseforrowsources + " "

                     "GROUP BY projects.name ")
    projectnamerowsources = cursor23.fetchall()

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT companyid_tblcompanies, companyname_tblcompanies FROM quotation_tblcompanies")
    supplierlist = cursor3.fetchall()
    transaction.commit()

    #import pdb;
    #pdb.set_trace()
#
    return render(request, 'quotation/timemanagercontent.html', {'timedones': timedones,
                                                       'projectnamerowsources': projectnamerowsources,
                                                       'numberofitems': numberofitems,
                                                       'supplierlist': supplierlist})
