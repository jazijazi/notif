from django.shortcuts import render , HttpResponse , get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification , Group
from .forms import NotificationForm

def home(request):
    groups = Group.objects.exclude(Q(name='all') | Q(name='admin'))
    return render(request , template_name='notification/home.html', context={'groups' : groups})


def addtogroup(request , group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return render(request, 'chat/404.html')
    
    return render(request , template_name='notification/group.html', context={'group' : group})


class NotificationCreateView(LoginRequiredMixin , CreateView):
    login_url = reverse_lazy('admin:login')
    model = Notification
    form_class = NotificationForm
    template_name = 'notification/notificationform.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = form.save()

        send_notification(response.group.name ,response.id ,response.title ,response.content , self.request.user.id)

        return super().form_valid(form)


def send_notification(group_name , id , title , content , user_id):
    channel_layer = get_channel_layer()
    channel_layer
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type' : 'chat.notify',
            'notification':{
                'id':id,
                'title':title,
                'content':content
            },
            'sender_user_id' : user_id
        }
    )