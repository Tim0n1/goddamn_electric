import mysql.connector
db = mysql.connector.connect(host='sql11.freesqldatabase.com', user='sql11504349', passwd='WBXaQjYwhn', database='sql11504349')
cursor = db.cursor()

def get_all_users():
    cursor.execute('SELECT * FROM user_info')
    return cursor.fetchall()


def get_all_ids():
    cursor.execute('SELECT discord_id FROM user_info')
    return cursor.fetchall()[0]

class BalanceUtilisation:

    @staticmethod
    def get_balance(discord_id: str):
        for i in get_all_users():
            if i[1] == discord_id:
                return i[2]

    @staticmethod
    def new_balance(discord_id: str, new_balance: int):
        cursor.execute('''UPDATE user
                                SET 
                                    balance = %s
                                WHERE
                                    discord_id = %s ;''', (new_balance, discord_id))
        db.commit()



print(BalanceUtilisation.get_balance('439875993998589953'))