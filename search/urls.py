from django.urls import path, include
from search.views import SearchProductView

app_name = "search"
urlpatterns = [
    path('search/', SearchProductView.as_view(), name="search_product"),
]
