# -*- coding: utf-8 -*-
import requests
#import os
import json
from flask import Flask, render_template, request, redirect, session

def get_board_lists(url, query_string, board_ID):
    url_board_lists = url + "boards/" + board_ID + "/lists"
    response_board_lists = requests.request("GET", url_board_lists, params = query_string)
    data_board_lists = json.loads(response_board_lists.text)
    return(data_board_lists)

def get_list(name, data_board_lists):
    for list in data_board_lists:
        if list['name'] == name:
            todoId = list['id']
            return todoId

def create_card(url, list_id, card_name, key, token):
    url = url + "cards"
    query_string = {"name": card_name, "idList": list_id, "key": key, "token": token}
    response = requests.request("POST", url, params=query_string)
    card_id = response.json()["id"]
    return card_id

def update_list(url, card_ID, done_ID, key, token):
    query_string = {"idList": done_ID, "key": key, "token": token}
    url_board_cards = url + "cards/" + card_ID
    response = requests.request("PUT", url_board_cards, params=query_string)

def get_card_ID_from_name(cardName, data_board_cards):
    for card in data_board_cards:
        nameCard = card['name']
        if cardName == nameCard:
            cardID = card['id']
            return(cardID)

def get_cards_on_list_class(url, list_ID, query_string, data_board_lists):
    url_list_of_cards = url + "lists/" + list_ID + "/cards"
    response_list_cards = requests.request("GET", url_list_of_cards, params = query_string)
    data_cards_lists = json.loads(response_list_cards.text)
    cards_on_list = []
    list_name = get_list_name(list_ID, data_board_lists)
    for i in data_cards_lists:
        item = ItemClass.from_trello_card(card = i, list = {'name': list_name})
        cards_on_list.append(item)
    return cards_on_list
   
def get_data_board_cards(url, query_string, board_ID):
    url_board_cards = url + "boards/" + board_ID + "/cards"
    response_board_cards = requests.request("GET", url_board_cards, params = query_string)
    data_board_cards = json.loads(response_board_cards.text)    
    return data_board_cards
    
def get_list_name(ID, data_board_lists):
    for list in data_board_lists:
        if list['id'] == ID:
            list_name = list['name']
            return list_name

def get_card_class(data_board_cards, data_board_lists):
    new_list = []
    list_info = []
    index = 0
    for card in data_board_cards:
        list_info.append({"name" : get_list_name(card['idList'], data_board_lists)})
        item = ItemClass.from_trello_card(card, list = list_info[index])
        index += 1
        new_list.append(item)
    return new_list
    
def complete_method(data_board_cards, url, done_ID, key, token):
      item_to_complete = str(request.form.get('complete_button'))
      card_ID = get_card_ID_from_name(item_to_complete, data_board_cards)
      update_list(url, card_ID, done_ID, key, token)
      
class ItemClass():

   def __init__(self, id, title, status):
        self.id = id
        self.status = status
        self.title = title

   @classmethod
   def from_trello_card(cls, card, list):
       return cls(card['id'], card['name'], list['name'])

