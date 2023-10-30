import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    # default value for all is an empty list
    all = []
    
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None
    
    @classmethod  
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        
        """
        CURSOR.execute(sql)
    
    @classmethod    
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        
        """
        CURSOR.execute(sql)
        
    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            
            """
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

        else:
            CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?",
                               (self.name, self.breed, self.id))
            
           
            
    @classmethod    
    def create(cls, name, breed):
        #create a dog instance
        dog = Dog(name,breed)
        #save dog to db using the save() method
        dog.save()
        
        return dog
    
    @classmethod
    #returns an instance from the rows in the db
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
        
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
         
        try:
            sql = """
                SELECT *
                FROM dogs
                WHERE name, breed = ?, ?
            
            """
            dog = CURSOR.execute(sql, (name,breed)).fetchone()
            return cls.new_from_db(dog)
        except:
            if dog is None:
                dog = cls.create(name, breed)
                            
    def update(self):
        self.save()
            