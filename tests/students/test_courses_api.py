import pytest
import os
from random import randint
from rest_framework.test import APIClient
from tests.fixtures.fixture_data import *
from django.conf import settings

client = APIClient()


class TestCourseModel:
    @pytest.mark.django_db(transaction=True)
    def test_courses_urls(self, course):
        response = client.get(f'/api/v1/courses/{course.id}/')
        assert response.status_code == 200, f'Status code {response.status_code} from ' \
                                            f'url: \'/api/v1/courses/{course.id}/\''
        assert response.data['id'] == course.id, f'Course id must be {course.id}, not {response.data["id"]}'

    @pytest.mark.django_db(transaction=True)
    def test_courses_list(self, courses):
        response = client.get(f'/api/v1/courses/')
        assert response.status_code == 200, f'Status code {response.status_code} from ' \
                                            f'url: \'/api/v1/courses/\''
        assert len(response.data) == len(courses), f'It must be 10 instances in response.data!'

    @pytest.mark.django_db(transaction=True)
    def test_courses_list_filters_id(self, courses):
        random_id = [c.id for c in courses][randint(0, 9)]
        response = client.get(f'/api/v1/courses/?id={random_id}')
        assert response.status_code == 200, f'Status code {response.status_code} from ' \
                                            f'url: \'/api/v1/courses/?id={random_id}\''
        assert response.data[0]['id'] == random_id, f'Course id must be {random_id}, not {response.data["id"]}'

    @pytest.mark.django_db(transaction=True)
    def test_courses_list_filters_name(self, courses):
        random_name = [c.name for c in courses][randint(0, 9)]
        response = client.get(f'/api/v1/courses/?name={random_name}')
        assert response.status_code == 200, f'Status code {response.status_code} from ' \
                                            f'url: \'/api/v1/courses/?name={random_name}\''
        assert response.data[0][
                   'name'] == random_name, f'Course name must be {random_name}, not {response.data["name"]}'

    @pytest.mark.django_db(transaction=True)
    def test_course_create(self):
        fixture_path = os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'courses.json')
        with open(fixture_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        create_response = client.post('/api/v1/courses/', data=data[0])

        assert create_response.status_code == 201, f'Status code {create_response.status_code} from ' \
                                                   f'url: \'/api/v1/courses/\''

    @pytest.mark.django_db(transaction=True)
    def test_course_update(self, course):
        original_response = client.get(f'/api/v1/courses/{course.id}/')
        assert original_response.status_code == 200, f'Status code {original_response.status_code} from ' \
                                                     f'url: \'/api/v1/courses/{course.id}\''
        update_response = client.put(f'/api/v1/courses/{course.id}/', data={'name': 'New name'})
        assert update_response.status_code == 200, f'Status code {update_response.status_code} from ' \
                                                   f'url: \'/api/v1/courses/{course.id}\''
        updated_response = client.get(f'/api/v1/courses/{course.id}/')
        assert updated_response.data != original_response.data, 'New data is the same as original!'

    @pytest.mark.django_db(transaction=True)
    def test_delete_course(self, course):
        retrieve_response = client.get(f'/api/v1/courses/{course.id}/')
        assert retrieve_response.status_code == 200, f'Status code {retrieve_response.status_code} from ' \
                                                     f'url: \'/api/v1/courses/{course.id}\''
        delete_response = client.delete(f'/api/v1/courses/{course.id}/')
        assert delete_response.status_code == 204, f'Status code {retrieve_response.status_code} from ' \
                                                   f'url: \'/api/v1/courses/{course.id}\''
        check_delete_response = client.get(f'/api/v1/courses/{course.id}/')
        assert check_delete_response.status_code == 404, f'Status code {check_delete_response.status_code} from ' \
                                                         f'url: \'/api/v1/courses/{course.id}\''
