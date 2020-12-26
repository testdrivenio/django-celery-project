from django.contrib.auth.forms import UserCreationForm

from tdd.models import Member


class MemberForm(UserCreationForm):

    class Meta:
        model = Member
        fields = ('username', 'email', 'password1', 'password2', 'avatar')
