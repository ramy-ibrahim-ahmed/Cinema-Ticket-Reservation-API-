from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter

# router registration
router = DefaultRouter()
# get (url, views.(viewsets function))
router.register("guests", views.viewsets_guest)
router.register("movies", views.viewsets_movie)
router.register("reservations", views.viewsets_reservation)

urlpatterns = [
    path("admin/", admin.site.urls),
    # 1 without rest framework and no model query (FBV)
    path("django/jsonresponsenomodel/", views.no_rest_no_model),
    # 2 model data default django without rest framework (FBV)
    path("django/jsonresponsefrommodle/", views.no_rest_from_model),
    # 3.1 function based views GET POST
    path("rest/fbv/", views.FBV_list),
    # 3.2 function based views GET PUT DELETE
    path("rest/fbv/<int:pk>", views.FBV_pk),
    # 4.1 class based views GET & POST
    path("rest/cbv/", views.CBV_LIST.as_view()),
    # 4.2 class based views GET & PUT & DELETE
    path("rest/cbv/<int:pk>", views.CBV_pk.as_view()),
    # 5.1 mixins list GET GET POST
    path("rest/mixins/", views.mixins_list.as_view()),
    # 5.2 mixins list GET PUT DELETE
    path("rest/mixins/<int:pk>", views.mixins_pk.as_view()),
    # 6.1 Generics GET  POST
    path("rest/generics/", views.generics_list.as_view()),
    # 6.2 Generics GET PUT DELETE
    path("rest/generics/<int:pk>", views.generics_pk.as_view()),
    # 7 viewsets GET POST PUT DELETE
    # use router
    path("rest/viewsets/", include(router.urls)),
]
