import os
import sys
import sqlite3
from PyQt5 import QtWidgets
from ui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        base = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base, 'shop.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(['customers', 'products', 'orders'])

        self.ui.pushButton.clicked.connect(self.load_table)
        self.ui.pushButton_2.clicked.connect(self.add_record)
        self.ui.pushButton_3.clicked.connect(self.update_record)
        self.ui.pushButton_4.clicked.connect(self.delete_record)

    def show_error(self, text):
        QtWidgets.QMessageBox.critical(self, 'Ошибка', text)

    def load_table(self):
        try:
            table = self.ui.comboBox.currentText()
            self.cur.execute(f'PRAGMA table_info({table})')
            cols = [row[1] for row in self.cur.fetchall()]
            self.cur.execute(f'SELECT * FROM {table} ORDER BY id')
            rows = self.cur.fetchall()
            self.ui.tableWidget.setRowCount(len(rows))
            self.ui.tableWidget.setColumnCount(len(cols))
            self.ui.tableWidget.setHorizontalHeaderLabels(cols)
            for r, row in enumerate(rows):
                for c, value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.ui.tableWidget.setItem(r, c, item)
        except sqlite3.Error as e:
            self.show_error(str(e))

    def add_record(self):
        try:
            table = self.ui.comboBox.currentText()
            parts = self.ui.lineEdit.text().strip().split()
            if table == 'customers':
                if len(parts) == 3 and parts[0].isdigit():
                    parts = parts[1:]
                name, phone = parts
                self.cur.execute('INSERT INTO customers (name, phone) VALUES (?, ?)', (name, phone))
            elif table == 'products':
                if len(parts) == 3 and parts[0].isdigit():
                    parts = parts[1:]
                title, price = parts
                self.cur.execute('INSERT INTO products (title, price) VALUES (?, ?)', (title, price))
            else:
                if len(parts) == 4 and parts[0].isdigit():
                    parts = parts[1:]
                customer_id, product_id, qty = parts
                self.cur.execute(
                    'INSERT INTO orders (customer_id, product_id, qty) VALUES (?, ?, ?)',
                    (customer_id, product_id, qty),
                )
            self.conn.commit()
            self.load_table()
        except (ValueError, IndexError):
            self.show_error('Неверный ввод')
        except sqlite3.Error as e:
            self.show_error(str(e))

    def update_record(self):
        try:
            table = self.ui.comboBox.currentText()
            parts = self.ui.lineEdit.text().strip().split()
            if table == 'customers':
                item_id, name, phone = parts
                self.cur.execute('UPDATE customers SET name = ?, phone = ? WHERE id = ?', (name, phone, item_id))
            elif table == 'products':
                item_id, title, price = parts
                self.cur.execute('UPDATE products SET title = ?, price = ? WHERE id = ?', (title, price, item_id))
            else:
                item_id, customer_id, product_id, qty = parts
                self.cur.execute(
                    'UPDATE orders SET customer_id = ?, product_id = ?, qty = ? WHERE id = ?',
                    (customer_id, product_id, qty, item_id),
                )
            self.conn.commit()
            self.load_table()
        except (ValueError, IndexError):
            self.show_error('Неверный ввод')
        except sqlite3.Error as e:
            self.show_error(str(e))

    def delete_record(self):
        try:
            table = self.ui.comboBox.currentText()
            item_id = self.ui.lineEdit.text().strip().split()[0]
            self.cur.execute(f'DELETE FROM {table} WHERE id = ?', (item_id,))
            self.conn.commit()
            self.load_table()
        except (ValueError, IndexError):
            self.show_error('Выберите поле для удаления')
        except sqlite3.Error as e:
            self.show_error(str(e))

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
