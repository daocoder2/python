"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

app_name = 'polls'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^shortcut/$', views.index, name='index'),
    # url(r'^detail/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # /polls/result/5
    # url(r'^result/(?P<question_id>[0-9]+)/$', views.results, name='results'),
    url(r'^result/(?P<pk>[0-9]+)/$', views.ResultsView.as_view(), name='results'),
    url(r'^vote/(?P<question_id>[0-9]+)/$', views.vote, name='vote'),
]
