"""adminsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from rest_framework.documentation import include_docs_urls
from event import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^docs/', include_docs_urls(title='API Doc')),
    url(r'^admin/', admin.site.urls),
    url(r'^event/(?P<ids>(\d+[,]?)+)$', views.get_events),
    url(r'^event/timeline/event/search$', views.get_timeline_search_events),
    url(r'^event/index/search$', views.search_event_index),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
