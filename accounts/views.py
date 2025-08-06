from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Passenger, Driver
from .forms import DriverRegistrationForm
from vehicles.models import Vehicle


# Create your views here.
class BaseLoginView(View):
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next') # GET is from in HTTP 
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
                return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_login
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = self.form_login(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = cd['phone_number']
            password = cd['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'user {phone_number} logged in')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,'phone number or password is incorrect')
        return render(request,self.template_name,{'form':form})
    
    
class PassengerLoginView(BaseLoginView):
    form_login = PassengerLoginForm
    template_name = 'accounts/passenger/login.html'


class DriverLoginView(BaseLoginView):
    form_login = DriverLoginForm
    template_name = 'accounts/driver/login.html'

    
class LogoutView(View):
     def get(self,request):
            logout(request)
            messages.success(request, 'logged out.')
            return redirect('home:home')


class PassengerRegisterView(View):
    form_class = PassengerRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/passenger/register.html',{'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            passenger, error = Passenger.create_passenger(
                phone_number=cd['phone_number'],
                full_name=cd['full_name'],
                password=cd['password'],
                national_number=cd['national_number'],
                age=cd['age']
            )
            if passenger:
                return redirect('accounts:passenger_login')
            else:
                messages.error(request, 'An error occured: ' + error)

        return render(request, 'accounts/passenger/register.html', {'form': form})



class DriverRegisterView(View):
    form_class = DriverRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/driver/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            driver, error = Driver.create_driver(
                phone_number=cd['phone_number'],
                full_name=cd['full_name'],
                password=cd['password'],
                national_number=cd['national_number'],
                age=cd['age'],
                license_number=cd['license_number'],
                vehicle=cd['vehicle']
            )
            if driver:
                return redirect('accounts:driver_login')
            else:
                messages.error(request, ': ' + error)

        return render(request, 'accounts/driver/register.html', {'form': form})


    
