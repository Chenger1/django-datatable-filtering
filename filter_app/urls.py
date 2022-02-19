from django.urls import path

from .views import MainView, MainViewFilter


app_name = 'filter'


urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path('filter/', MainViewFilter.as_view(), name='main_view_filter')
]
