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

        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT NOT NULL)'
        )
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, price REAL NOT NULL)'
        )
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL, qty INTEGER NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)'
        )
        self.conn.commit()

        self.cur.execute('SELECT COUNT(*) FROM customers')
        if self.cur.fetchone()[0] == 0:
            self.cur.executemany(
                'INSERT INTO customers (name, phone) VALUES (?, ?)',
                [('Ivanov', '79001234567'), ('Petrova', '79007654321')],
            )
            self.conn.commit()

        self.cur.execute('SELECT COUNT(*) FROM products')
        if self.cur.fetchone()[0] == 0:
            self.cur.executemany(
                'INSERT INTO products (title, price) VALUES (?, ?)',
                [('Notebook', 1200), ('Mouse', 700)],
            )
            self.conn.commit()

        self.cur.execute('SELECT COUNT(*) FROM orders')
        if self.cur.fetchone()[0] == 0:
            self.cur.executemany(
                'INSERT INTO orders (customer_id, product_id, qty) VALUES (?, ?, ?)',
                [(1, 1, 2), (2, 2, 1)],
            )
            self.conn.commit()

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(['customers', 'products', 'orders'])

        self.ui.pushButton.clicked.connect(self.load_table)
        self.ui.pushButton_2.clicked.connect(self.add_record)
        self.ui.pushButton_3.clicked.connect(self.update_record)
        self.ui.pushButton_4.clicked.connect(self.delete_record)

    def load_table(self):
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

    def add_record(self):
        table = self.ui.comboBox.currentText()
        parts = self.ui.lineEdit.text().strip().split()
        if not parts:
            return
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

    def update_record(self):
        table = self.ui.comboBox.currentText()
        parts = self.ui.lineEdit.text().strip().split()
        if not parts:
            return
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

    def delete_record(self):
        table = self.ui.comboBox.currentText()
        item_id = self.ui.lineEdit.text().strip().split()[0]
        self.cur.execute(f'DELETE FROM {table} WHERE id = ?', (item_id,))
        self.conn.commit()
        self.load_table()

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
