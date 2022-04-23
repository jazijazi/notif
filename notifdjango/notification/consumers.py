from django.contrib.auth.models import User
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

import urllib.parse as urlparse
import json

from .models import Notification, Group



class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        self.all_user_groups = []

        #get query strings from url
        query = self.scope['query_string']
        params = urlparse.parse_qs(query.decode('UTF-8'))
        group_name = params.get('group_name' , [None])[0] #values come in arry

        await self.accept()

        #add to all group
        await self.channel_layer.group_add(
            f'all',
            self.channel_name
        )
        thisgroup = await self.change_group_num_active('all' , 'inc') #change num_active in db
        await self.group_change_number(thisgroup.name , thisgroup.num_active) #send changed num_active realtime

        if self.user.is_authenticated:
            #add to self user group
            await self.channel_layer.group_add(
                f'{self.user.username}',
                self.channel_name
            )
            #add to admin group
            if self.user.is_staff:
                await self.channel_layer.group_add(
                    f'admin',
                    self.channel_name
                )
                thisgroup = await self.change_group_num_active('admin' , 'inc') #change num_active in db
                await self.group_change_number(thisgroup.name , thisgroup.num_active) #send changed num_active realtime

        #add to group_name <come with url from group.html page>
        if group_name:
            await self.channel_layer.group_add(
                f'{group_name}',
                self.channel_name
            )
            group = await self.change_group_num_active(group_name , 'inc') #change num_active in db
            await self.group_change_number(group.name , group.num_active) #send changed num_active realtime

    async def receive_json(self, content, **kwargs):
        if content:
            if content['type'] == 'ack_message':
                thisnotification = await self.get_notification(content['id']) #get notification by id
                if thisnotification:
                    await self.add_seen_count(thisnotification.id) #rc?

    async def disconnect(self, code=None):
        for group in self.all_user_groups:
            await self.channel_layer.group_discard(group , self.channel_name) #disconnect from this group
            thisgroup = await self.change_group_num_active(group , 'dec') # increace num_active for this group in db
            await self.group_change_number(thisgroup.name , thisgroup.num_active) #change group active number realtime
        self.all_user_groups = []


    async def chat_notify(self , data):
        if data['sender_user_id'] != self.scope['user'].id: #dont send for hisself
            await self.send_json(data)

    async def group_change_active_num(self , data):
        await self.send_json(data)

    async def group_change_number(self , group_name , num_active):
        await self.channel_layer.group_send(
            'all',
            {
                'type':'group_change_active_num',
                'data':{
                    'group_name': group_name ,
                    'num': num_active
                }
            }
        )


    @database_sync_to_async
    def get_notification(self , id):
        try:
            noti = Notification.objects.get(pk=id)
            return noti
        except Notification.DoesNotExist:
            return None

    @database_sync_to_async
    def add_seen_count(self , id):
        try:
            noti = Notification.objects.get(pk=id)
            noti.seenCounts += 1
            noti.save()
        except Notification.DoesNotExist:
            return None

    @database_sync_to_async
    def change_group_num_active(self , group_name , change):
        try:
            group = Group.objects.get(name=group_name)
            if change.lower() == 'inc':
                group.num_active += 1
                self.all_user_groups.append(group_name) #add
            elif change.lower() == 'dec':
                group.num_active -= 1
                #self.all_user_groups.remove(group_name) #remove
            group.save()
            return group
        except Notification.DoesNotExist:
            return None





class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user'] #get user
        self.target_user = await self.get_target_user(self.scope['url_route']['kwargs']['targetUser']) #get tagetUser username from url
        
        
        if self.target_user:
            #add user to self group
            await self.channel_layer.group_add(f'{self.user.username}' , self.channel_name)
            #connect
            await self.accept()
        else:
            # Accept and then reject to send custom close_code (otherwise JUST send 1006 code)
            await self.accept()
            await self.close(code=4004)


    async def receive_json(self, content, **kwargs):
        if(content):
            if content['type'] == 'message':
                #send message to target user
                await self.send_to_user_layer(content=content['content'] ,
                            sender=self.user.username , target=self.target_user)
                #create a new notification
                new_notif = await self.create_new_notification(title='New Message' , content=f'You Have New Message from {self.user.username}')
                #send notification to target user
                # if new_notif:
                #     await self.channel_layer.group_send(
                #         f'{self.target_user}',
                #         {
                #             'type':'chat.notify',
                #             'notification':{
                #                 'id':new_notif.id,
                #                 'title':new_notif.title,
                #                 'content':new_notif.content
                #             },
                #             'sender_user_id' : self.user.id
                #         }
                #     )

    async def disconnect(self, code=None):
        await self.channel_layer.group_discard(f'{self.user.username}' , self.channel_name) #disconnect


    @database_sync_to_async
    def get_target_user(self , targetUser):
        try:
            return User.objects.get(username=targetUser)
        except User.DoesNotExist:
            return None

    async def send_to_user(self , data):
        await self.send_json(data)

    async def send_to_user_layer(self , content , sender , target):
        await self.channel_layer.group_send(
            f'{target}',
            {
                'type':'send_to_user',
                'data':{
                    'content': content ,
                    'sender': sender
                }
            }
        )

    @database_sync_to_async
    def create_new_notification(self , title , content):
        try:
            new_notif = Notification(title=title, content=content ,creator=self.user ,group=Group.objects.get(id=1))
            new_notif.save()
            return new_notif
        except:
            return None