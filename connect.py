from mysql.connector import connect, Error


class ConeBase:
    def __init__(self):
        self.con = 0

    def con_base(self):
        try:
            self.con = connect(
                host='localhost',
                user='root',
                db='company'
            )
            return self.con

        except Error as e:
            print('Соединения нет')
            print(e)