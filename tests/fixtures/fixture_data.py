import pytest
import json
from model_bakery import baker
from students.models import Course


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='TestUser', password='1234567')


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def course():
    return baker.make('students.Course')


@pytest.fixture
def courses():
    return baker.make('students.Course', _quantity=10)


@pytest.fixture
def student():
    return baker.make('students.Student')


@pytest.fixture
def students():
    return baker.make('students.Student', _quantity=10)


@pytest.fixture
def courses_json():
    with open('courses.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    courses = Course.objects.bulk_create([Course(**item_data) for item_data in data])
    return courses