from boto.s3.connection import S3Connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import UserForm, LoginForm
from .models import S3File

class S3FileCreateView(CreateView):
    model = S3File
    fields = ['upload', 'description']
    success_url = reverse_lazy('files')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(S3FileCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s3files = S3File.objects.all()
        context['s3files'] = s3files
        return context

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data
            username = login_data['user_name']
            password = login_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    #return HttpResponse('Authenticated ' \
                    #       'successfully')
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user_data = form.cleaned_data
                if User.objects.filter(username=user_data['user_name']).exists():
                    form = UserForm()
                    return render(request, 'signup.html', {'user_taken': True, 'form': form})

                user = User.objects.create_user(
                    username=user_data['user_name'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'])
                return HttpResponseRedirect('/login/')
            except Exception as e:
                return HttpResponse(e)

    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')