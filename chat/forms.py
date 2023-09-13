from django.contrib.auth.forms import UserCreationForm
from django import forms


from .models import UserProfile
from .models import Comment


# ---------------------------------------------------------------------------- #
#                   creating a form to allow users to sign up                  #
# ---------------------------------------------------------------------------- #

# ----------------------------- USer signup form ----------------------------- #
class UserCreation(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'phone')

    def save(self, commit=True):
        user = super(UserCreation, self).save(commit=False)
        if commit:
            user.is_active = True
            user.save()

        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")

