from django.conf.urls import url
from lists import views as list_views
from lists import urls as list_urls

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'lists/', include(list_urls)),
]
