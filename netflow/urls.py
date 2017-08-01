from django.conf.urls import url
from netflow.views import (
    TestApi,
    SrcIpStats
)

urlpatterns = [
    url(r'^test/?$', TestApi.as_view()),
    url(r'^src_ip_stats/?$', SrcIpStats.as_view()),
]
