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
from distrochooser.views import start, load_question, submit_answers, get_locales, vote, get_given_answers, update_remark, get_ssr_data, get_language_values, get_stats, get_feedback, process_feedback
from backend.settings import CONFIG

system_suffix = CONFIG["backend"]["SUFFIX"]

urlpatterns = [
    path('admin{0}/'.format(system_suffix), admin.site.urls),
    path('start/<str:lang_code>/<str:reflink_encoded>/', start, name='start'),
    path('locales/', get_locales, name='locales'),
    path('ssrdata/<str:lang_code>/', get_ssr_data, name='get_ssr_data'),
    path('question/<int:index>/', load_question, name='loadQuestion'),
    path('submit/<str:lang_code>/<str:token>/<str:method>/', submit_answers, name='submit_answers'),
    path('vote/', vote, name='voteSelection'),
    path('remarks/', update_remark, name='update_remark'),
    path('answers/<str:token>/', get_given_answers, name='get_given_answers'),
    path('translation/<str:lang_code>/', get_language_values, name="get_language_values"),
    path('stats{0}/'.format(system_suffix), get_stats, name="get_stats"),
    path('feedback{0}/'.format(system_suffix), get_feedback, name="get_feedback"),
    path('process_feedback{0}/<str:token>/'.format(system_suffix), process_feedback, name="process_feedback")
    
]