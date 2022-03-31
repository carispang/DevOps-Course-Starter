import sys
from data.trello_items import get_board_lists, get_list
import pytest
from _pytest.monkeypatch import monkeypatch
from dotenv import load_dotenv, find_dotenv
import requests
import os
print("Current working directory: {0}".format(os.getcwd()))
from app import create_app
import os

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
    token = os.getenv('TRELLO_TOKEN')
    key = os.getenv('TRELLO_KEY')
    board_ID = os.getenv('BOARD_ID')
    url = "https://api.trello.com/1/"
    query_string = {"key" : key, "token" : token}   
    # Replace call to requests.get(url) with our own function
    monkeypatch.setattr(requests, 'get', get_board_lists_stub)
    lists_stub = get_board_lists(url, query_string, board_ID)
    assert type(lists_stub) == list
    in_progress_data = get_list('In Progress', lists_stub)
    assert in_progress_data == 'TEST_ID_2'
    
class StubResponse():

    def __init__(self, fake_response_data):
        self.text = fake_response_data
        
def get_board_lists_stub(url, params):

    fake_response_data = '[{"id":"TEST_ID_1","name":"To Do","closed":"false","idBoard":"TEST_BOARD_1"},{"id":"TEST_ID_2","name":"In Progress","closed":"false","idBoard":"TEST_BOARD_2"},{"id":"TEST_ID_3","name":"Done","closed":"false","idBoard":"TEST_BOARD_3"}]'
    
    return StubResponse(fake_response_data)
