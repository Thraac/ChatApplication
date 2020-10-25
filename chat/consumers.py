import asyncio, json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):

    # when the socket connects
    async def websocket_connect(self, event):

        await self.send({
            "type": "websocket.accept",
        })
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)
        chat_room = f"thread_{thread_obj.id}"

        self.thread_obj = thread_obj
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name,
        )

    # when the socket gets a message
    async def websocket_receive(self, event):

        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            user = self.scope['user']
            username = 'none'
            if user.is_authenticated:
                username=user.username
            myReponse = {
                'message': msg,
                'username': username,
            }
            await self.create_chat_message(user, msg)

            # broadcast the message to send
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myReponse),
                }
            )

    async def chat_message(self, event):
        #send the message being broadcast
        await self.send ({
                "type": "websocket.send",
                "text": event['text'],
        })


    # when the socket disconnects
    async def websocket_disconnect(self, event):
        print("disconnect", event)

    # returns the thread
    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    # creates the chat message
    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)