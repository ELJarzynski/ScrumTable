from django.test import TestCase
from ..models import Board, BoardUser
from user.models import User
from django.utils import timezone


class BoardUserTest(TestCase):

    def setUp(self):
        # Provide email, first_name, and last_name when creating the user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='password'
        )

    def test_board_str_method(self):
        # Your test logic here
        self.assertEqual(str(self.user), 'testuser@example.com')

    def test_board_user_creation(self):
        # Your test logic here
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

from django.utils import timezone

class BoardTest(TestCase):

    def setUp(self):
        self.due_date = timezone.now() + timezone.timedelta(days=7)

    def test_board_creation(self):
        # Tworzenie tablicy
        board = Board.objects.create(
            name="Test Board",
            description="This is a test board.",
            due_date=self.due_date
        )

        # Testowanie właściwości tablicy
        self.assertEqual(board.name, "Test Board")
        self.assertEqual(board.description, "This is a test board.")
        self.assertEqual(board.due_date, self.due_date)  # Porównanie tylko daty
        self.assertIsNotNone(board.create_date)  # create_date powinno zostać ustawione automatycznie
        self.assertEqual(str(board), "Test Board")  # Metoda __str__ powinna zwrócić nazwę
