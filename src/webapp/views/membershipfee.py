from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from webapp.models import MembershipFee


@staff_member_required
def test_list(request):
    return redirect('admin:webapp_membershipfee_changelist')


@login_required
def membershipfee_pay(request, **kwargs):
    """
      Method for mark payed member
    """

    membershipfee = get_object_or_404(MembershipFee, id=kwargs.get('pk'))
    membershipfee.is_payed = True
    membershipfee.payed_at = timezone.now()
    membershipfee.save()
    return redirect('admin:webapp_membershipfee_changelist')
