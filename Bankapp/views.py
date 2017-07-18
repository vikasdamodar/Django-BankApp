from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Bankapp.form import *


def login_user(request):
    """
    authenticates admin and users to dashboard page
    """
    if request.user.is_authenticated():
        return redirect('admin')

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            invalid = "Invalid Username / Password"
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin')
    else:
        login_form = LoginForm()
        username = request.user.get_username()

    return render(request, "login.html", locals())


def logout_user(request):
    logout(request)
    return render(request, "logout.html")


@login_required(login_url='/Bankpro/')
def admin_main(request):
    """
    admin main page displays bank branches
    """
    username = request.user.get_username()
    user = User.objects.values_list('id', flat=True).filter(username=username)
    user_id = user[0]
    admin = None
    if user_id == 1:
        view_bank_query = Bank.objects.all()
        admin = 1
    else:
        banks = BranchPermissions.objects.values_list('branch_id', flat=True).filter(user_id=user_id)
        view_bank_query = Bank.objects.filter(ifsc_code__in=banks)

    context = {
        "view_bank_query": view_bank_query, "user1": user_id, "admin": admin
    }
    return render(request, "AdminMain.html", locals())


@login_required(login_url='/Bankpro/')
def add_bank(request):
    """
    For Super Admin To Add Bank Branches
    """
    username = request.user.get_username()
    user = User.objects.values_list('id', flat=True).filter(username=username)
    user_id = user[0]
    admin = None
    if user_id == 1:
        admin = 1
    if request.method == "POST":
        add_bank_form = BankForm(request.POST)
        if add_bank_form.is_valid():
            db_instance = Bank()
            db_instance.branch_name = request.POST.get('branch_name')
            db_instance.ifsc_code = request.POST.get('ifsc_code')
            db_instance.branch_address = request.POST.get('branch_address')
            db_instance.branch_contact = request.POST.get('branch_contact')
            db_instance.save()
            return render(request, "success.html", locals())

        else:
            print(add_bank_form.errors)

    else:
        add_bank_form = BankForm()
        print(add_bank_form.errors)

    return render(request, "AdminMain.html", locals(), )


@login_required(login_url='/Bankpro/')
def edit_bank(request, name):
    """
    Update  Bank details if required
    """
    username = request.user.get_username()
    user = User.objects.values_list('id', flat=True).filter(username=username)
    user_id = user[0]
    print(user_id)
    bank_list = BranchPermissions.objects.values_list('branch_id', flat=True).filter(user_id=user_id)
    print(list(bank_list))
    true = 0
    admin = None
    if user_id == 1:
        admin = 1
        true = 1
    if name in list(bank_list):
        true = 1
    print(true)
    if true == 1:
        if request.method == "POST":
            db_instance = Bank()
            db_instance.branch_name = request.POST.get('branch_name')
            db_instance.ifsc_code = request.POST.get('ifsc_code')
            db_instance.branch_address = request.POST.get('branch_address')
            db_instance.branch_contact = request.POST.get('branch_contact')
            db_instance.save()
            return render(request, "success.html", locals())
        else:
            edit_bank_query = Bank.objects.filter(ifsc_code=name)
            context = {
                "edit_bank_query": edit_bank_query, "username": username, "admin": admin,
                "user_id": user_id, "name": name
            }
            return render(request, "AdminMain.html", context)
    else:
        return redirect("logout")


@login_required(login_url='/Bankpro/')
def add_account(request):
    """
    Create new Accounts to Particular Bank Branches
    """
    username = request.user.get_username()
    user = User.objects.values_list('id', flat=True).filter(username=username)
    user_id = user[0]
    if request.method == "POST":
        add_account_form = AccountForm(request.POST)
        if add_account_form.is_valid():
            db_instance = Account()
            db_instance.account_no = request.POST.get('account_no')
            db_instance.account_holder = request.POST.get('account_holder')
            db_instance.account_type = request.POST.get('account_type')
            db_instance.pancard_no = request.POST.get('pancard_no')
            db_instance.address = request.POST.get('address')
            db_instance.contact = request.POST.get('contact')
            db_instance.bank_id = request.POST.get('bank')
            db_instance.save()
            return render(request, "success.html", locals())

        else:
            print(add_account_form.errors)

    else:
        admin = None
        if user_id == 1:
            bank_list_add_account = Bank.objects.all()
            admin = 1
        else:
            banks = BranchPermissions.objects.values_list('branch_id', flat=True).filter(user_id=user_id)
            bank_list_add_account = Bank.objects.values('branch_name', 'ifsc_code').filter(ifsc_code__in=banks)
        add_account_form = AccountForm()
        print(add_account_form.errors)

    return render(request, "AdminMain.html", locals(), )


