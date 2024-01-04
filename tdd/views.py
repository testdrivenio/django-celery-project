from django.db import transaction
from django.shortcuts import render
from functools import partial

from tdd.forms import MemberForm
from tdd.tasks import generate_avatar_thumbnail


@transaction.atomic
def member_signup(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            # save form data and image
            instance = form.save()
            transaction.on_commit(partial(generate_avatar_thumbnail.delay, instance.pk))
            return render(request, 'member_signup_success.html', {'member': instance})
    else:
        form = MemberForm()

    return render(request, 'member_signup.html', {'form': form})
