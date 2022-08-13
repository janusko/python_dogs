from config.mysqlconnection import connectToMySQL
DATABASE = 'dogs_schema'

class Dog:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.breed = data['breed']
        self.color = data['color']
        self.created_at = data['created_at']
        self.updated_at = data['created_up']


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
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dogs WHERE id = %(id)s;"     ## data needs to be dictionary with key of id- holding id of dog we want to get
        results = connectToMySQL(DATABASE).query_db(query,data)     ## still going to be a list of dictionaries, even if just one dog
        ## we want to instantiate this one dog, but also solve situation if we don't don't find dog/dog id doesn't exist
        if results:     ## if don't find dog id, reuslts will come back as empty list
            dog_instance = cls(results[0])      ## results is a list, and create an instance off first dict -> just one -> [0]
            return dog_instance
        return results  ## if empty <- get back empty list/no dog id


    ## CREATE A DOG 
    @classmethod      ## all queries will be classmethod so we can access them right off the class-- don't need to instantiate anything
    def create(cls, data):      ## Taking in data ()
        query = "INSERT INTO dogs (name, color, breed) VALUES (%(name)s, %(color)s, %(breed)s);"
        return connectToMySQL(DATABASE).query_db(query, data)      ## just need to return, because value we are getting back is just the id // data has to have same key as rows in DB


    ## UPDATE A DOG
    @classmethod
    def update(cls, data):
        query = "UPDATE dogs SET name = %(name)s, color = %(color)s, breed = %(breed)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    ## DELETE A DOG
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM dogs WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
        