@login_required(login_url='/Bankpro/')
def view_account(request):
    """
    View Accounts Based on Branches
    """
    username = request.user.get_username()
    user = User.objects.values_list('id', flat=True).filter(username=username)
    user_id = user[0]
    admin = None
    if user_id == 1:
        admin = 1
    if request.method == "POST":
        bank = request.POST.get('bank')
        accounts = Account.objects.filter(bank_id=bank)
        context = {
            "accounts": accounts, "username": username, "admin": admin,
            "user_id": user_id
        }
        return render(request, "AdminMain.html", context)
    else:
        if user_id == 1:
            bank_list = Bank.objects.all()
            admin = 1
        else:
            banks = BranchPermissions.objects.values_list('branch_id', flat=True).filter(user_id=user_id)
            bank_list = Bank.objects.values('branch_name', 'ifsc_code').filter(ifsc_code__in=banks)
    return render(request, "AdminMain.html", locals())


@login_required(login_url='/Bankpro/')
def edit_account(request, account):
    """
    Update Account Details If required
    """
    username = request.user.get_username()
    user = User.objects.values_list('id', flat=True).filter(username=username)
    user_id = user[0]
    banks = BranchPermissions.objects.values_list('branch_id', flat=True).filter(user_id=user_id)
    bank_accounts = Bank.objects.values_list('ifsc_code', flat=True).filter(ifsc_code__in=banks)
    account_list = Account.objects.values_list('account_no', flat=True).filter(bank_id__in=banks)
    acc = 0
    account = int(account)
    print(list(account_list))
    if account in list(account_list):
        acc = 1
    admin = None
    if user_id == 1:
        admin = 1
        acc = 1
    print(acc)
    if acc == 1:
        if request.method == "POST":
            db_instance = Account()
            db_instance.account_no = request.POST.get('account_no')
            db_instance.account_holder = request.POST.get('account_holder')
            db_instance.account_type = request.POST.get('account_type')
            db_instance.pancard_no = request.POST.get('pancard_no')
            db_instance.bank_id = request.POST.get('bank')
            db_instance.address = request.POST.get('address')
            db_instance.contact = request.POST.get('contact')
            db_instance.save()
            return render(request, "success.html", locals())
        else:
            edit_account_query = Account.objects.filter(account_no=account)
            context = {
                "edit_account_query": edit_account_query, "username": username,
                "admin": admin, "user_id": user_id, "account": account
            }
            return render(request, "AdminMain.html", context)
    else:
        return redirect(reverse("logout"))


@login_required(login_url='/Bankpro/')
def choose_account_add_transaction(request):
    """
    Add transactions on bank accounts
    """
    username = request.user.get_username()
    user = User.objects.values_list('id', flat=True).filter(username=username)
    user_id = user[0]
    admin = None
    if user_id == 1:
        admin = 1
    if request.method == "POST":
        db_instance = Transaction()
        db_instance.transaction_type = request.POST.get('transaction_type')
        db_instance.account_id = request.POST.get('account')
        db_instance.date = request.POST.get('date')
        db_instance.time = request.POST.get('time')
        db_instance.amount = request.POST.get('amount')
        db_instance.save()
        return render(request, "success.html", locals())

    else:
        if user_id == 1:
            transaction_account = Account.objects.values('account_no')
            admin = 1
        else:
            banks = BranchPermissions.objects.values_list('branch_id', flat=True).filter(user_id=user_id)
            bank_account_transaction = Bank.objects.values_list('ifsc_code', flat=True).filter(ifsc_code__in=banks)
            transaction_account = Account.objects.values('account_no').filter(bank_id__in=bank_account_transaction)
        add_transaction_form = TransactionForm()
        print(add_transaction_form.errors)
        return render(request, "AdminMain.html", locals())


@login_required(login_url='/Bankpro/')
def choose_account_view_transaction(request):
    """
    Choose account to view it's transactions
    """
    username = request.user.get_username()
    user = User.objects.values_list('id', flat=True).filter(username=username)
    user_id = user[0]
    admin = None
    if user_id == 1:
        admin = 1
    if request.method == "POST":
        account = request.POST.get('account')
        transaction_account_query = Transaction.objects.filter(account_id=account)
        context = {"transaction_account_query": transaction_account_query, "username": username,
                   "admin": admin, "user_id": user_id}
        return render(request, "AdminMain.html", context)

    else:
        if user_id == 1:
            view_transaction_account = Account.objects.values('account_no')
            admin = 1
        else:
            banks = BranchPermissions.objects.values_list('branch_id', flat=True).filter(user_id=user_id)
            bank_account_transaction = Bank.objects.values_list('ifsc_code', flat=True).filter(ifsc_code__in=banks)
            view_transaction_account = Account.objects.values('account_no').filter(bank_id__in=bank_account_transaction)
        return render(request, "AdminMain.html", locals())
