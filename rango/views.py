from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
  category_list = Category.objects.all()[:5]
  context_dict = {"categories":category_list}	
  return render(request,'rango/index.html',context_dict)

def category(request, category_name_slug):
  context_dict = {}
  try:
  	category = Category.objects.get(slug = category_name_slug)
  	context_dict['category_name'] = category.name
  	context_dict['category'] = category
  	pages = Page.objects.filter(category = category)
  	context_dict['pages'] = pages
  except Category.DoesNotExist:
  	pass

  return render(request, 'rango/category.html', context_dict)	

def add_category(request):
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})  


def register(request):
  registered = False
  if request.method=='POST':
    user_form = UserForm(data = request.POST)
    profile_form = UserProfileForm(data = request.POST)
    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()
      profile = profile_form.save(commit=False)
      profile.user = user
      if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']
      profile.save()
      
      registered = True
    else:
      print user_form.errors, profile_form.errors
  else:
    user_form = UserForm()
    profile_form = UserProfileForm()
  if registered:
    return render(request,'/rango/index.html',{})
  else:  
    context_instance = {'user_form':user_form,'profile_form':profile_form}  
    return render(request,'rango/register.html',context_instance)  

def user_login(request):
  if request.method=='POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
      if user.is_active:
        login(request,user)
        return HttpResponseRedirect('/rango/')
      else:
        return HttpResponse('Your Account is disabled')
    else:
      return HttpResponse('Invalid Login Details Provided')
  else:
    return render(request, 'rango/login.html',{}) 

def loggedout(request):
  logout(request)
  return index(request)
  

@login_required
def restricted(request):
  return HttpResponse('Since You are logged in, You can see this text')
        












  




















