from django.conf.urls import url, include
from django.contrib import admin
from Bankapp.views import login_user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^Bankpro/', include('Bankapp.urls')),
    url(r'^$', login_user),
]
