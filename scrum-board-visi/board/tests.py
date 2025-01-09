from django.test import TestCase
from board.models import Board, BoardUser
from user.models import User
from django.utils import timezone

"""Models Tests"""
class BoardUserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='password'
        )

    def test_board_str_method(self):
        self.assertEqual(str(self.user), 'testuser@example.com')

    def test_board_user_creation(self):
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)


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

"""serializer models"""
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from board.serializer import BoardSerializer
from board.models import Board
from user.models import User
from django.utils import timezone


class BoardSerializerTest(APITestCase):

    def setUp(self):
        # Tworzenie przykładowego użytkownika i tablicy
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='password'
        )
        self.due_date = timezone.now() + timezone.timedelta(days=7)
        self.board_data = {
            'name': 'Test Board',
            'description': 'This is a test board.',
            'due_date': self.due_date
        }
        self.board = Board.objects.create(**self.board_data)


    def test_board_serializer_valid(self):
        """Test, czy serializer poprawnie serializuje dane tablicy"""
        board = Board.objects.create(
            name='Test Board',
            description='This is a test board.',
            due_date=self.due_date.date()  # Użycie .date() z datetime
        )
        serializer = BoardSerializer(board)
        # Sprawdzamy, czy dane w serializerze odpowiadają danym w obiekcie
        self.assertEqual(serializer.data['name'], board.name)
        self.assertEqual(serializer.data['description'], board.description)
        self.assertEqual(serializer.data['due_date'], board.due_date.strftime('%d %B %Y'))

    def test_board_serializer_invalid_due_date(self):
        """Test, czy serializer poprawnie obsługuje nieprawidłową datę"""
        invalid_data = {
            'name': 'Test Board',
            'description': 'This is a test board.',
            'due_date': 'invalid date'
        }
        serializer = BoardSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_board_serializer_create(self):
        """Test, czy serializer poprawnie deserializuje dane do modelu"""
        data = {
            'name': 'New Board',
            'description': 'This is a new test board.',
            'due_date': timezone.now().date()
        }
        serializer = BoardSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        board = serializer.save()
        self.assertEqual(board.name, data['name'])
        self.assertEqual(board.description, data['description'])
        # Porownanie stringow
        self.assertEqual(str(board.due_date), str(data['due_date']))

    def test_board_serializer_missing_field(self):
        """Test, czy serializer zwróci błąd, gdy brakuje obowiązkowego pola"""
        data = {
            'description': 'Test board with missing name',
            'due_date': timezone.now() + timezone.timedelta(days=7)
        }
        serializer = BoardSerializer(data=data)
        self.assertFalse(serializer.is_valid())  # Dane będą niepoprawne
        self.assertIn('name', serializer.errors)  # Powinno zwrócić błąd dla pola