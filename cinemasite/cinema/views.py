from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, LoginSuperUserRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from cinema.models import Hall, Movies, Sessions, Purchase
from cinema.forms import RegisterForm, SessionCreateForm, HallsCreateForm, MoviesCreateForm, PurchaseForm, SortForm


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
    extra_context = {'purchase_form': PurchaseForm, }
    paginate_by = 5

    def get_ordering(self):
        sort_form = self.request.GET.get('sort_form')
        if sort_form == 'PriceLH':
            self.ordering = ['price']
        elif sort_form == 'PriceHL':
            self.ordering = ['-price']                         
        elif sort_form == "Time":
            print("I am here!")
            self.ordering = ['start_session_time']
        return self.ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = SortForm
        return context


class SessionCreateView(LoginSuperUserRequiredMixin, CreateView):
    model = Sessions
    permission_required = 'is_superuser'
    form_class = SessionCreateForm
    success_url = '/add_sessions/'
    template_name = 'add_sessions.html'
    
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
        purchase.consumer = self.request.user
        session = Sessions.objects.get(id=self.request.POST['session_id'])
        cash = session.price * purchase.quantity
        free_seats = session.free_seats - purchase.quantity

        if free_seats > 0:
            session.free_seats -= purchase.quantity
            consumer = self.request.user
            consumer.spent += cash
            purchase.session_id = self.request.POST['session_id']
            session.save()
            consumer.save()
            purchase.save()
            return super().form_valid(form=form)
        else:
            messages.error(self.request,'No available amount')
            return redirect(f"/")

class ProductPurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'purchases_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(consumer=self.request.user)
        return queryset

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