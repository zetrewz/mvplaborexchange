from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404

from chat.models import ChatMessage
from service.models import Application
from service.utils import is_worker


# @login_required
# def chat_room(request, application_id):
#     application = Application.objects.get(
#         id=application_id)
#     messages = ChatMessage.objects.filter(user__in=[
#         application.vacancy.user, application.resume.user],
#         room_group_name=f'chat_{application.id}')
#
#     context = {'application': application, 'messages': messages}
#     return render(request, 'chat/room.html', context)
#
#
# @login_required
# def holl(request):
#     if is_worker(request.user):
#         try:
#             applications = Application.objects.filter(
#                 resume=request.user.resume)
#         except:
#             applications = []
#     else:
#         try:
#             applications = Application.objects.filter(vacancy__user=request.user)
#         except Application.DoesNotExist:
#             applications = []
#
#     context = {'applications': applications}
#     return render(request, 'chat/holll.html', context)


@login_required
def chat_room(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    users_in_chat = [application.vacancy.user, application.resume.user]
    messages = ChatMessage.objects.filter(user__in=users_in_chat,
                                          room_group_name=f'chat_{application.id}')

    context = {'application': application, 'messages': messages}
    return render(request, 'chat/room.html', context)


@login_required
def holl(request):
    try:
        if is_worker(request.user):
            applications = Application.objects.filter(resume=request.user.resume)
        else:
            applications = Application.objects.filter(vacancy__user=request.user)
    except ObjectDoesNotExist:
        applications = []
    context = {'applications': applications}

    return render(request, 'chat/holll.html', context)

