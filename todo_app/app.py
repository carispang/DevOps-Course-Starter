from flask import Flask, appcontext_popped, render_template, redirect, request
from todo_app.flask_config import Config
from dotenv import load_dotenv, find_dotenv
from todo_app.data.trello_items import *
from todo_app.data.class_definitions import ViewModel
import os

file_path = find_dotenv('.env')
load_dotenv(file_path, override=True)

def create_app():

   token = os.getenv('TRELLO_TOKEN')
   key = os.getenv('TRELLO_KEY')
   board_ID = os.getenv('BOARD_ID')
   url = "https://api.trello.com/1/"
   query_string = {"key" : key, "token" : token}

   app = Flask(__name__)
   app.config.from_object(Config())

   @app.route('/', methods = ['GET', 'POST'])
   def createUI():
      data_board_cards = get_data_board_cards(url, query_string, board_ID)
      data_board_lists = get_board_lists(url, query_string, board_ID)
      list_id = get_list('To Do', data_board_lists)
      todo_cards = get_cards_on_list_class(url, list_id, query_string, data_board_lists)
      if request.method == 'POST':
         if not request.form.get('complete_button'):
            card_name = request.form.get('submit_button') 
            create_card(url, list_id, card_name, key, token)
            todo_cards = get_cards_on_list_class(url, list_id, query_string, data_board_lists)
         else:
            data_board_lists = get_board_lists(url, query_string, board_ID)
            done_ID = get_list('Done', data_board_lists)
            complete_method(data_board_cards, url, done_ID, key, token)
            todo_cards = get_cards_on_list_class(url, list_id, query_string, data_board_lists)
      return render_template('index.html', ls = todo_cards)

   return app


