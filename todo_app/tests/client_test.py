import sys
from todo_app.data.trello_items import get_board_lists, get_list
import pytest
from dotenv import load_dotenv, find_dotenv
import requests
import os
print("Current working directory: {0}".format(os.getcwd()))
from todo_app.app import create_app
from todo_app.data.class_definitions import ViewModel

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_get_board_lists(client, monkeypatch):
    # Replace call to requests.get(url) with our own function
    monkeypatch.setattr(requests, 'get', get_board_lists_stub)
    home_page = client.get('/')
    assert home_page.status_code == 200
    #assert "do work" in home_page.data.decode()
    
class StubResponse():

    def __init__(self, fake_response_data):
        self.text = fake_response_data
        
def get_board_lists_stub(url, params):

    token = os.getenv('TRELLO_TOKEN')
    print(token)
    key = os.getenv('TRELLO_KEY')
    print(key)
    board_ID = os.getenv('BOARD_ID')
    print(board_ID)
    base_url = "https://api.trello.com/1/"
    query_string = {"key" : key, "token" : token}   
    print(url)
    if url == base_url +  "boards/" + board_ID + "/lists":
        fake_response_data = '[{"id":"TEST_ID_1","name":"To Do","closed":"false","idBoard":"TEST_BOARD_1"},{"id":"TEST_ID_2","name":"In Progress","closed":"false","idBoard":"TEST_BOARD_2"},{"id":"TEST_ID_3","name":"Done","closed":"false","idBoard":"TEST_BOARD_3"}]'
    if url == base_url + "lists/" + 'TEST_ID_1' + "/cards":
        fake_response_data = '[{"name": "do work"}, {"name": "do more work"}]'
    if url == base_url + "boards/" + board_ID + "/cards":
        fake_response_data = '[{"id":"CARD_ID_1"}, {"id":"CARD_ID_2"}, {"id":"CARD_ID_3"}]'   
    return StubResponse(fake_response_data)
