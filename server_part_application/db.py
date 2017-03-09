import sqlite3


# Create table
# c.execute("CREATE TABLE IF NOT EXISTS 'users_table' ('id_user' INT NOT NULL, 'login_user' VARCHAR(45) NOT NULL,"
#           "'password_user' VARCHAR(45) NOT NULL, PRIMARY KEY ('id_user'))")
# CREATE TABLE `users_table` (
# 	`id_user`	INTEGER PRIMARY KEY AUTOINCREMENT,
# 	`login_user`	INTEGER NOT NULL,
# 	`password_user`	INTEGER NOT NULL
# );

# Insert a row of data
# c.execute("INSERT INTO users_table VALUES (123,123)")

class DbAdapter():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    def add_user(self, login, password):
        self.c.execute(str.format("INSERT INTO users_table VALUES ('%s','%s')" % (login, password)))
        self.conn.commit()

    def read_users(self):
        result = self.c.execute("SELECT * FROM users_table ")
        # result = c.fetchone()
        return result

    def close(self):
        self.conn.close()


# if __name__ == '__main__':
    # for i in read_users():
    #     print(i)
        # conn.close()
