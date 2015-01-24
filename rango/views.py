from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

def index(request):
  request.session.set_test_cookie()
  category_list = Category.objects.all()[:5]
  context_dict = {"categories":category_list}	
  visits = int(request.COOKIES.get('visits','1'))
  recent_last_visit_time = False
  response = render(request,'rango/index.html',context_dict)
  if 'last_visit' in request.COOKIES:
    last_visit = request.COOKIES['last_visit']
    last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
    if (datetime.now()-last_visit_time).seconds > 1:
      visits = visits + 1
      recent_last_visit_time = True
  else:
    reset_last_visit_time = True
    context_dict['visits'] = visits    
    response = render(request, 'rango/index.html', context_dict)
  response.set_cookie('last_visit', datetime.now())
  if recent_last_visit_time:
    response.set_cookie('visits', visits)
  return response    
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
  if request.session.test_cookie_worked():
    print ">>>> TEST COOKIE WORKED!"
    request.session.delete_test_cookie()
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
        












  




















