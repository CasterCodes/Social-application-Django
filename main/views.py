from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import UserProfile, Post, PostLikes, Following
from itertools import chain
import random

# Create your views here.

@login_required(login_url='login')
def index(request):
    loggedin_user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=loggedin_user)

    user_following_usernames = []
    feed = []

    followings = Following.objects.filter(follower=request.user.username)

    for follow in followings:
        user_following_usernames.append(follow.user)

    for username in user_following_usernames:
        feed_lists =  Post.objects.filter(user=username)
        feed.append(feed_lists)

    posts =  list(chain(*feed))

    # User suggestion algorithim begins here

    users = User.objects.all()

    users_user_is_following = []

    for user in followings: 
        print(user)
        user_result = User.objects.filter(username=user)
        users_user_is_following.append(user_result)

    suggestions =  [x for x in list(users) if (x not in list(users_user_is_following))]

    logged_in_user = User.objects.filter(username=request.user.username)

    new_user_suggestions  =  [x for x in list(suggestions) if x not in list(logged_in_user)]

    random.shuffle(new_user_suggestions)


    suggestions_profile = []

    for user in new_user_suggestions:
        suggestion_profile  = UserProfile.objects.filter(user=user)
        suggestions_profile.append(suggestion_profile)

    actual_suggestions = list(chain(*suggestions_profile))

    context = {'user_profile': user_profile, 'posts': posts, 'suggestions': actual_suggestions[:5]}

    return render(request, 'index.html', context)

@login_required(login_url='login')
def search(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user);

    if request.method == 'POST':
        search_query = request.POST.get('username')

        usernames_results = User.objects.filter(username__icontains=search_query)
       
        profile_results_list = []

        for username in usernames_results:
          user_profile_result = UserProfile.objects.filter(user=username)
          profile_results_list.append(user_profile_result)

        profiles = list(chain(*profile_results_list))

        print(profiles)

        return render(request, 'search.html', {
        'user_profile': user_profile,
        "profiles": profiles
        
          })

       

        
         

    

         

    


@login_required(login_url='login')   
def follow(request):
    if(request.method != 'POST'):
        return redirect('/')

    follower = request.POST.get('follower')
    user = request.POST.get('user')
    loggedin_user_follows = Following.objects.filter(follower=follower, user=user).first()

    if loggedin_user_follows == None:

        following = Following.objects.create(follower=follower,user=user)
        following.save()
        return redirect('/profile/'+user)
    
    loggedin_user_follows.delete()

    return redirect('/profile/'+user)
    

@login_required(login_url='login')
def profile(request,username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_posts = Post.objects.filter(user=user)
    user_total_posts = len(user_posts)
    followers = len(Following.objects.filter(user=user.username))
    following =  len(Following.objects.filter(follower=user.username))

    if Following.objects.filter(follower=request.user.username, user=username).first():
        text = 'Unfollow'
    else:
        text = 'Follow'



    print(followers, following)

    context = {
        'profile': user_profile,
        'user_posts': user_posts,
        "user_total_posts": user_total_posts,
        'followers': followers,
        'following': following,
        'text': text
    }

    return render(request, 'profile.html', context)


@login_required(login_url='login')
def like(request): 
    post_id = request.GET.get('post_id')
    username = request.user.username
    post = Post.objects.get(post_id=post_id)

    user_liked_post = PostLikes.objects.filter(username=username, post_id=post_id).first()

    if user_liked_post == None:
        like_post = PostLikes.objects.create(username=username, post_id=post_id)
        like_post.save()

        post.likes = post.likes+1

        post.save()

        return redirect('/')
    
    user_liked_post.delete()
    post.likes = post.likes-1

    post.save()
    
    return redirect('/')

@login_required(login_url='login')
def upload_post(request):
    if request.method != 'POST':
        return redirect('/')
    image = request.FILES.get('post_image')
    caption = request.POST.get('caption')
    user = request.user.username

    post = Post.objects.create(user=user, caption=caption, image=image)
    post.save()

    return redirect('/')

@login_required(login_url='login')
def account_settings(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('profile_image') == None:
            image = user_profile.user_profile_image
            location = request.POST.get('location')
            about_user = request.POST.get('about')

            user_profile.user_profile_image = image
            user_profile.user_location = location
            user_profile.user_bio = about_user

            user_profile.save();
        if request.FILES.get('profile_image') != None:
            image = request.FILES.get('profile_image')
            location = request.POST.get('location')
            about_user = request.POST.get('about')

            user_profile.user_profile_image = image
            user_profile.user_location = location
            user_profile.user_bio = about_user

            user_profile.save();
        return redirect('/account/settings')

    else:
         return render(request, 'setting.html', {'user_profile': user_profile})


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.info(request, 'Passwords do not much')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'There is already user with that email')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'That username is already taken')
            return  redirect('signup')

        user = User.objects.create_user(username=username,email=email, password=password)

        user.save()

        auth_user = auth.authenticate(username=username, password=password)

        auth.login(request, auth_user)

        current_user = User.objects.get(username=username)

        current_user_profile = UserProfile.objects.create(user=current_user)

        current_user_profile.save();

        return redirect('/account/settings')
        
       
    else:
         return render(request, 'signup.html')

def user_login(request):

    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is None:
            messages.info(request, 'There is no user with that credentials')
            return redirect('login')
        
        auth.login(request, user)
        
        return redirect('/')
    else:
        return render(request, 'signin.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

