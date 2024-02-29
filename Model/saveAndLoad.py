from PyQt6 import QtCore
from PyQt6.QtCore import QThread, QDate
from Model import datesExpand

from collections import defaultdict
import sqlite3


def string_cleaner(str_temp) -> str:
    clean_string = ""
    for i in str_temp:
        clean_string += str(i)
    return clean_string


class CalendarRead(QThread):
    # row, column, color(r, g, b), note
    w_data = QtCore.pyqtSignal(int, int, int, int, int, str)
    s_tables = QtCore.pyqtSignal(list)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.table_name = None

    def set(self, table_name) -> None:
        self.table_name = table_name

    @staticmethod
    def get_tables() -> list:
        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()
        cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        table_list = cursor.fetchall()
        return table_list

    def run(self):
        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()
        cursor.execute(f"SELECT count(*) FROM {self.table_name}")
        count = cursor.fetchone()
        count = int(string_cleaner(count))

        for index in range(1, count + 1):

            cursor.execute(f"SELECT startDate FROM {self.table_name} WHERE ROWID = ?", (index,))
            start_date = cursor.fetchone()
            if start_date is not None:
                start_date = string_cleaner(start_date)

            cursor.execute(f"SELECT endDate FROM {self.table_name} WHERE ROWID = ?", (index,))
            end_date = cursor.fetchone()
            if end_date is not None:
                end_date = string_cleaner(end_date)

            cursor.execute(f"SELECT notes FROM {self.table_name} WHERE ROWID = ?", (index,))
            notes = cursor.fetchone()
            if notes is not None:
                notes = string_cleaner(notes)

            cursor.execute(f"SELECT color FROM {self.table_name} WHERE ROWID = ?", (index,))
            color = cursor.fetchone()
            if color is None:
                red, green, blue = (None, None, None)

            else:
                color = string_cleaner(color)
                color = color.split(":")

                red = int(color[0])
                green = int(color[1])
                blue = int(color[2])

            if start_date is not None and end_date is not None:
                dates_list = datesExpand.expand_dates(f"{start_date}-{end_date}")
                for date in dates_list:
                    column, row = date.split(':')
                    self.w_data.emit(int(column) - 1, int(row) - 1, red, green, blue, notes)

        connect.close()


class CalendarSave(QThread):
    s_data = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.tableName = None
        self.table = None

    def set(self, table_name, table) -> None:
        self.tableName = table_name
        self.table = table

    def run(self):
        cords_dict = defaultdict(list)
        notes_dict = {}

        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()

        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                cell = self.table.item(row, column)

                if cell:
                    bg = cell.background()
                    note = str(cell.toolTip())
                    red, green, blue, _ = bg.color().getRgb()

                    color = f"{red}:{green}:{blue}"
                    cell_cords = f"{row + 1}:{column + 1}"

                    cords_dict[color].append(cell_cords)
                    notes_dict[color] = note

        keys = cords_dict.keys()
        for key in keys:
            start_date = cords_dict[key][0]
            end_date = cords_dict[key][-1]

            cords_dict[key] = list()

            cords_dict[key].append(start_date)
            cords_dict[key].append(end_date)
            cords_dict[key].append(notes_dict[key])
            # now cords_dist looks like this: [key(color):[start_date, end_date, notes]]

            start_date = cords_dict[key][0]
            end_date = cords_dict[key][1]
            notes = cords_dict[key][2]

            cursor.execute(f"SELECT color FROM {self.tableName} WHERE color = ?", (key,))
            check = cursor.fetchone()

            if check is None:
                cursor.execute(f"""SELECT startDate, endDate, color FROM {self.tableName} """)
                check = cursor.fetchall()

                intersection = False

                for date in check:
                    dates = datesExpand.expand_dates(f'{date[0]}-{date[1]}')

                    if (start_date in dates) or (end_date in dates):
                        intersection = True

                if intersection:
                    print("intersection detected, alarm")
                    self.s_data.emit('intersection_alr')

                else:
                    cursor.execute(
                        f"INSERT INTO {self.tableName}(color, startDate, endDate, notes) VALUES(?, ?, ?, ?)",
                        (key, start_date, end_date, notes))
                    connect.commit()

            else:
                self.s_data.emit('alr')

        connect.close()
        self.s_data.emit('cls')


class TableSave(QThread):
    s_data = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.tableName = None
        self.table = None
        self.date = None

    def set(self, table, table_name) -> None:
        self.tableName = table_name
        self.table = table

    def run(self) -> None:
        def standard_save(name_in_db):
            item = cell.text()
            cursor.execute(
                f"UPDATE {self.tableName} SET {name_in_db} = ? WHERE date = ?",
                (item, self.date))
            connect.commit()
            self.s_data.emit('upd')

        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()

        for row in range(self.table.rowCount() - 2):
            for column in range(self.table.columnCount()):
                cell = self.table.item(row, column)
                if cell and row > 1:
                    match column:

                        case 0:
                            self.date = cell.text()
                            cursor.execute(f"SELECT date FROM {self.tableName} WHERE date = ?", (self.date,))
                            db_date = cursor.fetchone()

                            if db_date is None:
                                cursor.execute(f"INSERT INTO {self.tableName}(date) VALUES(?);", (self.date,))

                            connect.commit()
                            self.s_data.emit('upd')

                        case 2:
                            standard_save('price')

                        case 3:
                            standard_save('sum')

                        case 4:
                            standard_save('rent')

                        case 5:
                            standard_save('guest')

                        case 6:
                            standard_save('avito')

                        case 7:
                            standard_save('expense')

                        case 8:
                            standard_save('indications')

                        case 9:
                            standard_save('income')

        connect.close()
        self.s_data.emit('cls')


class TableRead(QThread):
    s_data = QtCore.pyqtSignal(int, int, str)
    w_data = QtCore.pyqtSignal(str, str, str, str, str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.colorVariations = []
        self.tableName = None
        self.table = None
        self.date = None

    def set(self, table_name, table) -> None:
        self.tableName = table_name
        self.table = table

    def insert_dates(self):
        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()

        cursor.execute(f"""SELECT startDate, endDate FROM {self.tableName}""")
        dates = cursor.fetchall()

        if dates is not None:
            for date in dates:
                start_date = date[0]
                end_date = date[1]
                min_month, min_day = start_date.split(':')
                max_month, max_day = end_date.split(':')
                days_count = len(datesExpand.expand_dates(f"{start_date}-{end_date}")) - 1

                self.w_data.emit(min_day, min_month, max_day, max_month, str(days_count))

    def run(self):
        def read(name_in_db, row, column):
            cursor.execute(f"SELECT {name_in_db} FROM {self.tableName} WHERE date = ?", (self.date,))
            db_data = cursor.fetchone()

            if db_data != (None,) and db_data is not None:
                db_data = string_cleaner(db_data)
                self.s_data.emit(row, column, db_data)

        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()

        for row in range(self.table.rowCount() - 2):
            for column in range(self.table.columnCount()):
                cell = self.table.item(row, column)

                if row > 1:
                    match column:

                        case 0:
                            self.date = cell.text()

                        case 2:
                            read('price', row, column)

                        case 3:
                            read('sum', row, column)

                        case 4:
                            read('rent', row, column)

                        case 5:
                            read('guest', row, column)

                        case 6:
                            read('avito', row, column)

                        case 7:
                            read('expense', row, column)

                        case 8:
                            read('indications', row, column)

                        case 9:
                            read('income', row, column)

        connect.close()
