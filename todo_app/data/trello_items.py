# -*- coding: utf-8 -*-
from telnetlib import STATUS
from turtle import update
import requests
import os
import json
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app = Flask(__name__, template_folder='../templates')

os.environ['TRELLO_TOKEN'] = "9cc5e1de416f419f2f1b3f5effda1d8bd01fde1e2f7291d656629b05633c708c"
token = os.getenv('TRELLO_TOKEN')

os.environ['TRELLO_KEY'] = "d59b47daa0229f97284d969ff1c3fd84"
key = os.getenv('TRELLO_KEY')

url = "https://api.trello.com/1/"

url_member = url + "members/carispang"
query_string = {"key" : key, "token" : token}

def get_board_lists(url, query_string):
    url_board_lists = url + "boards/" + "w71XY2GF" + "/lists"
    response_board_lists = requests.request("GET", url_board_lists, params = query_string)
    data_board_lists = json.loads(response_board_lists.text)
    return(data_board_lists)

def get_list(name, data_board_lists):
    for list in data_board_lists:
        if list['name'] == name:
            todoId = list['id']
            return todoId

def createCard(url, list_id, card_name):
    url = url + "cards"
    query_string = {"name": card_name, "idList": list_id, "key": key, "token": token}
    response = requests.request("POST", url, params=query_string)
    card_id = response.json()["id"]
    return card_id

def update_list(url, card_ID, done_ID):
    query_string = {"idList": done_ID, "key": key, "token": token}
    url_board_cards = url + "cards/" + card_ID
    response = requests.request("PUT", url_board_cards, params=query_string)

def getCardNames(data_board_cards):
    cardNames = []
    for card in data_board_cards:
        cardNames.append({"name": card['name']})
    return cardNames

def getCardIDFromName(cardName, data_board_cards):

    for card in data_board_cards:
        nameCard = card['name']
        if cardName == nameCard:
            cardID = card['id']
            return(cardID)

def get_data_board_cards(url, query_string):

    url_board_cards = url + "boards/" + "w71XY2GF" + "/cards"
    response_board_cards = requests.request("GET", url_board_cards, params = query_string)
    data_board_cards = json.loads(response_board_cards.text)    
    return data_board_cards
def get_list_name(ID, data_board_lists):
    for list in data_board_lists:
        if list['id'] == ID:
            list_name = list['name']
            return list_name
    
def get_card_info(data_board_cards):
    card_info = []
    for card in data_board_cards:
        card_info.append({"name": card['name'], "id": getCardIDFromName(card['name'], data_board_cards)})
    return card_info


def get_list_info(data_board_cards):
    list_info = []
    for j in data_board_cards:
        list_info.append({"name" : get_list_name(j['idList'], data_board_lists)})
    return list_info


def get_listForLoop(card_info, list_info):

    new_list = []
    index = 0
    for i in card_info:
        item = ItemClass.from_trello_card(card = card_info[index], list = list_info[index])
        new_list.append(item)
        index += 1
    return new_list

data_board_cards = get_data_board_cards(url, query_string)
data_board_lists = get_board_lists(url, query_string)
todo_ID = get_list('To Do', data_board_lists)
in_progress_ID = get_list('In Progress', data_board_lists)
done_ID = get_list('Done', data_board_lists)
task_4_ID = createCard(url, todo_ID, "task 4")  

@app.route('/', methods = ['GET', 'POST'])
def createUI():
    card_names = getCardNames(data_board_cards)
    if request.method == 'POST':
        card_ID = getCardIDFromName(str(request.form['submit_button']), data_board_cards)
        update_list(url, card_ID, done_ID)
        return redirect(request.url)
    return render_template('index_2.html', ls = card_names)

class ItemClass():

  def __init__(self, id, title, status):
        self.id = id
        self.status = status
        self.title = title

  @classmethod
  def from_trello_card(cls, card, list):
      return cls(card['id'], card['name'], list['name'])


@app.route('/ExerciseFive')
def exercise_five():

    card_info = get_card_info(data_board_cards)
    list_info = get_list_info(data_board_cards)
    new_list = get_listForLoop(card_info, list_info)
    cardNames = getCardNames(data_board_cards)
    
    return render_template('index_3.html', ls = new_list)

app.run()

