from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                        UserPassesTestMixin)
# LoginRequiredMixin -> makes it possible to be redirected when tried to go to some URL when logged out
# UserPassesTestMixin -> used for avoiding tries of editing a post created by other users
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
# ^ a class based view


# handles the traffic from the home page of our app
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>/html
    # ^ specifying which existing template to use
    context_object_name = 'posts'
    # ^ is used coz we wanted to change the default name of 
    # the variable that we would be loopping over in the template 
    ordering = ['-date_posted']
    # ^ would order the posts from newest to oldest
    paginate_by = 5

# when we want to see a specified user's posts
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>/html
    # ^ specifying which existing template to use
    context_object_name = 'posts'
    # ^ is used coz we wanted to change the default name of 
    # the variable that we would be loopping over in the template 
    paginate_by = 5
    
    # modifying the query set that this list view 
    # returns
    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        # ^ getting the username from the URL| kwargs -> query parameters
        return Post.objects.filter(author = user).order_by('-date_posted')
    #                                                        ^ would order the posts from newest to oldest

class PostDetailView(DetailView):
    model = Post
    
# a view with a form where we create a new post 
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        # setting up the author on the form
        return super().form_valid(form)
        # ^ validating the form
        # ^ would run anyway but we are saying that it would run after specifying the author

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # a function that our user 
    # passes test mixin will run in order to see 
    # if our user passes a certain test condition
    def test_func(self):
        post = self.get_object()
        # The UpdateView's ^ method for getting the post that we are trying to update
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post       
    success_url ='/'
    # ^ we go to "home" after deleting 
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})







