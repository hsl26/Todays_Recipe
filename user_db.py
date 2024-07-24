import sqlite3

# DB의 파일명 입니다.
DB_NAME = 'user.db'

# 사용하실 필요 없습니다.
def initialize_recipe_table(db_name = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        ID TEXT NOT NULL, 
        food TEXT NOT NULL,
        recipe TEXT NOT NULL,
        PRIMARY KEY (ID, food)
    )
    ''')
    conn.commit()
    conn.close()

# 사용자 정보 추가
def add_user(id, pwd, email, name):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_information (
        "ID" TEXT PRIMARY KEY NOT NULL,
        "PWD" TEXT NOT NULL,
        "EMAIL" TEXT,
        "NAME" TEXT
    ); ''')
   
    cur.execute("INSERT INTO user_information Values(?, ?, ?, ?)", (id, pwd, email, name))
    con.commit()
    cur.close()
    con.close()


# 사용자 정보 수정 ( password, email )
def edit_information(id, new_pwd, new_email):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_information (
        "ID" TEXT PRIMARY KEY NOT NULL,
        "PWD" TEXT NOT NULL,
        "EMAIL" TEXT,
        "NAME" TEXT
    ); ''')
    
    cur.execute("UPDATE user_information SET PWD = ?, EMAIL = ? WHERE ID = ?", (new_pwd, new_email, id))

    con.commit()
    cur.close()
    con.close()


# 아이디 존재여부 확인 ( 존재하면 0 반환 )
def id_not_exists(id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_information (
        "ID" TEXT PRIMARY KEY NOT NULL,
        "PWD" TEXT NOT NULL,
        "EMAIL" TEXT,
        "NAME" TEXT
    ); ''')

    cur.execute("SELECT EXISTS(SELECT 1 FROM user_information WHERE id=?)", (id, ))
    exists = cur.fetchone()[0]
    con.close()
    return exists == 0


# 로그인 (성공시 1 반환)
def log_in(id, pwd):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_information (
        "ID" TEXT PRIMARY KEY NOT NULL,
        "PWD" TEXT NOT NULL,
        "EMAIL" TEXT,
        "NAME" TEXT
    ); ''')

    cur.execute("SELECT PWD FROM user_information WHERE ID = ?", (id, ))
    if pwd == cur.fetchone()[0]:
        return 1
    else:
        return 0


# 사용자 이름 조회 
def get_user_name(id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_information (
        "ID" TEXT PRIMARY KEY NOT NULL,
        "PWD" TEXT NOT NULL,
        "EMAIL" TEXT,
        "NAME" TEXT
    ); ''')
    
    cur.execute("SELECT NAME FROM user_information WHERE ID = ?", (id, ))
    
    name = cur.fetchone()
    if name:
        return name[0]


# DB에서 회원 정보를 가져오는 함수
def get_user_information(user_id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("SELECT PWD, EMAIL, NAME FROM user_information WHERE ID = ?", (user_id,))
    user_info = cur.fetchone()
    cur.close()
    con.close()
    return user_info


# 사용자 계정 삭제
def delete_user(id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_information (
        "ID" TEXT PRIMARY KEY NOT NULL,
        "PWD" TEXT NOT NULL,
        "EMAIL" TEXT,
        "NAME" TEXT
    ); ''')

    cur.execute("DELETE FROM user_information WHERE ID = ?", (id, ))

    con.commit()
    cur.close()
    con.close()


# 냉장고에 재료 추가
def add_ingredient(id, ingredient):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS refrigerator (
            "ID" TEXT NOT NULL,
            "INGREDIENT" TEXT NOT NULL,
            PRIMARY KEY ("ID", "INGREDIENT")
        );
    ''')

    cur.execute("INSERT INTO refrigerator Values(?, ?)", (id, ingredient))
    con.commit()
    cur.close()
    con.close()


# 냉장고에 재료 삭제
def delete_ingredient(id, ingredient):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS refrigerator (
            "ID" TEXT NOT NULL,
            "INGREDIENT" TEXT NOT NULL,
            PRIMARY KEY ("ID", "INGREDIENT")
        );
    ''')

    cur.execute("DELETE FROM refrigerator WHERE ID = ? AND INGREDIENT = ?", (id, ingredient))

    con.commit()
    cur.close()
    con.close()


# 냉장고 재료 조회
def get_ingredient(id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS refrigerator (
            "ID" TEXT NOT NULL,
            "INGREDIENT" TEXT NOT NULL,
            PRIMARY KEY ("ID", "INGREDIENT")
        );
    ''')

    cur.execute("SELECT INGREDIENT FROM refrigerator WHERE ID = ?", (id, ))
    result = cur.fetchall()
    lst = [row[0] for row in result] if result else []

    cur.close()
    con.close()
    return lst


# 좋아하는 음식 추가 
def add_likes(id, like):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS like_items (
        "ID" TEXT NOT NULL,
        "LIKE" TEXT NOT NULL,
        PRIMARY KEY ("ID", "LIKE")
    ); ''')

    cur.execute("INSERT INTO like_items Values(?, ?)", (id, like))

    con.commit()
    cur.close()
    con.close()


# 좋아하는 음식 삭제
def delete_likes(id, like):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS like_items (
        "ID" TEXT NOT NULL,
        "LIKE" TEXT NOT NULL,
        PRIMARY KEY ("ID", "LIKE")
    ); ''')

    cur.execute("DELETE FROM like_items WHERE ID = ? AND LIKE = ?", (id, like))

    con.commit()
    cur.close()
    con.close()


