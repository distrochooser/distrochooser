"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from distrochooser.views import start, loadQuestion, submitAnswers, getLocales, vote, getGivenAnswers, updateRemark,getSSRData, getStatus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('start/<str:langCode>/', start, name='start'),
    path('locales/', getLocales, name='locales'),
    path('ssrdata/<str:langCode>/', getSSRData, name='getTranslation'),
    path('question/<str:langCode>/<int:index>/<str:token>/', loadQuestion, name='loadQuestion'),
    path('submit/<str:langCode>/<str:token>/', submitAnswers, name='submitAnswers'),
    path('vote/', vote, name='voteSelection'),
    path('remarks/', updateRemark, name='updateRemark'),
    path('answers/<str:slug>/', getGivenAnswers, name='getGivenAnswers'),
    path('status/<str:slug>/', getStatus, name='getStatus')
]
