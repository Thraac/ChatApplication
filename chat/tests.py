from django.test import TestCase
import unittest
from .models import ChatMessage, Thread, ThreadManager
from django.contrib.auth import get_user_model

User = get_user_model()


class TestChat(unittest.TestCase):
    testuser1 = None
    testuser2 = None

    def setUp(self):
        # testuser1 = User.objects.create_user(username='testuser1', password='123456')
        # testuser2 = User.objects.create_user(username='testuser2', password='123456')
        testuser1 = 'testuser1'
        testuser2 = 'testuser2'
        testmessage = ChatMessage.objects.create(user=self.testuser1, message="test")
        
    def test_message_made(self):
        message = ChatMessage.objects.get(pk=1)
        self.assertEqual(message.message, "test")

    def test_thread(self):
        thread = Thread.objects.get()
        self.assertNotEqual(thread.first, thread.second)
        self.assertEqual(thread.room_group_name, 'chat_1')
        self.assertEqual(thread.roomname, "Chat room between testuser1 and testuser2\n")