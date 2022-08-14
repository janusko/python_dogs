from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Award:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dog_id = data['dog_id']

        ### NOTICE: I forgot the take 's' off of dog_id when I created the ERD table, so any dogs_id, should be dog_id for future projects

    
    ## CREATE AN AWARD
    @classmethod
    def create(cls, data):
        query = "INSERT INTO awards (title, dog_id) VALUES (%(title)s, %(dog_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    
    ## 