from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db import connection



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM auth_user WHERE username = %s AND password = %s", [username, password])
            user = cursor.fetchone()

        if user:
            return redirect('user_profile', user_id=user[0])
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})            

        # FIX:
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('user_profile', user_id=user.id)
        # else:
        #     return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# broken access control
@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profile.html', {'user': user})

@login_required
def proper_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
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
            result = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{query}'")
        else:
            result = User.objects.filter(username__icontains=query)
    return render(request, 'result.html', {'result': result})