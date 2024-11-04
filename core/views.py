from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Cargo
from .utils import get_parser
from .forms import CargoForm

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('login')  # Yetkisiz kullanıcıları giriş sayfasına yönlendir

class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def form_valid(self, form):
        if form.get_user().is_superuser:
            return super().form_valid(form)
        else:
            return self.form_invalid(form)  # Superuser olmayan giriş yapamaz

class CargoListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Cargo
    template_name = 'core/cargo_list.html'
    context_object_name = 'cargos'

class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'core/cargo_form.html'
    success_url = reverse_lazy('cargo_list')

class CargoUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Cargo
    template_name = 'core/cargo_form.html'
    fields = ['carrier_name', 'tracking_number', 'tracking_url_template']
    success_url = reverse_lazy('cargo_list')

class CargoDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Cargo
    template_name = 'core/cargo_confirm_delete.html'
    success_url = reverse_lazy('cargo_list')

class CargoDetailView(DetailView):
    model = Cargo
    template_name = 'core/cargo_detail.html'
    context_object_name = 'cargo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cargo = self.get_object()
        
        # Parsingi başlat
        try:
            parser = get_parser(cargo.carrier_name, cargo.get_tracking_url())
            cargo_data = parser.parse()
            context['cargo_data'] = cargo_data
        except Exception as e:
            context['error'] = str(e)
        
        return context