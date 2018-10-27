from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from quotation.models import tblDoc
# from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# import pdb; pdb.set_trace()

def quotation(request):
        quotations = tblDoc.objects.all()#.filter(Pcd_tblDoc=5555)
        return render(request, 'quotation/quotation.html', {'quotations': quotations})
