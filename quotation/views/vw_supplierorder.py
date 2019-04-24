from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from datetime import datetime, timedelta

# import pdb;
# pdb.set_trace()

def supplierorderpre(request):
    return render(request, 'quotation/supplierorderpre.html', {})


