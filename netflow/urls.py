from django.conf.urls import url
from netflow.views import TestApi

urlpatterns = [
    url(r'^test/?$', TestApi.as_view()),
]