# 좋아하는 음식 조회
def get_likes(id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS like_items (
        "ID" TEXT NOT NULL,
        "LIKE" TEXT NOT NULL,
        PRIMARY KEY ("ID", "LIKE")
    ); ''')

    cur.execute("SELECT LIKE FROM like_items WHERE ID = ?", (id, ))
    result = cur.fetchall()
    lst = [row[0] for row in result] if result else []
    
    cur.close()
    con.close()
    return lst


# 싫어하는 음식 추가
def add_dislikes(id, dislike):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS dislike_items (
        "ID" TEXT NOT NULL,
        "DISLIKE" TEXT NOT NULL,
        PRIMARY KEY ("ID", "DISLIKE")   
    ); ''')

    cur.execute("INSERT INTO dislike_items Values(?, ?)", (id, dislike))

    con.commit()
    cur.close()
    con.close()


# 싫어하는 음식 삭제
def delete_dislikes(id, dislike):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS dislike_items (
        "ID" TEXT NOT NULL,
        "DISLIKE" TEXT NOT NULL,
        PRIMARY KEY ("ID", "DISLIKE")   
    ); ''')

    cur.execute("DELETE FROM dislike_items WHERE ID = ? AND DISLIKE = ?", (id, dislike))
    
    con.commit()
    cur.close()
    con.close()


# 싫어하는 음식 조회
def get_dislikes(id):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS dislike_items (
        "ID" TEXT NOT NULL,
        "DISLIKE" TEXT NOT NULL,
        PRIMARY KEY ("ID", "DISLIKE")   
    ); ''')

    cur.execute("SELECT DISLIKE FROM dislike_items WHERE ID = ?", (id, ))
    result = cur.fetchall()
    lst = [row[0] for row in result] if result else []

    cur.close()
    con.close()
    return lst

######################################################################################################################################
# 내 레시피 저장 테이블 관련 인터페이스 함수들

# DB에 id,food,recipe를 삽입하는 함수입니다. 사용법 예시) insert_recipe(id,food,recipe)
def insert_recipe(id, food, recipe, db_name = DB_NAME):
    # 어디서 호출 하더라도 오류를 막기 위해서. 
    initialize_recipe_table()
    
    # DB 열기.
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # DB 삽입.
    cursor.execute('INSERT INTO recipes (ID, food, recipe)VALUES (?, ?, ?)', (id, food, recipe))
    
    # 커밋하고 닫기
    conn.commit()
    conn.close()

# DB내의 모든 값 반환하는 함수입니다. 사용법 예시) all_history = get_all_history()
def get_all_history(db_name = DB_NAME):
    initialize_recipe_table()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM recipes')
    recipes = cursor.fetchall()
    
    conn.close()
    
    return recipes

# DB내의 모든 값 프린트하는 함수입니다. 사용법 예시) print_all_history()
def print_all_history(db_name = DB_NAME):
    initialize_recipe_table()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM recipes')
    recipes = cursor.fetchall()
    
    conn.close()
    
    for row in recipes :
        print(row)

# id랑 food를 파라미터로 받아서 recipe를 얻어내는 함수입니다. 사용법 예시) recipe_text = get_recipe(id,food)
def get_recipe(id, food,db_name = DB_NAME):
    initialize_recipe_table()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # id, food랑 매치되는 곳의 recipe 가져옵니다.
    cursor.execute('SELECT recipe FROM recipes WHERE ID = ? AND food = ?', (id, food))
    recipe = cursor.fetchone()
    conn.close()
    
    # 레시피를 반환합니다.
    return recipe[0] if recipe else None

# 특정 유저의 모든 food를 반환하는 함수.   사용법 예시 ) users_all_food = get_users_all_food('parkgod98')
# 파이썬 배열 형식의 리턴값을 가집니다. ex ['김치찌개', '된장찌개', '사시미']
def get_users_all_food(id, db_name=DB_NAME):
    initialize_recipe_table()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT food FROM recipes WHERE ID = ?', (id,))
    foods = cursor.fetchall()
    
    conn.close()
    
    return [food[0] for food in foods]

# id,food만 파라미터로 삽입하면 그 행을 지울 함수입니다. 사용법 예시) remove_recipe(id,food)
def remove_recipe(id, food,db_name = DB_NAME):
    initialize_recipe_table()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM recipes WHERE ID = ? AND food = ?', (id, food))
    
    conn.commit()
    conn.close()

# 레시피 존재 여부 확인 ( 존재하면 1 반환 )
def check_exists(id, food, db_name = DB_NAME):
    initialize_recipe_table()

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM recipes WHERE ID=? AND food=?)", (id, food))
    result = cursor.fetchone()[0]
    conn.close()

    return result

# 새로운 값으로 덮어쓰기
def replace_recipe(id, food, new_food_name, new_recipe, db_name = DB_NAME):
    initialize_recipe_table()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE recipes SET food = ?, recipe = ? WHERE ID = ? AND food = ?', (new_food_name, new_recipe, id, food))
    
    conn.commit()
    conn.close()
