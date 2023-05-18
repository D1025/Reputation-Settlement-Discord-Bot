import sqlite3

# Tworzenie bazy danych i połączenie
conn = sqlite3.connect('data/database.db')
c = conn.cursor()

# Tworzenie tabeli "channels"
c.execute('''CREATE TABLE IF NOT EXISTS channels
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name VARCHAR,
             url VARCHAR
             )''')

# Tworzenie tabeli "ch_set"
c.execute('''CREATE TABLE IF NOT EXISTS ch_set
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              channel_id INTEGER,
              settlement_id INTEGER,
              message_id INTEGER,
              FOREIGN KEY (channel_id) REFERENCES channels(id),
              FOREIGN KEY (settlement_id) REFERENCES settlements(id))''')

# Tworzenie tabeli "settlements"
c.execute('''CREATE TABLE IF NOT EXISTS settlements
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name VARCHAR(255),
              reputation INTEGER DEFAULT 2,
              population VARCHAR(255) DEFAULT 4,
              food INTEGER DEFAULT 2,
              outlook INTEGER DEFAULT 2,
              defences INTEGER DEFAULT 0)''')

# Zatwierdzanie zmian i zamykanie połączenia
conn.commit()
conn.close()
