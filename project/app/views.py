from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Profile, CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db import connection


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        custom_user = CustomUser.objects.create(username=username, password=password) #save plain text here
        Profile.objects.create(user=custom_user)
        return redirect('login')
    return render(request, 'register.html')

#FIX:
# use django's built in User model to hash the password
# user = User.objects.create_user(username=username, password=password)
# then create a profile linked to the django User
# Profile.objects.create(user=user)
# the secure Profile object will be in models.py

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            if user.password == password: #Here is the plain text comparison 
                return redirect('user_profile', user_id=user[0])
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})            
        except CustomUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


    # FIX:
    # user = authenticate(request, username=username, password=password)
    # if user is not None:
    #     login(request, user)
    #     return redirect('user_profile', user_id=user.id)
    # else:
    #     return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# broken access control
# user profile allows any authenticated user to access other user's profile
# by altering the user_id in the url
@login_required
def user_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    return render(request, 'profile.html', {'user': user, 'profile': profile})

@login_required
def proper_user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user.id == user_id:
        return render(request, 'profile.html', {'user': user})
    else:
        return redirect('login')

@login_required
def search(request):
    return render(request, 'search.html')

#injection
@login_required
def search_results(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')
    result = []
    if query:
        if search_type == 'wonky':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM auth_user WHERE username LIKE '%{}%'".format(query))
                result = cursor.fetchall()
        else:
            result = CustomUser.objects.filter(username__icontains=query)
    return render(request, 'result.html', {'result': result})