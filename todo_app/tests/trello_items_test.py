import os
#os.chdir('/Users/carispang/Documents/my-code/DevOps/DevOps-Course-Starter/todo_app/tests')
print("Current working directory: {0}".format(os.getcwd()))
from data.class_definitions import ItemClass, ViewModel

#class TestViewModel: 
   # @staticmethod
def test_doing_items():
    list = [ItemClass(id = 1, title = 'do some coding', status = 'To Do'), ItemClass(id = 2, title = 'In Progress', status = 'Doing'), ItemClass(id = 3, title = 'write some unit tests', status = 'Done')]
    testViewModel = ViewModel(list) 
    doing_items = testViewModel.doing_items
    assert len(doing_items) == 0


#  @staticmethod
def test_done_items():
    list = [ItemClass(id = 1, title = 'do some coding', status = 'To Do'), ItemClass(id = 2, title = 'In Progress', status = 'Doing'), ItemClass(id = 3, title = 'write some unit tests', status = 'Done')]
    testViewModel = ViewModel(list) 
    done_items = testViewModel.done_items
    assert len(done_items) == 1

  #  @staticmethod
def test_toDo_items():
    list = [ItemClass(id = 1, title = 'do some coding', status = 'To Do'), ItemClass(id = 2, title = 'In Progress', status = 'Doing'), ItemClass(id = 3, title = 'write some unit tests', status = 'Done')]
    testViewModel = ViewModel(list) 
    toDo_items = testViewModel.toDo_items
    assert len(toDo_items) == 1

# create an instance of ViewModel containing some example item objects with various statuses




