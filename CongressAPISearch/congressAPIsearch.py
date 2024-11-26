import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout, QLineEdit, QVBoxLayout, QScrollArea
import re

api_key = "mnpNTFwOdFJfmUDDESkbMdya23z47J68knYJqKNF"
bills_url = "https://api.congress.gov/v3/bill"

def search_function(result_layout, date_input):

    
    for i in reversed(range(result_layout.count())):
        widget = result_layout.itemAt(i).widget()
        if widget:
            widget.deleteLater()


    date = date_input.text().strip()
    if not date:
        date = None
        info_label = QLabel("No input entered, Fetching the most recent bills.")
        result_layout.addWidget(info_label)

    if date:
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, date):
            error_label = QLabel("Invalid date format. Please use YYYY-MM-DD")
            result_layout.addWidget(error_label)
            return

    bills_params = {
    #'fromDateTime': f'{date}T00:00:00Z',   
    'toDateTime': f"{date}T00:00:00Z" if date else None,
    'format': 'json',
    'offset': None,
    'limit': None,
    'api_key': api_key,
}

    bill_count = 0

    response = requests.get(bills_url, params=bills_params)
    if response.status_code == 200:
        print(response.url)
        data = response.json()
        bills = data.get('bills', '[]')
        if not bills:
            result_label = QLabel(f'No bills found for date: {date}.')
            result_layout.addWidget(result_label)
            return
            
        result_label = QLabel(f"Bills for {date}:")
        result_layout.addWidget(result_label)
        for index, bill in enumerate(bills):
            for key, value in bill.items():
                print(f'{key}: {value}')
                bill_count += 1
            title_label = QLabel(f"{index + 1}. {bill['title']}")
            result_layout.addWidget(title_label)
    else:
        error_label = QLabel(f"Error: {response.status_code} - {response.text}")
        result_layout.addWidget(error_label)
    print(bill_count)

class CongressAPISearch(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        #set the main layout
        main_layout = QVBoxLayout()

        #create the input layout
        input_layout = QGridLayout()

        self.example_label = QLabel("Enter a date (YYYY-MM-DD):")
        input_layout.addWidget(self.example_label, 0, 0)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText('e.g., 2024-01-01')
        input_layout.addWidget(self.date_input, 0, 1)

        self.leave_blank_label = QLabel("Leave blank for most recent bills.")
        input_layout.addWidget(self.leave_blank_label, 1, 0)

        self.search_button = QPushButton('Search')
        input_layout.addWidget(self.search_button, 1, 1)
        main_layout.addLayout(input_layout)


        #results section
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_container.setLayout(self.results_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.results_container)
        main_layout.addWidget(scroll_area)


        self.search_button.clicked.connect(
            lambda: search_function(self.results_layout, self.date_input)
            )

        #set the layout to the main window
        self.setLayout(main_layout)
        self.setWindowTitle("Congress API Search")
        self.setGeometry(100, 100, 400, 300)
        

if __name__ == '__main__':
    app = QApplication([])
    window = CongressAPISearch()
    window.show()
    app.exec()