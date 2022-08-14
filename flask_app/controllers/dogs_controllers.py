from flask_app.models.dog_model import Dog
from flask import render_template, redirect, request, session, flash
from flask_app import app



## READ ALL ROUTE
@app.route('/')
def index():
    all_dogs = Dog.get_all()
    return render_template("index.html", dogs = all_dogs)  ## server calls get_all method, all_dogs in get_all method, which returns a list of dicitonaries of the dogs in the DB.



## READ ONE ROUTE
@app.route('/dogs/<int:id>')  ## Passing info from user to route via path variable -> need to go into parameters of def function and then into the data dictionary
def display_one(id):
    data = {         ## Route needs to form a data dictionary of the id of the dog we want to get // the query method is looking for an id-- we need to pass it a data dictionary that has an id
        "id" : id
    }
    dog = Dog.get_one(data)     ## Passing data dictionary from two lines above here, and need to put it as an argument one line below
    return render_template("one_dog.html", dog = dog) # Passing dog to the template here



## CREATE A DOG
@app.route('/dogs/new')         ## renders the form that lets us create a dog
def new_dog_form():
    return render_template('new_dog.html')

@app.route('/dogs/create', methods=['POST'])      ## ACTION route that actually creates the dog in the DB
def create_dog():
    Dog.create(request.form)    ## request.form is an immutable dictionary
    return redirect('/')



## UPDATE DOG
@app.route('/dogs/<int:id>/edit')    ## Use the path variables again // display the form to edit a dog
def edit_form_dog(id):      ## need to pass the path variable id
    data = {
        "id" : id           ## id from path to get dog's info
    }
    dog = Dog.get_one(data)
    return render_template("edit_dog.html", dog = dog)

@app.route('/dogs/<int:id>/update', methods=['POST'])      ## ACTION ROUTE to actually update entries
def update_dog(id):
    data = {
        "name" : request.form['name'],
        "color" : request.form['color'],
        "breed" : request.form['breed'],
        "id" : id       ## Need to set and pass id, because the query is requesting an id in WHERE conditional
    }
    Dog.update(data)    ## using class method update to change DB
    return redirect('/')  ## always redirect on an action route




## DELETE (adopt) DOG
@app.route('/dogs/<int:id>/delete')     ## ACTION ROUTE -> since it is doing something on the backend -> redirect
def delete_dog(id):
    data = {
        "id" : id
    }
    Dog.delete(data)
    return redirect('/')

