#!
from flask import Flask, appcontext_popped, render_template, redirect, request
from todo_app.flask_config import Config
from dotenv import load_dotenv, find_dotenv
from todo_app.data.trello_items import *

def create_app():

   file_path = find_dotenv('.env')
   load_dotenv(file_path)

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
      todo_cards = get_cards_on_list(url, list_id, query_string)
      if request.method == 'POST':
         if not request.form.get('complete_button'):
            card_name = request.form.get('submit_button') 
            create_card(url, list_id, card_name, key, token)
            todo_cards.append({"name": card_name})
         else:
            data_board_lists = get_board_lists(url, query_string, board_ID)
            done_ID = get_list('Done', data_board_lists)
            complete_method(data_board_cards, url, done_ID, key, token)
            todo_cards = get_cards_on_list(url, list_id, query_string)
      return render_template('index.html', ls = todo_cards)

   @app.route('/ExerciseFive')
   def exercise_five():
      data_board_cards = get_data_board_cards(url, query_string, board_ID)
      card_info = get_card_info(data_board_cards)
      data_board_lists = get_board_lists(url, query_string, board_ID)
      list_info = get_list_info(data_board_cards, data_board_lists)
      new_list = get_listForLoop(card_info, list_info)
      cardNames = get_card_names(data_board_cards)
    
      return render_template('index_3.html', ls = new_list)

   return app

#create_app()
