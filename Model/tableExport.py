import pandas
from PyQt6.QtWidgets import QTableWidget


def export(table: QTableWidget) -> str:
    data = {}
    column_name = []

    for column in range(table.columnCount()):
        item = table.item(0, column)

        if item is not None:
            if item.text() != "Оплата":
                column_name.append(item.text())

            else:
                for column in range(1, table.columnCount()):
                    item = table.item(1, column)

                    if item is not None:
                        column_name.append(item.text())

    for column in column_name:
        row_list = []

        for row in range(2, table.rowCount()):

            item = table.item(row, column_name.index(column))
            if item is not None:
                row_list.append(item.text())
            else:
                row_list.append('')

        for _ in row_list:
            data[column] = row_list

    df = pandas.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    df.to_excel('./export.xlsx')

    return "table exported successfully"
