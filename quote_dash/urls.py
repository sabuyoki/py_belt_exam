from django.conf.urls import url, include	# added an import!
urlpatterns = [
    url(r'^', include('apps.dashboard_app.urls')),	# use your app_name here
]
