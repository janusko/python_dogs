from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import award_model  ## do it this way to avoid circular imports // don't import just Award
from flask_app import DATABASE

class Dog:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.breed = data['breed']
        self.color = data['color']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    ## READ ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dogs;"
        results = connectToMySQL(DATABASE).query_db(query)      ## holds list of dictionary from DB, call query_db method that takes in query and potentially some data
        all_dogs = []
        for row in results:      ## row is iterative variable (can call whatever we want, here row is one row in our DB) // results (above) is a list of dictionaries that we will be looping over
            dog_instance = cls(row)     ## row == data in constructor // cls (could use Dog(row) if that makes it more clear) -- reference to the class we are in. We are instantiating a dog from the row in our DB. That dict has all the keys from the constructor (id, name, breed...)
            all_dogs.append(dog_instance)     ## now we put each row (as an individual row) into a dictionary and htat into our all_dogs list, which becomes a list of dictionaries
        return all_dogs

    
    ## READ ONE
    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM dogs WHERE id = %(id)s;"     ## data needs to be dictionary with key of id- holding id of dog we want to get
    #     results = connectToMySQL(DATABASE).query_db(query,data)     ## still going to be a list of dictionaries, even if just one dog
    #     ## we want to instantiate this one dog, but also solve situation if we don't don't find dog/dog id doesn't exist
    #     if results:     ## if don't find dog id, reuslts will come back as empty list
    #         dog_instance = cls(results[0])      ## results is a list, and create an instance off first dict -> just one -> [0]
    #         return dog_instance
    #     return results  ## if empty <- get back empty list/no dog id

##### Above is fine for non-JOIN, but since we want to JOIN awards onto dogs, we need need to rewrite the method

    ## READ ONE v.2 -- JOIN
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dogs LEFT JOIN awards ON awards.dog_id = dogs.id WHERE dogs.id = %(id)s;"      ## LEFT JOIN incase any dogs don't have any awards. 
        results = connectToMySQL(DATABASE).query_db(query,data)

    ## now we are going to instantiate two different objects and then associate them with each other
        ## we'll have a dog_instance and then make a new attribute for that dog_instance
            ## then create an award_instance and store it in that new attribute

        if results:
            dog_instance = cls(results[0])
            awards_list = []        
            for row_in_db in results:       ## results is list of dicts
                ## ambigous fields on right side of join are appended with name of the table -> make dictionary that has all award info from that row
                ## will need to change the names of those columns -> add awards. in front of the columns that have a shared name
                award_data = {
                    # "title" : row_in_db['title'],       ## can't use awards.title, because the dictionary doesn't have a key of awards.title
                    # "dog_id" : row_in_db['dog_id'],
                    **row_in_db,      ## alternative -- unpacks a dictionary -> keyword arguments // sets up every key from that dictionary with every value of that dictionary. don't need to supply unambigious fields // has to be above the awards.
                    "id" : row_in_db['awards.id'],
                    "created_at" : row_in_db['awards.created_at'],
                    "updated_at" : row_in_db['awards.updated_at']
                }
                award_instance = award_model.Award(award_data)
                awards_list.append(award_instance)
            dog_instance.list_awards = awards_list      ## creates new attribute list_awards on this dog instance // list_awards can be anything we want, just keep it descriptive.
            return dog_instance
        return results  
        ## now our get_one method returns dog_instance with a new attribute called list_awards that hold a list of thier awards (via award_data)
            ## now we need to change show_one_dog -> we rewrote that get_one to include a JOIN.
            ## This is not creating an awards list for every dog we create from now on. If we wanted to do that, we could add self.list_awards = [].


    ## CREATE A DOG 
    @classmethod      ## all queries will be classmethod so we can access them right off the class-- don't need to instantiate anything
    def create(cls, data):      ## Taking in data ()
        query = "INSERT INTO dogs (name, color, breed) VALUES (%(name)s, %(color)s, %(breed)s);"
        return connectToMySQL(DATABASE).query_db(query, data)      ## just need to return, because value we are getting back is just the id // data has to have same key as rows in DB


    ## UPDATE A DOG
    @classmethod
    def update(cls, data):
        query = "UPDATE dogs SET name = %(name)s, breed = %(breed)s, color = %(color)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    ## DELETE A DOG
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM dogs WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
        