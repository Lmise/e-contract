from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    # contract views
    url(r'^$', views.contract_list, name='contract_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.contract_list, name='contract_list_by_tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<contract>[-\w]+)/',
        views.contract_detail, name='contract_detail'),
    url(r'^(?P<contract_id>\d+)/share/$', views.contract_share, name='contract_share'),
]





