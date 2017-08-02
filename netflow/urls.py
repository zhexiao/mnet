from django.conf.urls import url
from netflow.views import (
    TestApi,
    IpStats,
    IpDateRecord
)

urlpatterns = [
    url(r'^test/?$', TestApi.as_view()),
    url(r'^ip_stats/?$', IpStats.as_view()),
    url(r'^ip_date_records/?$', IpDateRecord.as_view()),
]
