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
def filtertemplatehtmlonproductform(request):
        invokedfrom = request.POST['invokedfrom']

        if invokedfrom == 'filteritemselectchanged': # when we want change a filteritems on html (clicking the selectbox on filteritem)
                filteritemselectedvalue = request.POST['filteritemselectedvalue']
                filteritemname = request.POST['filteritemname']
                filteritemrowid = request.POST['filteritemrowid']

                if filteritemname == 'customerdescription':
                        if filteritemselectedvalue == 'contains':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'doesntcontain':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'none':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'any':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                if filteritemname == 'listprice':
                        if filteritemselectedvalue == 'is':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'gteq':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'lteq':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'between':

                                return render(request, 'quotation/filteritemtemplatebetweeninputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'none':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'any':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                if filteritemname == 'currency':
                        cursor3 = connection.cursor()
                        cursor3.execute(
                            "SELECT currencyid_tblcurrency, currencyisocode_tblcurrency FROM quotation_tblcurrency")
                        currencycodes = cursor3.fetchall()

                        if filteritemselectedvalue == 'is':

                                return render(request, 'quotation/filteritemtemplateselect.html', {'filteritemfirstinputboxselectoptions': currencycodes,
                                                                                                   'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'isnot':

                                return render(request, 'quotation/filteritemtemplateselect.html', {'filteritemfirstinputboxselectoptions': currencycodes,
                                                                                                   'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'none':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'any':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

        if invokedfrom == 'addfilterselectchanged': # when we want to search first click the #Add Filter selectbox and add some filteritems to html
                filteritemrowid = request.POST['filteritemmaxrowid']
                selectedvalue = request.POST['selectedvalue']
                selectedoption = request.POST['selectedoption'] # name which appears for user


                if selectedvalue == 'customerdescription': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 4;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'customerdescription' #attribute for elements

                    filteritemselectoptions[0][0] = 'contains'
                    filteritemselectoptions[0][1] = 'contains'

                    filteritemselectoptions[1][0] = 'doesntcontain'
                    filteritemselectoptions[1][1] = "doesn't contain"

                    filteritemselectoptions[2][0] = 'none'
                    filteritemselectoptions[2][1] = 'none'

                    filteritemselectoptions[3][0] = 'any'
                    filteritemselectoptions[3][1] = 'any'

                if selectedvalue == 'listprice':

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 6;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'listprice' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                    filteritemselectoptions[1][0] = 'gteq'
                    filteritemselectoptions[1][1] = '>='

                    filteritemselectoptions[2][0] = 'lteq'
                    filteritemselectoptions[2][1] = '<='

                    filteritemselectoptions[3][0] = 'between'
                    filteritemselectoptions[3][1] = 'between'

                    filteritemselectoptions[4][0] = 'none'
                    filteritemselectoptions[4][1] = 'none'

                    filteritemselectoptions[5][0] = 'any'
                    filteritemselectoptions[5][1] = 'any'

                if selectedvalue == 'currency': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 4;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'currency' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                    filteritemselectoptions[1][0] = 'isnot'
                    filteritemselectoptions[1][1] = "is not"

                    filteritemselectoptions[2][0] = 'none'
                    filteritemselectoptions[2][1] = 'none'

                    filteritemselectoptions[3][0] = 'any'
                    filteritemselectoptions[3][1] = 'any'

        return render(request, 'quotation/filtertemplatehtml.html',{'selectedoption': selectedoption,
                                                                    'filteritemrowid': filteritemrowid,
                                                                    'filteritemname': filteritemname,
                                                                    'filteritemselectoptions': filteritemselectoptions})
