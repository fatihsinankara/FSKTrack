from django.urls import path
from .views import (
    CustomLoginView,
    CargoListView,
    CargoCreateView,
    CargoUpdateView,
    CargoDeleteView,
    CargoDetailView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', CargoListView.as_view(), name='cargo_list'),
    path('cargo/<int:pk>/', CargoDetailView.as_view(), name='cargo_detail'),
    path('cargo/add/', CargoCreateView.as_view(), name='cargo_add'),
    path('cargo/<int:pk>/update/', CargoUpdateView.as_view(), name='cargo_update'),
    path('cargo/<int:pk>/delete/', CargoDeleteView.as_view(), name='cargo_delete'),
]
