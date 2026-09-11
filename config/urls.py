from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from accounts.views import AppLoginView
urlpatterns=[path('admin/',admin.site.urls),path('',include('accounting.urls')),path('accounts/',include('accounts.urls')),path('manifest.webmanifest',TemplateView.as_view(template_name='manifest.webmanifest',content_type='application/manifest+json'),name='manifest.webmanifest'),path('service-worker.js',TemplateView.as_view(template_name='service-worker.js',content_type='application/javascript'),name='service-worker.js'),path('login/',AppLoginView.as_view(),name='login'),path('logout/',__import__('django.contrib.auth.views',fromlist=['LogoutView']).LogoutView.as_view(),name='logout')]
