from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)

urlpatterns = [
    path("admin/", admin.site.urls),
    # 1
    path("django/jsonresponsenomodel/", views.no_rest_no_model),
    # 2
    path("django/jsonresponsefrommodle/", views.no_rest_from_model),
    # 3
    path("rest/fbv/", views.FBV_list),
    # 4
    path("rest/fbv/<int:pk>", views.FBV_pk),
    # 5
    path("rest/cbv/", views.CBV_LIST.as_view()),
    # 6
    path("rest/cbv/<int:pk>", views.CBV_pk.as_view()),
    # 7
    path("rest/mixins/", views.mixins_list.as_view()),
    # 8
    path("rest/mixins/<int:pk>", views.mixins_pk.as_view()),
    # 9
    path("rest/generics/", views.generics_list.as_view()),
    # 10
    path("rest/generics/<int:pk>", views.generics_pk.as_view()),
    # 11
    path("rest/viewsets/", include(router.urls)),
    # 12
    path("fbv/findmovie/", views.find_movie),
]