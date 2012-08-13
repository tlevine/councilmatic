from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns(
    'cm',

    url(r'^profile$', views.ProfileAdminView.as_view(),
        name='cm_profile_admin'),

    url(r'^$', views.LandingPageView.as_view(),
        name='landing'),
    url(r'^$', views.LandingPageView.as_view(),
        name='browse'),
    url(r'^$', views.LandingPageView.as_view(),
        name='about'),
    url(r'^$', views.LandingPageView.as_view(),
        name='login'),
    url(r'^$', views.LandingPageView.as_view(),
        name='signup'),
    url(r'^$', views.LandingPageView.as_view(),
        name='search'),
)
