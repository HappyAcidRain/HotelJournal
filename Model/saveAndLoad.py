from PyQt6 import QtCore
from PyQt6.QtCore import QThread, QDate

import sqlite3


def string_cleaner(str_temp) -> str:
    clean_string = ""
    for i in str_temp:
        clean_string += str(i)
    return clean_string


class CalendarRead(QThread):
    # row, column, color(r, g, b), note
    s_data = QtCore.pyqtSignal(int, int, int, int, int, str)
    s_tables = QtCore.pyqtSignal(list)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.table_name = None

    def set(self, table_name) -> None:
        self.table_name = table_name

    @staticmethod
    def get_tables():
        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()
        cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        table_list = cursor.fetchall()
        return table_list

    def run(self) -> None:
        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()
        cursor.execute(f"SELECT count(*) FROM {self.table_name}")
        count = cursor.fetchone()
        count = int(string_cleaner(count))

        for index in range(count + 1):
            if index != 0:

                # column
                cursor.execute(f"SELECT day FROM {self.table_name} WHERE ROWID = ?", (index,))
                column = cursor.fetchone()
                if column is not None:
                    column = int(string_cleaner(column))

                # row
                cursor.execute(f"SELECT month FROM {self.table_name} WHERE ROWID = ?", (index,))
                row = cursor.fetchone()
                if row is not None:
                    row = int(string_cleaner(row))

                # notes
                cursor.execute(f"SELECT notes FROM {self.table_name} WHERE ROWID = ?", (index,))
                notes = cursor.fetchone()
                if notes is not None:
                    notes = string_cleaner(notes)

                # color
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

                self.s_data.emit(row, column, red, green, blue, notes)

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

    def run(self) -> None:  # TODO: adjust db, add keys, etc.

        cords_list = []
        same_color_items = []

        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()

        for column in range(self.table.columnCount()):
            for row in range(self.table.rowCount()):
                cell = self.table.item(row, column)

                if cell:
                    bg = cell.background()
                    note = str(cell.toolTip())
                    red, green, blue, _ = bg.color().getRgb()

                    color = f"{red}:{green}:{blue}"
                    cell_cords = f"{row}:{column}"

                    cords_list.append([cell_cords, color, note])

        for cur_item in cords_list:
            next_item = cords_list[cords_list.index(cur_item)+1]

            if cur_item[1] == next_item[1]:
                same_color_items.append(f"{cur_item[0]}-{next_item[1]}")
            else:
                pass

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

        cursor.execute(f"""SELECT month FROM {self.tableName} WHERE color = '{color}'""")
        db_month = cursor.fetchall()
        db_month.sort()

        index = 0
        for item in db_month:

            month_temp = ""
            for i in item:
                month_temp += str(i)
            month = int(month_temp)

            db_month[index] = month
            index += 1

        db_month = list(dict.fromkeys(db_month))

        day_list = []

        for month in db_month:
            cursor.execute(f"""SELECT day FROM {self.tableName} WHERE month = {month} AND color = '{color}'""")
            db_day = cursor.fetchall()

            index = 0
            for item in db_day:

                day_temp = ""
                for i in item:
                    day_temp += str(i)
                day = int(day_temp) + 1

                db_day[index] = day
                index += 1

            day_list.append(db_day)

        min_day = day_list[0][0]  # FIX: IndexError: list index out of range
        max_day = day_list[-1][-1]

        min_month = db_month[0] + 1
        max_month = db_month[-1] + 1

        return min_day, min_month, max_day, max_month


def run(self) -> None:
    def standard_read(name_in_db, row, column):
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
                        standard_read('price', row, column)

                    case 3:
                        standard_read('sum', row, column)

                    case 4:
                        standard_read('rent', row, column)

                    case 5:
                        standard_read('guest', row, column)

                    case 6:
                        standard_read('avito', row, column)

                    case 7:
                        standard_read('expense', row, column)

                    case 8:
                        standard_read('indications', row, column)

                    case 9:
                        standard_read('income', row, column)

    connect.close()
