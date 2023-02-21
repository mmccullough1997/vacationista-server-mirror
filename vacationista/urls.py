"""vacationista URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls import include
from rest_framework import routers
from django.contrib import admin
from django.urls import path

from vacationistaapi.views import register_user, check_user, ArticleView, HighlightView, RecommendationView, UserView, TransportationTypeView, ExpenseTypeView, EventTypeView, TripLegView, TripView, LegView, TransportationView, EventView, ExpenseView, YelpAPIView, AutocompleteAPIView

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'articles', ArticleView, 'article')
router.register(r'highlights', HighlightView, 'highlight')
router.register(r'recommendations', RecommendationView, 'recommendation')
router.register(r'users', UserView, 'user')
router.register(r'transportationtypes', TransportationTypeView, 'transportationtype')
router.register(r'expensetypes', ExpenseTypeView, 'expensetype')
router.register(r'eventtypes', EventTypeView, 'eventtype')
router.register(r'trips', TripView, 'trip')
router.register(r'legs', LegView, 'leg')
router.register(r'triplegs', TripLegView, 'tripleg')
router.register(r'transportations', TransportationView, 'transportation')
router.register(r'expenses', ExpenseView, 'expense')
router.register(r'events', EventView, 'event')

urlpatterns = [
    path('register', register_user),
    path('checkuser', check_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('locations/<str:param>/', YelpAPIView.as_view()),
    path('autocomplete/<str:param>/', AutocompleteAPIView.as_view())
]
