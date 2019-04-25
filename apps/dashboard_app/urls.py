from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^edit_user$', views.edit_user),
    url(r'^update_user$', views.update_user),
    url(r'^(?P<id>[0-9]+)/delete$', views.delete),
    url(r'^quote_post$', views.quote_post),
    url(r'^quote_list$', views.quote_list),
    url(r'^(?P<id>[0-9]+)/quote_user_list$', views.quote_user_list),
    url(r'^(?P<id>[0-9]+)/like_quote$', views.like_quote),
    url(r'^clear$', views.clear),
    
]