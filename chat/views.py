from .forms import UserCreation
from django.http import JsonResponse
from django.contrib.auth import login
from .models import Message, UserProfile
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import get_object_or_404, render
from django.views import generic


from .forms import CommentForm
from .models import Post

# Create your views here.

# ---------------------------------------------------------------------------- #
#                             Function Based Views                             #
# ---------------------------------------------------------------------------- #

# --------------------------- Creating User Profile -------------------------- #
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserCreation  # Import your user creation form from your app

def signup(request):
    if request.method == 'POST':
        userform = UserCreation(request.POST)
        if userform.is_valid():
            user = userform.save(commit=True)

            # Log in the user
            login(request, user)

            # Redirect to the desired page (e.g., the inbox)
            return redirect('chat:inbox', username=user.username)

        else:
            # Handle form errors here
            errors = {}
            for field in userform:
                for error in field.errors:
                    errors[field.name] = error
            return JsonResponse({"status": False, "errors": errors})

    else:
        userform = UserCreation()

    return render(request, 'auth/signup.html', {'form': userform})


# ---------------------------------------------------------------------------- #
#                               Class based Views                              #
# ---------------------------------------------------------------------------- #

# ----------------------- Inbox/messages/users list ----------------------- #

class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat/messages_list.html'
    context_object_name = 'messages'
    login_url = '/login/'

    def get_queryset(self):
        user = self.request.user
        # Fetch messages involving the current user
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)


# --------------------------------- Chat view -------------------------------- #
class InboxView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'chat/inbox.html'
    login_url = '/login/'

    def get_object(self):
        username = self.kwargs.get("username")
        return UserProfile.objects.get(username=username)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        other_user = self.get_object()
        # Fetch messages between the two users
        messages = Message.objects.filter(sender=user, recipient=other_user) | Message.objects.filter(sender=other_user, recipient=user)
        context['messages'] = messages
        context['other_person'] = other_user
        context['you'] = user
        return context
    def post(self, request, *args, **kwargs):
        sender = request.user
        recipient_username = self.kwargs.get("username")
        recipient = UserProfile.objects.get(username=recipient_username)
        message_text = request.POST.get('message')

        if message_text:
            Message.objects.create(sender=sender, recipient=recipient, message=message_text)

        return redirect('chat:inbox', username=recipient_username)

# -------------------------------- Users list -------------------------------- #
class UserListsView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'chat/users_list.html'
    context_object_name = 'users'
    login_url = '/login/'

    def get_queryset(self):
        return UserProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 3
    login_url = '/blog/'



def post_detail(request, slug):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )
