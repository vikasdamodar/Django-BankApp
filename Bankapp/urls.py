from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login_user, name="login"),
    url(r'^logout$', views.logout_user, name="logout"),
    url(r'^admin/$', views.admin_main, name="admin"),
    url(r'^addBank/$', views.add_bank, name="addBank"),
    # url(r'^editBank/$', views.edit_bank, name="editBank"),
    url(r'^editBank/([0-9A-Za-z]+)/$', views.edit_bank, name="editBank"),
    url(r'^addAccount/$', views.add_account, name="addAccount"),
    url(r'^viewAccount/$', views.view_account, name="viewAccount"),
    url(r'^editAccount/$', views.edit_account, name="editAccount"),
    url(r'^editAccount/([0-9A-Za-z]+)/$', views.edit_account, name="editAccount"),
    url(r'^AddTransaction/$', views.choose_account_add_transaction, name="chooseAccount"),
    # url(r'^addTransaction/$', views.add_transaction, name="addTransaction"),
    url(r'^viewTransaction/$', views.choose_account_view_transaction, name="viewTransaction"),

]
