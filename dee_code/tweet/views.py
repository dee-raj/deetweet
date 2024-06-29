from .models import Tweet
from .forms import TweetForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

# Create your views here.

def index(request):

   return render(request, 'index.html')

def tweet_list(req):
   tweets = Tweet.objects.all().order_by('-created_at')

   return render(req, 'tweet_list.html', {'tweets':tweets})

@login_required
def tweet_create(req):
   if req.method == "POST":
      form = TweetForm(req.POST, req.FILES)
      if form.is_valid():
         tweet = form.save(commit=False)
         tweet.user = req.user
         tweet.save()

         return redirect('tweet_list')
   else:
      form = TweetForm()
   return render(req, 'tweet_form.html', {'form':form})

@login_required
def tweet_edit(req, tweet_id):
   tweet=get_object_or_404(Tweet, pk=tweet_id, user=req.user)
   if req.method == 'POST':
      form = TweetForm(req.POST, req.FILES, instance=tweet)
      if form.is_valid():
         tweet = form.save(commit=False)
         tweet.user = req.user
         tweet.save()

         return redirect('tweet_list')
   else:
      form = TweetForm(instance=tweet)
   return render(req, 'tweet_form.html', {'form':form})

@login_required
def tweet_delete(req, tweet_id):
   tweet=get_object_or_404(Tweet, pk=tweet_id, user=req.user)
   if req.method == 'POST':
      tweet.delete()

      return redirect('tweet_list')
   return render(req, 'tweet_confirm_delete.html', {'tweet':tweet})


def register(req):
   if req.method == 'POST':
      form = UserCreationForm(req.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.set_password(form.cleaned_data['password1'])
         user.save()
         login(req, user)

         return redirect('tweet_list')
   else:
      form = UserCreationForm()
   return render(req, 'registration/register.html', {'form':form})

# views.py

def search_tweets(request):
   query = request.GET.get('q')
   if query:
      results = Tweet.objects.filter(Q(text__icontains=query))
   else:
      results = None
   return render(request, 'search_results.html', {'results': results, 'query': query})
