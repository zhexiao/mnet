from django.conf.urls import url
from .views import (
    TestApi,
    TotalStats,
    DateHistory
)

urlpatterns = [
    url(r'^test/?$', TestApi.as_view()),
    url(r'^total/?$', TotalStats.as_view()),
    url(r'^date_history/?$', DateHistory.as_view())
]
