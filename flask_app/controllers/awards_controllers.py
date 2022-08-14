from flask_app.models.award_model import Award
from flask_app.models.dog_model import Dog
from flask import render_template, redirect, request, session, flash
from flask_app import app


### EVERY TIME YOU MAKE A NEW CONTROLLER, IMPORT IT IN THE SERVER.PY ###

## AWARDING A DOG
@app.route('/awards/new')     ## display the new award form
def new_award_form():
    all_dogs = Dog.get_all()      ## going to need all dogs from template to be able to assign an award to a specific dog
    return render_template('new_award.html', all_dogs = all_dogs)

@app.route('/awards/create', methods=['POST'])
def create_award():
    ## need to call upon Award model to interact with DB via craete function -> INSERT query -> request.form via html (html matches INSERT query requiremnets: title and dog_id)
    Award.create(request.form)
    return redirect(f"/dogs/{request.form['dog_id']}")     #### NEED TO use an f string to make sure we are going through the /dogs/<int:id> to get the dog's id
    ## above, we don't have access to the dogs_id, so we have to get it from the request.form -> redirect dynamically


##### We need to make changes with dog controller and dog model , now that we want to display the awards on the dog's page #####
## Start by editing dog_get_one function so that we now get a list of awards assigned to that dog -> JOIN dog_model -> need to rewrite the dog get_one ##


@app.route('/awards')
def all_awards():
    awards = Award.get_all_with_recipient()
    return render_template('all_awards.html', awards = awards)

@app.route('/awards/<int:id>')
def one_award(id):
    data = {
        'id' : id 
    }
    award = Award.get_one_with_recipients(data)
    return render_template('one_award.html', award = award)