from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, LoginSuperUserRequiredMixin
from django.http import request 
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Sum
from cinema.models import Hall, Movies, Sessions, Purchase
from cinema.forms import RegisterForm, SessionCreateForm, HallsCreateForm, MoviesCreateForm, \
                        PurchaseForm, SortForm


class Login(LoginView):
    template_name = 'login.html'
        
    def get_success_url(self):
        return '/'


class Logout(LogoutView):
    next_page = '/'


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def get_success_url(self):
        return '/'


class SessionsListView(ListView):
    model = Sessions
    template_name = 'session_list.html'
    # form_class = SessionForm
    extra_context = {'purchase_form': PurchaseForm, }
    paginate_by = 3

    # def get_queryset(self):
    #     today = timezone.now()
    #     tomorrow = timezone.now() + timedelta(days=1)
    #     if self.request.method =="POST":
    #         user_form = SessionForm(data=self.request.POST)
    #         if user_form.is_valid():
    #             if self.request.POST['session_form'] == 'Today':
    #                 self.queryset = Sessions.objects.filter(start_session_time__gte = today)
    #             elif self.request.POST['session_form'] == 'Tomorrow':
    #                 self.queryset = Sessions.objects.filter(start_session_time__gte = tomorrow) 
    #     else:
    #         user_form = SessionForm()
    #     return self.queryset
    def get_queryset(self):
        today = timezone.now()
        tomorrow = timezone.now() + timedelta(days=1)
        session_form = self.request.GET.get('session_form')

        if session_form == 'Today':
            return super().get_queryset().filter(date_start_show__lte = today, date_end_show__gt = today)
        elif session_form == 'Tomorrow':
            return super().get_queryset().filter(date_start_show__lte = tomorrow, date_end_show__gt = tomorrow)
        return super().get_queryset().filter(date_end_show__gt = today)

    def get_ordering(self):
        sort_form = self.request.GET.get('sort_form')
        if sort_form == 'PriceLH':
            self.ordering = ['price']
        elif sort_form == 'PriceHL':
            self.ordering = ['-price']                         
        elif sort_form == "Time":
            self.ordering = ['start_session_time']
        return self.ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = SortForm
        return context


class SessionCreateView(LoginSuperUserRequiredMixin, CreateView):
    model = Sessions
    form_class = SessionCreateForm
    success_url = '/create_sessions/'
    template_name = 'create_sessions.html'
    
    def form_valid(self, form):
        movie = form.save(commit=False)
        hall = Hall.objects.get(id=self.request.POST['hall_name'])
        movie.free_seats = hall.size
        movie.save()
        return super().form_valid(form=form)    
        
class HallsCreateView(LoginSuperUserRequiredMixin, CreateView):
    model = Hall
    form_class = HallsCreateForm
    success_url="/"
    template_name = 'create_halls.html'
    
class MoviesCreateView(LoginSuperUserRequiredMixin, CreateView):
    login_url = "login/"
    form_class = MoviesCreateForm
    template_name = 'create_movies.html'
    extra_context = {'add_form': MoviesCreateForm()}
    success_url='/movies/list_of_movies'

class MoviesListView(LoginRequiredMixin, ListView):
    model = Movies
    login_url = "login/"
    template_name = 'movies_list.html'

class ProductPurchaseView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'session_list.html'
    paginate_by = 5
    success_url='/'

    def form_valid(self, form):
        purchase = form.save(commit=False)
        quantity = int(form.data['quantity'])
        user = self.request.user
        purchase.сonsumer = user
        session = Sessions.objects.get(id=self.request.POST['session'])
        purchase.session = session
        hall = session.hall_name
        total_quantity = session.purchase_session.aggregate(Sum('quantity'))['quantity__sum']
        if not total_quantity:
            total_quantity = 0
        free_seats = hall.size - total_quantity
        if free_seats < quantity:
            messages.error(self.request, f'Dont enough free seats! Available seats: {free_seats}')
            return redirect(f"/")
        user.spent += quantity * session.price
        user.save()
        purchase.save()
        return super().form_valid(form=form)
       
class ProductPurchaseListView(LoginRequiredMixin, ListView):
    login_url = "login/"
    model = Purchase
    template_name = 'purchases_list.html'
    
    # def get_queryset(self):
    #     return super().get_queryset().filter(consumer=self.request.user)

class UpdateProductView(LoginSuperUserRequiredMixin, UpdateView):
    template_name = 'update_sessions.html'
    model = Sessions
    form_class = SessionCreateForm
    success_url = '/'

class UpdateProductView(LoginSuperUserRequiredMixin, UpdateView):
    template_name = 'update_sessions.html'
    model = Sessions
    form_class = SessionCreateForm
    success_url = '/'


class UpdateHallsView(LoginSuperUserRequiredMixin, UpdateView):
    template_name = 'update_halls.html'
    model = Hall
    form_class = HallsCreateForm
    success_url = '/'