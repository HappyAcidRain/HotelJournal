from PyQt6 import QtCore
from PyQt6.QtCore import QThread

import sqlite3


def string_cleaner(str_temp) -> str:
    clean_string = ""
    for i in str_temp:
        clean_string += str(i)
    return clean_string


class ReadThread(QThread):
    # row, column, color(r, g, b), note
    s_data = QtCore.pyqtSignal(int, int, int, int, int, str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.table_name = None

    def set(self, table_name) -> None:
        self.table_name = table_name

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

                if column is None:
                    return

                column = int(string_cleaner(column))

                cursor.execute(f"SELECT month FROM {self.table_name} WHERE ROWID = ?", (index,))
                row = cursor.fetchone()
                row = int(string_cleaner(row))

                # notes
                cursor.execute(f"SELECT notes FROM {self.table_name} WHERE ROWID = ?", (index,))
                notes = cursor.fetchone()

                if notes is None:  # check really it needs or not
                    notes = None
                else:
                    notes = string_cleaner(notes)

                # color
                cursor.execute(f"SELECT color FROM {self.table_name} WHERE ROWID = ?", (index,))
                color = cursor.fetchone()

                if color is None:
                    red = None
                    green = None
                    blue = None

                else:
                    color = string_cleaner(color)

                    color = color.split(":")
                    red = int(color[0])
                    green = int(color[1])
                    blue = int(color[2])

                self.s_data.emit(row, column, red, green, blue, notes)


class SaveThread(QThread):
    s_update = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.tableName = None
        self.table = None

    def set(self, table_name, table) -> None:
        self.tableName = table_name
        self.table = table

    def run(self) -> None:
        connect = sqlite3.connect("Model/Database/people.db")
        cursor = connect.cursor()

        for column in range(self.table.columnCount()):
            for row in range(self.table.rowCount()):
                cell = self.table.item(row, column)

                if cell:
                    bg = cell.background()
                    note = cell.toolTip()

                    red, green, blue, _ = bg.color().getRgb()
                    color = f"{red}:{green}:{blue}"

                    row_and_column = f"{row}:{column}"

                    cursor.execute(f"SELECT rowAndColumn FROM {self.tableName} WHERE rowAndColumn = ?",
                                   (row_and_column,))

                    db_row_and_column = cursor.fetchone()

                    if db_row_and_column is None:
                        cursor.execute(f"""INSERT INTO {self.tableName}(rowAndColumn, notes, color, day, month)
                                            VALUES(?, ?, ?, ?, ?);""",
                                       (row_and_column, note, color, column, row))

                        connect.commit()
                        self.s_update.emit('upd')

                    else:
                        cursor.execute(f"UPDATE {self.tableName} SET notes = ? WHERE rowAndColumn = ?",
                                       (note, row_and_column))

                        cursor.execute(f"UPDATE {self.tableName} SET color = ? WHERE rowAndColumn = ?",
                                       (color, row_and_column))

                        cursor.execute(f"UPDATE {self.tableName} SET day = ? WHERE rowAndColumn = ?",
                                       (column, row_and_column))

                        cursor.execute(f"UPDATE {self.tableName} SET month = ? WHERE rowAndColumn = ?",
                                       (row, row_and_column))

                        connect.commit()
                        self.s_update.emit('upd')

                else:

                    row_and_column = f"{row}:{column}"

                    cursor.execute(f"SELECT rowAndColumn FROM {self.tableName} WHERE rowAndColumn = ?",
                                   (row_and_column,))

                    db_row_and_column = cursor.fetchone()

                    if db_row_and_column is not None:
                        cursor.execute(f"DELETE FROM {self.tableName} WHERE rowAndColumn = ?",
                                       (row_and_column,))

        connect.close()
        self.s_update.emit('cls')


class SaveReportThread(QThread):
    s_updPB = QtCore.pyqtSignal(str)

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
            cursor.execute(f"UPDATE {self.tableName} SET {name_in_db} = ? WHERE date = ?",
                           (item, self.date))

            connect.commit()
            self.s_updPB.emit('upd')

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
                            self.s_updPB.emit('upd')

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
        self.s_updPB.emit('cls')


class ReadReportThread(QThread):
    s_readData = QtCore.pyqtSignal(int, int, str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.tableName = None
        self.table = None
        self.date = None

    def set(self, table_name, table) -> None:
        self.tableName = table_name
        self.table = table

    def run(self) -> None:
        def standard_read(name_in_db, row, column):
            cursor.execute(f"SELECT {name_in_db} FROM {self.tableName} WHERE date = ?", (self.date,))
            db_data = cursor.fetchone()

            if db_data != (None,) and db_data is not None:
                db_data = string_cleaner(db_data)
                self.s_readData.emit(row, column, db_data)

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
