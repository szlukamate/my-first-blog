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
def filtermain(request):

        filterfield = []

        # fieldname, visibility

        fieldproperties = ('customerdescription',1)
        filterfield.append(fieldproperties)

        fieldproperties = ('listprice',1)
        filterfield.append(fieldproperties)

        fieldproperties = ('currency',1)
        filterfield.append(fieldproperties)



        json_data = json.dumps(filterfield[1][0])

        return HttpResponse(json_data, content_type="application/json")
def filtertemplatehtmlonproductform(request):
        invokedfrom = request.POST['invokedfrom']

        if invokedfrom == 'filteritemselectchanged': # when we want change a filteritems on html (clicking the selectbox on filteritem)
                filteritemselectedvalue = request.POST['filteritemselectedvalue'] # here the value is number
                filteritemname = request.POST['filteritemname']
                filteritemrowid = request.POST['filteritemrowid']

                if filteritemname == 'customerdescription':
                        if int(filteritemselectedvalue) == 1: # 1 means 'contains'

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {})

                        if int(filteritemselectedvalue) == 2: # 2 means 'does not contain'

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {})

                        if int(filteritemselectedvalue) == 3: # 3 means 'none'

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if int(filteritemselectedvalue) == 4: # 4 means 'any'

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                if filteritemname == 'listprice':
                        if int(filteritemselectedvalue) == 1: # 1 means 'is'

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {})

                        if int(filteritemselectedvalue) == 2: # 2 means '>='

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {})

                        if int(filteritemselectedvalue) == 3: # 3 means '<='

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {})

                        if int(filteritemselectedvalue) == 4: # 4 means 'between'

                                return render(request, 'quotation/filteritemtemplatebetweeninputbox.html', {})

                        if int(filteritemselectedvalue) == 5: # 5 means 'none'

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if int(filteritemselectedvalue) == 6: # 6 means 'any'

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

        if invokedfrom == 'addfilterselectchanged': # when we want to search first click the #Add Filter selectbox and add some filteritems to html
                filteritemrowid = request.POST['filteritemmaxrowid']
                selectedvalue = request.POST['selectedvalue']
                selectedoption = request.POST['selectedoption']


                if selectedvalue == 'customerdescription': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 4;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'customerdescription'

                    filteritemselectoptions[0][0] = 1
                    filteritemselectoptions[0][1] = 'contains'

                    filteritemselectoptions[1][0] = 2
                    filteritemselectoptions[1][1] = "doesn't contain"

                    filteritemselectoptions[2][0] = 3
                    filteritemselectoptions[2][1] = 'none'

                    filteritemselectoptions[3][0] = 4
                    filteritemselectoptions[3][1] = 'any'

                if selectedvalue == 'listprice':

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 6;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'listprice'

                    filteritemselectoptions[0][0] = 1
                    filteritemselectoptions[0][1] = 'is'

                    filteritemselectoptions[1][0] = 2
                    filteritemselectoptions[1][1] = '>='

                    filteritemselectoptions[2][0] = 3
                    filteritemselectoptions[2][1] = '<='

                    filteritemselectoptions[3][0] = 4
                    filteritemselectoptions[3][1] = 'between'

                    filteritemselectoptions[4][0] = 5
                    filteritemselectoptions[4][1] = 'none'

                    filteritemselectoptions[5][0] = 6
                    filteritemselectoptions[5][1] = 'any'

        return render(request, 'quotation/filtertemplatehtml.html',{'selectedoption': selectedoption,
                                                                    'filteritemrowid': filteritemrowid,
                                                                    'filteritemname': filteritemname,
                                                                    'filteritemselectoptions': filteritemselectoptions})
