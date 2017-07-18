from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Bank(models.Model):
    """
    Bank Table includes all bank detail
    """
    branch_name = models.CharField(max_length=50, null=False, unique=True)
    ifsc_code = models.CharField(max_length=50, primary_key=True)
    branch_address = models.CharField(max_length=150)
    branch_contact = models.BigIntegerField(default=None)

    def __str__(self):
        return self.ifsc_code


class Account(models.Model):
    """
    Account table includes account details of each bank branch
    """
    account_no = models.BigIntegerField(primary_key=True, )
    account_holder = models.CharField(max_length=30)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20)
    pancard_no = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=150)
    contact = models.BigIntegerField(default=None)

    def __str__(self):
        return unicode(self.account_no)


transaction_choices = [('Credit', 'Credit'), ('Debit', 'Debit')]


class Transaction(models.Model):
    """
    Transaction table includes all transaction detail of particular account
    """
    transaction_id = models.BigIntegerField(primary_key=True, )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    amount = models.IntegerField(default=None)
    transaction_type = models.CharField(max_length=20, choices=transaction_choices)

    def __unicode__(self):
        return unicode(self.transaction_id)


class BranchPermissions(models.Model):
    """
    Permission Table defines sub admin's permissions to access branches
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Bank, on_delete=models.CASCADE)
