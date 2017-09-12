from django.conf.urls import url
from django.contrib import admin
from qsbk_app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^qiushibaike', views.qsbk),
]
