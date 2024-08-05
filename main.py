import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QDialog, QFormLayout 
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class PersonalFinanceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Manager")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.date_label = QLabel("Date:")
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")

        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Enter a description")

        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter an amount")

        self.category_label = QLabel("Category:")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Enter a category")

        self.tag_label = QLabel("Tags (comma-separated):")
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Enter tags")

        self.add_transaction_button = QPushButton("Add Transaction")
        self.add_transaction_button.clicked.connect(self.add_transaction)
        self.add_transaction_button.setEnabled(False)

        self.view_transactions_button = QPushButton("View Transactions")
        self.view_transactions_button.clicked.connect(self.view_transactions)
        self.view_transactions_button.setEnabled(False)

        self.generate_monthly_report_button = QPushButton("Generate Monthly Report")
        self.generate_monthly_report_button.clicked.connect(self.generate_monthly_report)
        self.generate_monthly_report_button.setEnabled(False)

        self.generate_yearly_report_button = QPushButton("Generate Yearly Report")
        self.generate_yearly_report_button.clicked.connect(self.generate_yearly_report)
        self.generate_yearly_report_button.setEnabled(False)

        self.generate_expense_report_button = QPushButton("Expense Report")
        self.generate_expense_report_button.clicked.connect(self.generate_expense_report)
        self.generate_expense_report_button.setEnabled(False)

        self.transaction_list = QListWidget()

        layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.username_label)
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_label)
        input_layout.addWidget(self.password_input)
        input_layout.addWidget(self.login_button)
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.description_label)
        input_layout.addWidget(self.description_input)
        input_layout.addWidget(self.amount_label)
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.category_label)
        input_layout.addWidget(self.category_input)
        input_layout.addWidget(self.tag_label)
        input_layout.addWidget(self.tag_input)
        input_layout.addWidget(self.add_transaction_button)
        input_layout.addWidget(self.view_transactions_button)
        input_layout.addWidget(self.generate_monthly_report_button)
        input_layout.addWidget(self.generate_yearly_report_button)
        input_layout.addWidget(self.generate_expense_report_button)

        layout.addLayout(input_layout)
        layout.addWidget(self.transaction_list)

        self.central_widget.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="daniyagarg",
                    database="personal_finance_manager"
                )

                cursor = db.cursor()

                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                user_id = cursor.fetchone()

                if user_id:
                    self.user_id = user_id[0]
                    self.add_transaction_button.setEnabled(True)
                    self.view_transactions_button.setEnabled(True)
                    self.generate_monthly_report_button.setEnabled(True)
                    self.generate_yearly_report_button.setEnabled(True)
                    self.generate_expense_report_button.setEnabled(True)
                else:
                    print("User not found.")

                cursor.close()
                db.close()
            except Exception as e:
                print("Error:", str(e))
        else:
            print("Please enter username and password.")

    def add_transaction(self):
        date = self.date_input.text()
        description = self.description_input.text()
        amount = self.amount_input.text()
        category = self.category_input.text()
        tags = self.tag_input.text().split(",")

        if date and description and amount and category and tags:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="daniyagarg",
                    database="personal_finance_manager"
                )

                cursor = db.cursor()

                tags_str = ",".join(tags)

                cursor.execute("INSERT INTO transactions (user_id, date, description, amount, category, tags) VALUES (%s, %s, %s, %s, %s, %s)",
                            (self.user_id, date, description, amount, category, tags_str))
                db.commit()

                cursor.close()
                db.close()

                self.transaction_list.addItem(f"{date}: {description} - {amount} - {category} - {tags_str}")

                self.date_input.clear()
                self.description_input.clear()
                self.amount_input.clear()
                self.category_input.clear()
                self.tag_input.clear()

            except Exception as e:
                print("Error:", str(e))
        else:
            print("Please fill in all fields.")

    def view_transactions(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="daniyagarg",
                database="personal_finance_manager"
            )

            cursor = db.cursor()

            cursor.execute("SELECT date, description, amount, category, tags FROM transactions WHERE user_id = %s", (self.user_id,))
            transactions = cursor.fetchall()

            cursor.close()
            db.close()

            self.transaction_list.clear()
            for transaction in transactions:
                date, description, amount,category,tags = transaction
                self.transaction_list.addItem(f"{date}: {description} - {amount} - {category} - {tags}")

            income = sum([transaction[2] for transaction in transactions if transaction[2] > 0])
            expenses = abs(sum([transaction[2] for transaction in transactions if transaction[2] < 0]))

            labels = ['Income', 'Expenses']
            sizes = [income, expenses]
            colors = ['lightgreen', 'lightcoral']
            plt.figure(figsize=(8, 6))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')  
            plt.title('Income vs. Expenses')
            plt.show()

        except Exception as e:
            print("Error:", str(e))

    
    def generate_monthly_report(self):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Generate Monthly Report")
            layout = QFormLayout()

            month_combo = QComboBox()
            year_combo = QComboBox()

            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            years = ["2019", "2020", "2021", "2022", "2023"]  

            month_combo.addItems(months)
            year_combo.addItems(years)

            layout.addRow("Select Month:", month_combo)
            layout.addRow("Select Year:", year_combo)

            generate_button = QPushButton("Generate Report")
            layout.addWidget(generate_button)

            dialog.setLayout(layout)

            def generate_report():
                selected_month = month_combo.currentText()
                selected_year = year_combo.currentText()

                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="daniyagarg",
                    database="personal_finance_manager"
                )

                cursor = db.cursor()

                cursor.execute("SELECT date, description, amount, category, tags FROM transactions WHERE user_id = %s AND MONTH(date) = %s AND YEAR(date) = %s", (self.user_id, months.index(selected_month) + 1, int(selected_year)))
                transactions = cursor.fetchall()

                cursor.close()
                db.close()

                if transactions:
                    report_text = f"Monthly Report for {selected_month} {selected_year}:\n"
                    income = 0
                    expenses = 0

                    for transaction in transactions:
                        date, description, amount, category, tags = transaction
                        report_text += f"{date}: {description} - {amount} - {category} - {tags}\n"

                        if amount > 0:
                            income += amount
                        else:
                            expenses += abs(amount)

                    report_text += f"Total Income: {income}\n"
                    report_text += f"Total Expenses: {expenses}\n"
                    report_text += f"Net Income: {income - expenses}\n"

                    labels = ['Income', 'Expenses']
                    sizes = [income, expenses]
                    colors = ['lightgreen', 'lightcoral']
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
                    ax.axis('equal')  
                    ax.set_title('Income vs. Expenses')

                    report_window = QDialog(self)
                    report_window.setWindowTitle("Monthly Report")
                    report_layout = QVBoxLayout()
                    canvas = FigureCanvas(fig)
                    report_layout.addWidget(canvas)

                    report_label = QLabel(report_text)
                    report_layout.addWidget(report_label)

                    report_window.setLayout(report_layout)
                    report_window.exec_()

                else:
                    print("No transactions found for the selected month and year.")

            generate_button.clicked.connect(generate_report)

            dialog.exec_()

        except Exception as e:
            print("Error:", str(e))

    def generate_yearly_report(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="daniyagarg",
                database="personal_finance_manager"
            )

            cursor = db.cursor()

            cursor.execute("SELECT date, description, amount, category, tags FROM transactions WHERE user_id = %s AND YEAR(date) = YEAR(CURDATE())", (self.user_id,))
            transactions = cursor.fetchall()

            cursor.close()
            db.close()

            if transactions:
                report_text = "Yearly Report:\n"
                income = 0
                expenses = 0

                dates = []
                net_incomes = []

                for transaction in transactions:
                    date, description, amount, category, tags = transaction
                    report_text += f"{date}: {description} - {amount} - {category} - {tags}\n"

                    if amount > 0:
                        income += amount
                    else:
                        expenses += abs(amount)
                    dates.append(date)
                    net_incomes.append(income - expenses)

                report_text += f"Total Income: {income}\n"
                report_text += f"Total Expenses: {expenses}\n"
                report_text += f"Net Income: {income - expenses}\n"

                report_window = QWidget()  
                report_window.setWindowTitle("Yearly Report")
                report_label = QLabel(str(report_text))
                report_layout = QVBoxLayout()
                report_layout.addWidget(report_label)

                # Create a figure and add a line chart
                figure = Figure()
                canvas = FigureCanvas(figure)
                report_layout.addWidget(canvas)

                # Plot the line chart
                ax = figure.add_subplot(111)
                ax.plot(dates, net_incomes, marker='o', linestyle='-')
                ax.set_xlabel('Date')
                ax.set_ylabel('Net Income')
                ax.set_title('Yearly Net Income')
                ax.grid(True)

                report_window.setLayout(report_layout)
                report_window.show()

                # Keep a reference to the report window
                self.report_window = report_window

            else:
                print("No transactions found for the current year.")

        except Exception as e:
            print("Error:", str(e))

    def generate_expense_report(self):
        try:
            # Connect to the MySQL database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="daniyagarg",
                database="personal_finance_manager"
            )

            cursor = db.cursor()

            # Retrieve transactions from the database for the logged-in user for the current year
            cursor.execute("SELECT date, description, amount, category, tags FROM transactions WHERE user_id = %s AND YEAR(date) = YEAR(CURDATE())", (self.user_id,))
            transactions = cursor.fetchall()

            cursor.close()
            db.close()

            # Create a yearly report
            if transactions:
                report_text = "Yearly Report:\n"
                income = 0
                expenses = 0

                # Create dictionaries to store expenses by category
                expenses_by_category = {}

                dates = []
                net_incomes = []

                for transaction in transactions:
                    date, description, amount, category, tags = transaction
                    report_text += f"{date}: {description} - {amount} - {category} - {tags}\n"

                    if amount > 0:
                        income += amount
                    else:
                        expenses += abs(amount)
                        # Update expenses by category
                        if category not in expenses_by_category:
                            expenses_by_category[category] = 0
                        expenses_by_category[category] += abs(amount)

                    dates.append(date)
                    net_incomes.append(income - expenses)

                report_text += f"Total Income: {income}\n"
                report_text += f"Total Expenses: {expenses}\n"
                report_text += f"Net Income: {income - expenses}\n"

                # Display the report in a separate window or save it to a file
                report_window = QWidget()  # Set the main window as the parent
                report_window.setWindowTitle("Expense Report")
                report_label = QLabel(str(report_text))
                report_layout = QVBoxLayout()
                report_layout.addWidget(report_label)

                # Create a figure and add both line and bar charts
                figure = Figure()
                canvas = FigureCanvas(figure)
                report_layout.addWidget(canvas)

                # Create subplots for line chart and bar chart
                ax2 = figure.add_subplot(212)  # Bar chart

                # Plot the bar chart for expenses by category
                categories = list(expenses_by_category.keys())
                expense_amounts = list(expenses_by_category.values())
                ax2.bar(categories, expense_amounts, color='red')
                ax2.set_xlabel('Expense Categories')
                ax2.set_ylabel('Expense Amount')
                ax2.set_title('Yearly Expenses by Category')
                ax2.grid(True)
                ax2.tick_params(axis='x', rotation=45)

                report_window.setLayout(report_layout)
                report_window.show()

                # Keep a reference to the report window
                self.report_window = report_window

            else:
                print("No transactions found for the current year.")

        except Exception as e:
            print("Error:", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PersonalFinanceManager()
    window.show()
    sys.exit(app.exec_())

