"""vendr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # OAuth.
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Web sockets.
    
    # API.
    url(r'^v1/search', include('ksearch.urls')),
    url(r'^v1/properties/', include('kproperty.urls')),
    url(r'^v1/users/', include('kuser.urls')),
    url(r'^v1/autocomplete', include('autocomplete.urls')),
    url(r'^v1/transactions/', include('transaction.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

