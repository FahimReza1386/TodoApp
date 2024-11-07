from django.test import TestCase
import pytest  # type: ignore
from rest_framework.test import APIClient # type: ignore
from django.urls import reverse
from accounts.models import User

@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def get_user():
    user= User.objects.create_user(email="Fahim@gmail.com" , password = "Fahim2684")
    return user

@pytest.mark.django_db
class TestTodoApi:

    def test_get_task_response_200_status(self , api_client , get_user):
        url = reverse('TodoList:api-v1:Tasks-list')
        user=get_user
        api_client.force_login(user=user)
        response = api_client.get(url)
        assert response.status_code == 200 , response.content


    def test_create_task_response_201_status(self , api_client , get_user):
        url = reverse('TodoList:api-v1:Tasks-list')
        user = get_user
        api_client.force_login(user=user)
        data = {
            "user":user.id,
            "Text" : "test",
        }
        print("Request data:", data)  
        print("User ID:", user.id) 
        response = api_client.post(url , data)
        assert response.status_code == 201 , response.content


    def test_delete_task_response_204_status(self , api_client , get_user):
        user = get_user
        api_client.force_login(user=user)
       
        create_url = reverse('TodoList:api-v1:Tasks-list')
        data = {
            "Text" : "test",
        }

        create_response = api_client.post(create_url , data)
        # Created The Task
        assert create_response.status_code == 201 , create_response.content

        task_id = create_response.data['id']

        get_response = api_client.get(reverse('TodoList:api-v1:Tasks-detail' ,args=[task_id]))
        # Get The Task
        assert get_response.status_code == 200 , get_response.content

        del_url = reverse('TodoList:api-v1:Tasks-detail' ,args=[task_id])
        response = api_client.delete(del_url)
        # Delete The Task
        assert response.status_code == 204 , response.content

        get_response_after_delete = api_client.get(reverse('TodoList:api-v1:Tasks-detail', args=[task_id]))
        # Check The Delete Task
        assert get_response_after_delete.status_code == 404 , response.content


    def test_put_task_response_200_status(self , api_client , get_user):
        user = get_user
        api_client.force_login(user=user)
       
        create_url = reverse('TodoList:api-v1:Tasks-list')
        data = {
            "Text" : "test",
        }

        create_response = api_client.post(create_url , data)
        # Created The Task
        assert create_response.status_code == 201 , create_response.content
        task_id = create_response.data['id']

        get_response = api_client.get(reverse('TodoList:api-v1:Tasks-detail' ,args=[task_id]))
        # Get The Task
        assert get_response.status_code == 200 , get_response.content

        put_url = reverse('TodoList:api-v1:Tasks-detail' , args=[task_id])
        data={
            "Text" : "test2",
        }
        put_response = api_client.put(put_url , data)
        assert put_response.status_code == 200 , put_response



    def test_patch_task_response_200_status(self , api_client , get_user):
        user = get_user
        api_client.force_login(user=user)
       
        create_url = reverse('TodoList:api-v1:Tasks-list')
        data = {
            "Text" : "test",
        }

        create_response = api_client.post(create_url , data)
        # Created The Task
        assert create_response.status_code == 201 , create_response.content
        task_id = create_response.data['id']

        get_response = api_client.get(reverse('TodoList:api-v1:Tasks-detail' ,args=[task_id]))
        # Get The Task
        assert get_response.status_code == 200 , get_response.content

        patch_url = reverse('TodoList:api-v1:Tasks-detail' , args=[task_id])
        data={
            "Text" : "test2",
        }
        patch_response = api_client.patch(patch_url , data)
        assert patch_response.status_code == 200 , patch_response

