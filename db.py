import sqlite3

def create_and_connect(db_name):
    # Подключение к базе данных (если файла базы данных не существует, он будет создан)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создание таблицы для хранения объектов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            a REAL NOT NULL,
            b REAL NOT NULL,
            p REAL NOT NULL,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

def add_object(a, b, p, name, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO objects (a, b, p, name)
            VALUES (?, ?, ?, ?)
        ''', (a, b, p, name))
        conn.commit()
        print(f"Object {name} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Object with name {name} already exists.")
    
    conn.close()

def add_objects(objects, db_name):
    for obj in objects:
        a, b, p, name = obj
        add_object(a, b, p, name, db_name)

def get_object(name, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM objects WHERE name = ?', (name,))
    obj = cursor.fetchone()
    
    conn.close()
    
    if obj:
        return {
            obj[1],
            obj[2],
            obj[3],
            obj[4]
        }
    else:
        print(f"Object with name {name} not found.")
        return None

def get_all_objects(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM objects')
    rows = cursor.fetchall()
    
    conn.close()
    
    objects = []
    for row in rows:
        objects.append((
            row[1],
            row[2],
            row[3],
            row[4]
        ))
    
    return objects

def update_object(a, b, p, name, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE objects
        SET a = ?, b = ?, p = ?
        WHERE name = ?
    ''', (a, b, p, name))
    
    conn.commit()
    conn.close()
    print(f"Object {name} updated successfully.")

def delete_object(name, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM objects WHERE name = ?', (name,))
    
    conn.commit()
    conn.close()
    print(f"Object {name} deleted successfully.")
