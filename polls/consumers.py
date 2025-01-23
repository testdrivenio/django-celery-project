import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from celery.result import AsyncResult


def get_task_info(task_id):
    """
    return task info according to the task_id
    """
    task = AsyncResult(task_id)
    state = task.state

    if state == 'FAILURE':
        error = str(task.result)
        response = {
            'state': state,
            'error': error,
        }
    else:
        response = {
            'state': state,
        }
    return response


def notify_channel_layer(task_id):
    """
    This function would be called in Celery task.

    Since Celery now still not support `asyncio`, so we should use async_to_sync
    to make it synchronous

    https://channels.readthedocs.io/en/stable/topics/channel_layers.html#using-outside-of-consumers
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        task_id,
        {'type': 'update_task_status', 'data': get_task_info(task_id)}
    )


class TaskStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']

        await self.channel_layer.group_add(
            self.task_id,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps(get_task_info(self.task_id)))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.task_id,
            self.channel_name
        )

    async def update_task_status(self, event):
        data = event['data']

        await self.send(text_data=json.dumps(data))
