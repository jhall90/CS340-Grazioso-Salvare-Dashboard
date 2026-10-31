# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self,username,password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # Credentials are passed in by the caller instead of being hard-coded here.
        # 
        # Connection Variables 
        USER = username 
        PASS = password
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
    def next_record_number(self):
        # Get the highest record number (this is the unique index in my mind) by going to the end of the list
        last_record = self.database.animals.find_one(
            sort=[("rec_num", -1)]
        )
        # If it does not exist start at 1
        if last_record and "rec_num" in last_record:
            return last_record["rec_num"] + 1
        else:
            return 1
            
    # Complete this create method to implement the C in CRUD. 
#     def create(self, data):
#         if data is not None: 
#             try:
#                 # Get the next rec_num for inserting
#                 data["rec_num"] = self.next_record_number()

#                 result = self.database.animals.insert_one(data)  # data should be dictionary 
#                 return True if result.inserted_id is not None else False
#             except Exception as e:
#                 print("Error inserting document: ", e)
#                 return False
#         else: 
#             raise Exception("Nothing to save, because data parameter is empty")
    def create(self, data):
        if data is None:
            raise Exception("Nothing to save, because data parameter is empty")

        try:
            # If data is a list insert all (had to update from single only because I created duplicates on accident and deleted the table)
            if isinstance(data, list):
                for document in data:
                    document["rec_num"] = self.next_record_number()
                    self.database.animals.insert_one(document)
                return True

            # If data is a single dictionary → insert one
            elif isinstance(data, dict):
                data["rec_num"] = self.next_record_number()
                result = self.database.animals.insert_one(data)
                return result.inserted_id is not None

            else:
                raise TypeError("Data must be dictionary or list of dictionaries.")

        except Exception as e:
            print("Error inserting document:", e)
            return False


    # Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None: 
            try:
                # Use .find() to return all matches
                documents = self.database.animals.find(query)  
                return list(documents) # Convert to list 
            except Exception as e:
                print("Error reading document: ", e)
                return []
        else: 
            raise Exception("Nothing to read, because query parameter is empty")

    # Update method to implement the U in CRUD.
    def update(self, query, new_values):
        if query is not None and new_values is not None:
            try:
                result = self.database.animals.update_many(query, new_values)
                return result.modified_count
            except Exception as e:
                print("Error updating document:", e)
                return 0
        else:
            raise Exception("query or new_values parameter is empty")
    
    # Delete method to implement the D in CRUD.
    def delete(self, query):
        if query is not None:
            try:
                result = self.database.animals.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print("Error deleting document:", e)
                return 0
        else:
            raise Exception("query parameter is empty")