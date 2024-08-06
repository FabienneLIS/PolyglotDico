"""
URL configuration for dico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from listings import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home_page/", views.home_page, name="home-page"),
    path("dictionary/list/", views.dictionary_list, name="dictionary-list"),
    path("dictionary/add/", views.dictionary_add, name="dictionary-add"),
    path('dictionary/<int:id>/update/', views.dictionary_update, name='dictionary-update'),
    
    path(
        "dictionary/<int:id>/delete/",
        views.dictionary_list_delete,
        name="dictionary-delete",
    ),
    path(
        "dictionary/<int:dictionary_id>/",
        views.dictionary_detail,
        name="dictionary-detail",
    ),
    path("dictionary/<int:dictionary_id>/new_word/", views.new_word, name="new-word"),
    path('word/<int:word_id>/delete/', views.new_word_delete, name='word-delete'),


]