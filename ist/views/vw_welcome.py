from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ist.models import tblIssue
from django.contrib.auth.decorators import login_required
#from .forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
# import pdb;
# pdb.set_trace()

def welcome(request):
        return render(request, 'ist/welcome.html', {})
