class ItemClass:

  def __init__(self, id, title, status):
        self.id = id
        self.status = status
        self.title = title

  @classmethod
  def from_trello_card(cls, card, list):
      return cls(card['id'], card['name'], list['name'])

class ViewModel:
    def __init__(self, item_list):
        self._items = item_list
        
    @property
    def items(self):
        return self._items

    @property
    def doing_items(self):
        doingList = []

        print(self.items)
        for i in self.items:
            if i.status == 'In Progress':
                print(i.status)
                doingList.append(i.title)

        return doingList

    @property
    def toDo_items(self):
        toDoList = []

        print(self.items)
        for i in self.items:
            if i.status == 'To Do':
                toDoList.append(i.title)

        return toDoList

    @property
    def done_items(self):
        doneList = []
        for i in self.items:
            if i.status == 'Done':
                doneList.append(i.title)

        return doneList