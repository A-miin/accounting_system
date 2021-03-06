import datetime

from main.celery import app
from webapp.models import Member, MembershipFee


@app.task
def create_membership_fee():
    for member in Member.objects.filter(deleted=None, membership_fee=False):
        MembershipFee.objects.create(payer=member)
    print('create_membership_fee')
