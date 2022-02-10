import datetime
import sqlite3


class Requester:
    def __init__(self, db_name):
        self.connection = sqlite3.connect("data\\" + db_name)
        self.cursor = self.connection.cursor()

    def get_all_results(self):
        return self.cursor.execute("SELECT * FROM records").fetchall()

    def add_new_result(self, score, title):
        self.cursor.execute("INSERT INTO records(time, title) VALUES(?, ?)", (score, title))
        self.connection.commit()


if __name__ == '__main__':
    req = Requester("best_results.sqlite")
    print(sorted(req.get_all_results()))
    req.add_new_result(10, str(datetime.datetime.now().strftime("%D %H:%M:%S")))
    print(sorted(req.get_all_results()))
