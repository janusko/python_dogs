from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import dog_model      ## import the whole file, not just the class to avoid circular import
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

    ## GET ALL WITH RECIPIENT
    @classmethod
    def get_all_with_recipient(cls):
        query = 'SELECT * FROM awards JOIN dogs ON awards.dog_id = dogs.id ;'       ## test join on MySQL to see if it works // each row will be one award and one recipient
        results = connectToMySQL(DATABASE).query_db(query)      ## list of dictionaries (even if it's just one result)
        if results:     ## protecting us if we don't have any dogs or awards in database upon query // would return an empty list because of the if
            awards = []
            for row in results:
                print(results)
                awards_instance = cls(row)      ## on the left, not going to have any data that isn't prepared for us
                recipient_data = {
                    **row,
                    'id' : row['dogs.id'],      ## again, only changing the ones that are on the right side of the JOIN // due to duplicate fields. Would be overridden if they weren't changed.
                    'created_at' : row['dogs.created_at'],
                    'updated_at' : row['dogs.updated_at']
                }
                dog_instance = dog_model.Dog(recipient_data)
                awards_instance.recipient = dog_instance        ## award_instance inside loop that has new attribute call recipient that hold entire Dog object // we can name recipient whatever we want
                awards.append(awards_instance)                  ## adding award_instance with dog_instance attached to it inside awards []
            return awards
        return results


    ## MANY TO ONE JOIN
    @classmethod
    def get_one_with_recipients(cls, data):
        query = 'SELECT * FROM awards JOIN dogs ON awards.dog_id = dogs.id WHERE awards.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            award_instance = cls(results[0])
            recipient_data = {
                **results[0],
                'id' : results[0]['dogs.id'],      ## again, only changing the ones that are on the right side of the JOIN // due to duplicate fields. Would be overridden if they weren't changed.
                'created_at' : results[0]['dogs.created_at'],
                'updated_at' : results[0]['dogs.updated_at']
            }
            recipient_instance = dog_model.Dog(recipient_data)
            award_instance.recipient  = recipient_instance
            return award_instance
        return results