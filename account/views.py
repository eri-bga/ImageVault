from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import Contact
from actions.utils import create_action
from actions.models import Action


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             user = authenticate(request,
#                                 username=cleaned_data['username'],
#                                 password=cleaned_data['password'],
#             )
#             if user is not None and user.is_active:
#                 login(request, user)
#                 return HttpResponse('Authentication successful')
#             else:
#                 return HttpResponse('Authentication failed')
            
#         else:
#             form = LoginForm()
#         return render(request, 'templates/account/login.html', {'form': form})

@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
                    .prefetch_related('target')[:10]
    return render(request,
                'account/dashboard.html',
                {'section': 'dashboard',
                'actions': actions})
    
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            messages.success(request, 'Registration successful', extra_tags='alert-success')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed', alert_tags='alert-error')
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', 
                {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, 
                                    data=request.POST, 
                                    files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error updating your profile')
            return redirect('dashboard')
    else:
        # try:
        try:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            
            return render(request, 
                'account/edit.html', 
                {'user_form': user_form,
                'profile_form': profile_form})
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user)
    
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 
                'account/user/list.html', 
                {'section': 'people', 
                'users': users})
    
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, 
                             is_active=True)
    return render(request, 
                  'account/user/detail.html', 
                  {'section': 'people',
                   'user': user})
    
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                        user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})