from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from project import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("projects/", views.project_list, name="projects"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
