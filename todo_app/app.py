from flask import Flask, appcontext_popped, render_template, redirect, request
#from data.session_items import get_items, add_item
from flask_config import Config
from dotenv import load_dotenv, find_dotenv
from data.trello_items import *

def create_app():

   file_path = find_dotenv('.env')
   load_dotenv(file_path)

   token = os.getenv('TRELLO_TOKEN')
   key = os.getenv('TRELLO_KEY')
   url = "https://api.trello.com/1/"
   url_member = url + "members/carispang"
   query_string = {"key" : key, "token" : token}

   app = Flask(__name__)
   app = Flask(__name__, template_folder='templates')
   app.config.from_object(Config())

   @app.route('/', methods = ['GET', 'POST'])
   def createUI():
      data_board_cards = get_data_board_cards(url, query_string)
      data_board_lists = get_board_lists(url, query_string)
      list_id = get_list('To Do', data_board_lists)
      todo_cards = get_cards_on_list(url, list_id, query_string)
      if request.method == 'POST':
         if not request.form.get('complete_button'):
            card_name = request.form.get('submit_button') 
            create_card(url, list_id, card_name, key, token)
            todo_cards.append({"name": card_name})
         else:
            data_board_lists = get_board_lists(url, query_string)
            done_ID = get_list('Done', data_board_lists)
            complete_method(data_board_cards, url, done_ID, key, token)
            todo_cards = get_cards_on_list(url, list_id, query_string)
      return render_template('index.html', ls = todo_cards)

   @app.route('/ExerciseFive')
   def exercise_five():
      data_board_cards = get_data_board_cards(url, query_string)
      card_info = get_card_info(data_board_cards)
      list_info = get_list_info(data_board_cards)
      new_list = get_listForLoop(card_info, list_info)
      cardNames = get_card_names(data_board_cards)
    
      return render_template('index_3.html', ls = new_list)

   app.run()

create_app()
