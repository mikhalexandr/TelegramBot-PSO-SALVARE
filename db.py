import sqlite3


con = sqlite3.connect(r"data\db.sqlite")
cur = con.cursor()


def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        lost (user_id TEXT, lost_name_id TEXT, born TEXT, regions TEXT, description TEXT, feature TEXT, 
        spec_feature TEXT, clothes TEXT, items TEXT, photo TEXT)
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS
            checking (user_id TEXT, lost_name_id TEXT, born TEXT, regions TEXT, description TEXT, feature TEXT, 
            spec_feature TEXT, clothes TEXT, items TEXT, photo TEXT)
        """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS
                people (user_id TEXT, name TEXT, help_count INT DEFAULT 0, comm_count INT DEFAULT 0, 
                alarm_count INT DEFAULT 0)
            """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        teams (id INTEGER PRIMARY KEY AUTOINCREMENT, loser TEXT, human TEXT UNIQUE)
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        alarmiks (user_id TEXT, cords TEXT, number TEXT, name TEXT, charge TEXT, look TEXT, situation TEXT, 
        photo_id TEXT)
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        alarm_users(user_id TEXT)
    """)


def get_human(user_id):
    req = """SELECT name FROM people WHERE user_id = ?"""
    return con.execute(req, (str(user_id),)).fetchone()[0]


def check_id(user_id):
    req = """SELECT EXISTS(SELECT 1 FROM people WHERE user_id = ?) as id_exists"""
    return cur.execute(req, (str(user_id),)).fetchone()[0]


def push_lost_info(user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo):
    req = """
        INSERT 
        INTO lost (user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cur.execute(req, (user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo))
    con.commit()


def push_checking_info(user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo):
    req = """
        INSERT 
        INTO checking (user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cur.execute(req, (user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo))
    con.commit()


def get_lost_info(lost_name_id):
    req = """
        SELECT user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo 
        FROM lost
        WHERE lost_name_id = ?
    """
    result = cur.execute(req, (lost_name_id,)).fetchone()
    return result


def del_lost(loser):
    req = """
            DELETE FROM lost
            WHERE lost_name_id = ?
            """
    cur.execute(req, (loser,))
    con.commit()


def get_all_lost_info():
    req = """
        SELECT user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo 
        FROM lost
    """
    result = cur.execute(req).fetchall()
    return result


def get_checking_info():
    req = """
        SELECT user_id, lost_name_id, born, regions, description, feature, spec_feature, clothes, items, photo 
        FROM checking
    """
    result = cur.execute(req, ).fetchone()
    return result


def delete_checking(lost_name_id):
    req = """
        DELETE FROM checking
        WHERE lost_name_id = ?
        """
    cur.execute(req, (lost_name_id,))
    con.commit()


def add_human(user_id, name):
    req1 = """SELECT * FROM people WHERE user_id = ?"""
    req2 = """UPDATE people
    SET name = ? WHERE user_id = ?"""
    req3 = """INSERT INTO people (user_id, name) VALUES (?, ?)"""
    if cur.execute(req1, (user_id,)).fetchone():
        cur.execute(req2, (name, user_id))
    else:
        cur.execute(req3, (user_id, name))
    con.commit()


def get_all():
    req = """SELECT user_id FROM people"""
    result = cur.execute(req).fetchall()
    return [i[0] for i in result]


def get_teams():
    req = """SELECT loser FROM teams"""
    result = cur.execute(req).fetchall()
    return [i[0] for i in result]


def create_team(loser):
    req = """INSERT INTO teams(loser, human) VALUES (?, NULL)"""
    cur.execute(req, (loser,))
    con.commit()


def add_team_member(member, loser):
    req2 = """INSERT INTO teams(loser, human) VALUES (?, ?) ON CONFLICT (human) DO NOTHING"""
    cur.execute(req2, (loser, member))
    con.commit()


def del_team_member(user_id):
    req = """DELETE FROM teams WHERE human = ?"""
    cur.execute(req, (user_id,))
    con.commit()


def is_in_team(user_id):
    req = """SELECT * FROM teams WHERE human = ?"""
    res = cur.execute(req, (user_id,)).fetchone()
    return res


def del_team(loser_id):
    req = """DELETE FROM teams WHERE loser = ?"""
    cur.execute(req, (loser_id,))
    con.commit()


def get_teammates(user_id):
    req = """SELECT human FROM teams WHERE loser = (
    SELECT loser FROM teams WHERE human = ?) AND human != ?"""
    return cur.execute(req, (user_id, user_id)).fetchall()


def get_teammates_by_loser(loser):
    req = """SELECT human FROM teams WHERE loser = ?"""
    return cur.execute(req, (loser,)).fetchall()


def add_alarmik(user_id, cords, number, name, charge, look, situation, photo=None):
    req = """
            INSERT INTO alarmiks (user_id, cords, number, name, charge, look, situation, photo_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
    cur.execute(req, (user_id, cords, number, name, charge, look, situation, photo))
    con.commit()


def get_alarmik(user_id):
    req = f"""
        SELECT * FROM alarmiks WHERE user_id = ?
    """
    return cur.execute(req, (user_id,)).fetchone()


def delete_alarmik(user_id):
    req = f"""
        DELETE FROM alarmiks
        WHERE user_id = ?
    """
    cur.execute(req, (user_id,))
    con.commit()


def add_alarm_id(user_id):
    req = f"""
        INSERT INTO alarm_users (user_id) VALUES (?)
    """
    cur.execute(req, (user_id,))
    con.commit()


def get_alarm_id():
    req = f"""
        SELECT user_id FROM alarm_users
    """
    return cur.execute(req).fetchone()


def update_person_name(user_id, name):
    req = f"""
        UPDATE people SET name = ?
        WHERE user_id = ?
    """
    cur.execute(req, (name, user_id))
    con.commit()


def get_person_info(user_id):
    req = f"""
        SELECT help_count, comm_count, alarm_count FROM people
        WHERE user_id = ?
    """
    res = list(cur.execute(req, (user_id,)).fetchone())
    return res


def update_help_count(user_id):
    req = f"""
        UPDATE people SET help_count = help_count + 1
        WHERE user_id = ?
    """
    cur.execute(req, (user_id,))
    con.commit()


def update_comm_count(user_id):
    req = f"""
        UPDATE people SET comm_count = comm_count + 1
        WHERE user_id = ?
    """
    cur.execute(req, (user_id,))
    con.commit()


def update_alarm_count(user_id):
    req = f"""
        UPDATE people SET alarm_count = alarm_count + 1
        WHERE user_id = ?
    """
    cur.execute(req, (user_id,))
    con.commit()
