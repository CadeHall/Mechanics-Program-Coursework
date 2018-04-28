import sqlite3

class Database:

    def __init__(self):
        self.file = 'MechanicsData.sqlite'
        self.conn = sqlite3.connect(self.file)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS simulations (
                        simID INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        type TEXT
                        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS balls (
                        ballID INTEGER PRIMARY KEY,
                        b_simID INTEGER,
                        type TEXT,
                        count INTEGER,
                        mass REAL,
                        radius INTEGER,
                        colour TEXT,
                        xposition INTEGER,
                        yposition INTEGER,
                        xvelocity REAL,
                        yvelocity REAL,
                        FOREIGN KEY (b_simID)REFERENCES simulations (simID)
                        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS acceleration (
                        accelerationID INTEGER PRIMARY KEY,
                        a_simID INTEGER,
                        walls BOOL,
                        variable TEXT,
                        xvelocity TEXT,
                        yvelocity TEXT,
                        FOREIGN KEY (a_simID) REFERENCES simulations (simID)
                        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS collisions (
                        collisionID INTEGER PRIMARY KEY,
                        c_simID INTEGER,
                        walls BOOL,
                        elastic BOOL,
                        radius BOOL,
                        ab REAL,
                        ac REAL,
                        ad REAL,
                        bc REAL,
                        bd REAL,
                        cd REAL,
                        FOREIGN KEY (c_simID) REFERENCES simulations (simID)
                        )''')

    def save(self, sim_type, data):

        self.cursor.execute('''INSERT INTO simulations (name, description, type) VALUES (
                            ?, ?, ?
                            )''', (data[0], data[1], sim_type))

        self.sim_id = self.cursor.lastrowid
        
        if sim_type == 'c':
            for ball in data[2]:
                self.cursor.execute(''' INSERT INTO balls (b_simId, type, count, mass, radius, colour, xposition ,yposition, xvelocity, yvelocity) VALUES (
                                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                                   )''', (self.sim_id, sim_type, ball.count, ball.mass, ball.radius, ball.colour, ball.position[0], ball.position[1], ball.xvel, ball.yvel))

            self.values = (self.sim_id, data[3][0], data[3][1], data[3][2], data[3][3], data[3][4], data[3][5], data[3][6], data[3][7], data[3][8])
                                                            
            self.cursor.execute(''' INSERT INTO collisions (c_simID, walls, radius, elastic, ab, ac, ad, bc, bd, cd) VALUES (
                               ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                               )''', (self.values))

        elif sim_type == 'a':
            ball = data[2]
            self.cursor.execute(''' INSERT INTO balls (b_simID, type, count, mass, radius, colour, xposition ,yposition, xvelocity, yvelocity) VALUES (
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                                )''', (self.sim_id, sim_type, ball.count, ball.mass, ball.radius, ball.colour, ball.position[0], ball.position[1], ball.xvel, ball.yvel))
                
            self.values = (str(self.sim_id), data[3][0], data[3][1], data[3][2], data[3][3])

            self.cursor.execute(''' INSERT INTO acceleration (a_simID, walls, variable, xvelocity, yvelocity) VALUES (
                               ?, ?, ?, ?, ?
                               )''', (self.values))

        else:
            return NotImplementedError

        self.conn.commit()


    def load_for_menu(self):
        self.cursor.execute(''' SELECT * FROM simulations ''')
        self.basic_info = self.cursor.fetchall()

        return self.basic_info

    def load_specific(self, sim_type, sim_id):
        self.sim_data = []
        self.ball_data = []
        
        if sim_type == 'c':
            self.cursor.execute(''' SELECT * FROM collisions WHERE c_simID = ? ''', (sim_id))
            self.sim_data = self.cursor.fetchall()

            self.cursor.execute(''' SELECT * FROM balls WHERE b_simID = ? ''', (sim_id))
            self.ball_data = self.cursor.fetchall()
            
        elif sim_type == 'a':
            self.cursor.execute(''' SELECT * FROM acceleration WHERE a_simID = ? ''', (sim_id))
            self.sim_data = self.cursor.fetchall()

            self.cursor.execute(''' SELECT * FROM balls WHERE b_simID = ? ''', (sim_id))
            self.ball_data = self.cursor.fetchall()

        self.conn.commit()

        return [self.sim_data, self.ball_data]

    def reset(self):
        self.cursor.execute('''DROP TABLE IF EXISTS balls''')
        self.cursor.execute('''DROP TABLE IF EXISTS simulations''')
        self.cursor.execute('''DROP TABLE IF EXISTS collisions''')
        self.cursor.execute('''DROP TABLE IF EXISTS acceleration''')
        
        self.conn.commit()

    def remove(self, sim_id):
        self.cursor.execute(''' DELETE FROM simulations WHERE simID = ? ''', sim_id)
        self.cursor.execute(''' DELETE FROM collisions WHERE c_simID = ? ''', sim_id)
        self.cursor.execute(''' DELETE FROM acceleration WHERE a_simID = ? ''', sim_id)
        self.cursor.execute(''' DELETE FROM balls WHERE b_simID = ? ''', sim_id)

        self.conn.commit()

    def finish(self):
        self.cursor.close()
        self.conn.close()





            
            
