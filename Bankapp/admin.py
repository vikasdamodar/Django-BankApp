from django.contrib import admin

from Bankapp.models import *

admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(Transaction)
admin.site.register(BranchPermissions)
