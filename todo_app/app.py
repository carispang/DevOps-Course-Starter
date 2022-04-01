#mydict = dict((rows[0],rows[1]) for rows in reader)
from flask import Flask, render_template, redirect, request
from todo_app.data.session_items import get_items, add_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())
#@app.route('/')
#def index():
    # Modify the index() function to get the list of items 
 #  items = get_items() 
  # return render_template('index.html', ls = items)

@app.route('/', methods = ['GET', 'POST'])
def post_item():
   items = get_items()
   if request.method == 'POST':
      title =  request.form.get('name')
      items = add_item(title)
      print(items)
      render_template('index.html', ls = items)
      return redirect(request.url)
   return render_template('index.html', ls = items) 
  # return 'hello'
# Update the function for your new route to retrieve the item title from the form data using request.form.get('field_name') — 
# where field_name 
# is the name of the input field in your form.
# Finally, add the item to the list, and redirect the user back to the index page, using the redirect function from Flask. 
# Returning a redirect means you avoid repetition of code, 
# plus the browser will show the correct URL and can refresh without resubmitting the form.

