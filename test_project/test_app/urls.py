from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('registration/', views.registration, name='registration'),
    path('catalog/', views.catalog, name='catalog'),
    path('test/<int:test_case_pk>/', views.test_view, name='test'),
    path('test/<int:test_case_pk>/<int:test_index>/', views.test_page, name='test-page'),
    path('test/result/<int:test_case_pk>/', views.test_result, name='test-result'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('contacts/', views.contacts, name='contacts')
]
