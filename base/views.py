from django.shortcuts import render
from .models import Task

# LoginRequiredMixin : Only logged in users can access the taklist view.
# Go to the settings and add this , so that it will redirect you to the login page.
# In settings.py
    # LOGIN_URL = 'login'
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


#######################################################  LIST VIEW ######################################################

from django.views.generic.list import ListView



# LoginRequiredMixin If i am not logged in , it will redirect me to the login page. 
# How will redirect,
# add this in the settings.py
# LOGIN_URL = "login"  (name of the url.)
class TaskList(LoginRequiredMixin,ListView):
    model = Task


# template_name: By default the ListView Looks for a template with the prefix of the model name (task) and 
# the suffix of _list.html if not otherwise set (task_list.html). This can be overridden by setting the “template_name” 
# attribute.

# context_object_name: Override the default queryset name of “object_list” by setting the “context_object_name” attribute. 
# It helps to have a more user friendly name to work with besides just “object_list”.

# paginate_by & ordering: The list view also has pagination and ordering already built in. 
# We can set these methods by setting their attributes like I did in the code example above.

    context_object_name = 'tasks'

    # adding some extra context to the page.
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        # Users will able to  see only their data not the whole database
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context








#######################################################  DETAIL VIEW ######################################################
from django.views.generic.detail import DetailView


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    


#######################################################  CREATE VIEW ######################################################

from django.views.generic.edit import CreateView

class TaskCreate(CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = '/'


# After Creating a new user , it doesnt add the items to the list, This form_valid will do that.
# This method is called when the form is POSTED.
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)





#######################################################  UPDATE VIEW ######################################################
from django.views.generic.edit import UpdateView

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = '/'



#######################################################  DELETE VIEW ######################################################

from django.views.generic.edit import DeleteView

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    fields = '__all__'
    success_url = '/'




#######################################################  LOGIN ######################################################

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    # If the user is authenticated , the user will not be allowed on this page.
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('TaskList')


#######################################################  LOGOUT ######################################################

from django.contrib.auth.views import LogoutView
# write this in urls.py
    # path('logout/',LogoutView.as_view(next_page='login'), name='logout')



#######################################################  REGISTER ######################################################

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


# This is because we want that the user after registration should be logged in directly.
from django.contrib.auth import login

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = '/'


    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    # Once you are logged in you cannot access the register page again.
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super(RegisterPage,self).get(self,*args,**kwargs)



#######################################################  SEARCH ######################################################

# add this in the TaskList View.
#       search_input = self.request.GET.get('search-area') or ''
#         if search_input:
#             context['tasks'] = context['tasks'].filter(title__icontains=search_input)
#         context['search_input'] = search_input
#         return context
# search_input = self.request.GET.get(name-of-the-input-type-in-tasklist.html)





#######################################################  Reorder ######################################################
# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))