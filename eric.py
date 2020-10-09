
from PyQt5 import QtGui
from PyQt5.QtGui import QPalette, QTextCharFormat
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QPushButton,
    QMessageBox,
    QLineEdit,
    QLabel,
    QGroupBox,
    QVBoxLayout,
    QRadioButton,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QProgressBar,
    QCalendarWidget,
    QTabWidget,
    QSizePolicy,
    QWidget,
    QTableWidget,
    QTextEdit,
    QTableWidgetItem,
)

import sys
import MySQLdb as mdb
from datetime import datetime
import time 
import requests
import pydash as pydash
 
class Window(QDialog):
    def __init__(self):
        super().__init__()
 
        self.title = "Daily Stock Data"
        self.top = 200
        self.left = 500
        self.width = 1000
        self.height = 800
 
        self.init()
 
 
    def init(self):
        self.createDbInputs()
        self.createApiInputs()
        self.createHedgeInputs()
        self.createTables()

        dbLayout = QHBoxLayout()
        dbLayout.addWidget(self.dbButton)
        dbLayout.addWidget(self.dbLabel)
        dbLayout.addWidget(self.dbInput)
        dbLayout.addWidget(self.userLabel)
        dbLayout.addWidget(self.userInput)
        dbLayout.addWidget(self.pwdLabel)
        dbLayout.addWidget(self.pwdInput)
 
        mainLayout = QGridLayout()
        mainLayout.addLayout(dbLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0, 2, 2)

        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1) 
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def createTables(self):
        print('test')
        self.bottomGroupBox = QGroupBox("Data")
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Ignored)

        tab1 = QWidget()
        historicalTableWidget = QTableWidget(10, 10)

        historicalTableWidget.setRowCount(7)
        historicalTableWidget.setHorizontalHeaderLabels(['Key','Date','Symbol','Open','High','Low','Close','Volume',])

        try:
            db = mdb.connect('localhost', self.userInput.text(), self.pwdInput.text(), self.dbInput.text())
            cursor = db.cursor()
            cursor.execute("Select * FROM " + self.dbInput.text() + ".`historical_data`;")
            
            rows = cursor.fetchall()
            i = 0
            for row in rows:
                historicalTableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))
                historicalTableWidget.setItem(i, 1, QTableWidgetItem(row[1]))
                historicalTableWidget.setItem(i, 2, QTableWidgetItem(row[2]))
                historicalTableWidget.setItem(i, 3, QTableWidgetItem(row[3]))
                historicalTableWidget.setItem(i, 4, QTableWidgetItem(row[4]))
                historicalTableWidget.setItem(i, 5, QTableWidgetItem(row[5]))
                historicalTableWidget.setItem(i, 6, QTableWidgetItem(row[6]))
                historicalTableWidget.setItem(i, 7, QTableWidgetItem(row[7]))
                i+=1
            cursor.close()
            db.commit()
 
        except mdb.Error as e:
            print(e)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(historicalTableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        dailyTableWidget = QTableWidget(10, 10)

        dailyTableWidget.setRowCount(7)
        dailyTableWidget.setHorizontalHeaderLabels(['Key','Date','Symbol','Open','High','Low','Close','Volume',])

        try:
            db = mdb.connect('localhost', self.userInput.text(), self.pwdInput.text(), self.dbInput.text())
            cursor = db.cursor()
            cursor.execute("Select * FROM " + self.dbInput.text() + ".`daily_trades`;")
            
            rows = cursor.fetchall()
            i = 0
            for row in rows:
                dailyTableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))
                dailyTableWidget.setItem(i, 1, QTableWidgetItem(row[1]))
                dailyTableWidget.setItem(i, 2, QTableWidgetItem(row[2]))
                dailyTableWidget.setItem(i, 3, QTableWidgetItem(row[3]))
                dailyTableWidget.setItem(i, 4, QTableWidgetItem(row[4]))
                dailyTableWidget.setItem(i, 5, QTableWidgetItem(row[5]))
                dailyTableWidget.setItem(i, 6, QTableWidgetItem(row[6]))
                dailyTableWidget.setItem(i, 7, QTableWidgetItem(row[7]))
                i+=1
            cursor.close()
            db.commit()
 
        except mdb.Error as e:
            print(e)

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(dailyTableWidget)
        tab2.setLayout(tab2hbox)


        tab3 = QWidget()
        portfolioTableWidget = QTableWidget(10, 10)

        portfolioTableWidget.setRowCount(1)
        portfolioTableWidget.setHorizontalHeaderLabels(['Key', 'Symbol'])

        try:
            db = mdb.connect('localhost', self.userInput.text(), self.pwdInput.text(), self.dbInput.text())
            cursor = db.cursor()
            cursor.execute("Select * FROM " + self.dbInput.text() + ".`portfolio`;")
            
            rows = cursor.fetchall()
            i = 0
            for row in rows:
                portfolioTableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))
                portfolioTableWidget.setItem(i, 1, QTableWidgetItem(row[1]))
                i+=1
            cursor.close()
            db.commit()
 
        except mdb.Error as e:
            print(e)
            
        tab3hbox = QHBoxLayout()
        tab3hbox.setContentsMargins(5, 5, 5, 5)
        tab3hbox.addWidget(portfolioTableWidget)
        tab3.setLayout(tab3hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Historical")
        self.bottomLeftTabWidget.addTab(tab2, "&Daily")
        self.bottomLeftTabWidget.addTab(tab3, "&Portfolio")

    def createHedgeInputs(self):
        self.topRightGroupBox = QGroupBox("Hedge Strategy")

        self.hedgeSymbol = QLabel("Symbol")
        self.hedgeSymbolInput = QLineEdit(self)
        self.hedgeSymbolInput.setText('All')

        self.hedgeCalender = QCalendarWidget(self)
        self.hedgeCalender.setGeometry(100,100,320,270)
        self.hedgeCalender.setGridVisible(True)

        self.begin_date = None
        self.end_date = None
        self.hedgeCalender.highlight_format = QTextCharFormat()
        self.hedgeCalender.highlight_format.setBackground(self.palette().brush(QPalette.Highlight))
        self.hedgeCalender.highlight_format.setForeground(self.palette().color(QPalette.HighlightedText))
        self.hedgeCalender.clicked.connect(self.hedgeDateClicked)

        self.hedgeButton = QPushButton("Perform Backtest Function")
        self.hedgeButton.clicked.connect(self.performBackTest)

        layout = QVBoxLayout()
        layout.addWidget(self.hedgeSymbol)
        layout.addWidget(self.hedgeSymbolInput)
        layout.addWidget(self.hedgeCalender)
        layout.addWidget(self.hedgeButton)
        layout.addStretch(1)

        self.topRightGroupBox.setLayout(layout)

    def performBackTest(self):
        try:
            db = mdb.connect('localhost', self.userInput.text(), self.pwdInput.text(), self.dbInput.text())
            cursor = db.cursor()
            daily_columns = '(`Key` INT NOT NULL AUTO_INCREMENT,`Date` VARCHAR(45) NOT NULL,`Symbol` VARCHAR(45) NOT NULL,`Open` VARCHAR(45) NOT NULL,`High` VARCHAR(45) NOT NULL,`Low` VARCHAR(45) NOT NULL,`Close` VARCHAR(45) NOT NULL,`Volume` VARCHAR(45) NOT NULL,PRIMARY KEY (`Key`), INDEX `portfolio_symbol_idx` (`Symbol` ASC) VISIBLE, CONSTRAINT  `daily_portfolio_symbol` FOREIGN KEY (`Symbol`) REFERENCES ' + self.dbInput.text() + '.`portfolio` (`Symbol`) ON DELETE CASCADE ON UPDATE CASCADE);'
            cursor.execute("create table IF NOT EXISTS " + self.dbInput.text() + '.daily_trades ' + daily_columns)
         
            if self.hedgeSymbolInput.text() == 'All':
                print("Select * FROM " + self.dbInput.text() + ".`historical_data` WHERE `Date` >= '" + str(QDateTime(self.begin_date).currentMSecsSinceEpoch()) + "' AND `Date` <= '" + str(QDateTime(self.end_date).currentMSecsSinceEpoch()) + "';")
                cursor.execute("Select * FROM " + self.dbInput.text() + ".`historical_data` WHERE `Date` >= '" + str(QDateTime(self.begin_date).currentMSecsSinceEpoch()) + "' AND `Date` <= '" + str(QDateTime(self.end_date).currentMSecsSinceEpoch()) + "';")
            else:
                cursor.execute("Select * FROM " + self.dbInput.text() + ".`historical_data` WHERE `Symbol` = '" + self.hedgeSymbolInput.text() + "' AND `Date` >= '" + str(QDateTime(self.begin_date).currentMSecsSinceEpoch()) + "' AND `Date` <= '" + str(QDateTime(self.end_date).currentMSecsSinceEpoch()) + "';")
            
            insert = ''
            print('cursor.fetchall()')
            print(cursor.fetchall())
            for row in cursor.fetchall():
                insert += "INSERT INTO " + self.dbInput.text() + ".`daily_trades` (`Date`,`Symbol`,`Open`,`High`,`Low`,`Close`,`Volume`)"
                insert += "SELECT * FROM (SELECT '" + row[1] + "' as `Date`, '" + row[2] + "' as `Symbol`, '" + row[3] + "' as `Open`,'" + row[4] + "' as `High`,'" + row[5] + "' as `Low`,'" + row[6] + "' as `Close`,'" + row[6] + "' as `Volume`) AS tmp "
                insert += "WHERE NOT EXISTS (SELECT `Date`, `Symbol` FROM " + self.dbInput.text() + ".`daily_trades` WHERE `Date` = '" + row[1] + "' AND `Symbol` = '" + row[2] + "') LIMIT 1;"
            cursor.execute(insert)
            cursor.close()
            db.commit()
            QMessageBox.about(self, 'Connection', 'Backtest Performed Successfully')
 
        except mdb.Error as e:
            print(e)
            QMessageBox.about(self, 'Connection', 'Failed To Performe Backtest')
            sys.exit(1)

    def format_range(self, format):
            print('format', format)
            if self.begin_date and self.end_date:
                d0 = min(self.begin_date, self.end_date)
                d1 = max(self.begin_date, self.end_date)
                while d0 <= d1:
                    print('d0', d0)
                    self.hedgeCalender.setDateTextFormat(d0, format)
                    d0 = d0.addDays(1)

    def hedgeDateClicked(self, date):
            # reset highlighting of previously selected date range
            self.format_range(QTextCharFormat())
            if self.begin_date:
                self.end_date = date
                # set highilighting of currently selected date range
                self.format_range(self.hedgeCalender.highlight_format)
            else:
                self.begin_date = date
                self.end_date = None

            print(self.end_date)
            print(self.begin_date)


    def printDateInfo(self, qDate):
        print('test')
        print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
        print(f'Day Number of the year: {qDate.dayOfYear()}')
        print(f'Day Number of the week: {qDate.dayOfWeek()}') 


    def createApiInputs(self):
        self.topLeftGroupBox = QGroupBox("Enter Daily Data")
        
        self.apiSymbol = QLabel("Symbol")

        self.apiSymbolInput = QLineEdit(self)
        self.apiSymbolInput.setText('IBM')
        
        self.apiKeyLabel = QLabel('Api Key')

        self.apiKeyInput = QLineEdit(self)
        self.apiKeyInput.setText('YHMY1XSUQCUM8Z2T')

        # self.apiProgressBar = QProgressBar(self)
        # self.apiProgressBar.setGeometry(200, 80, 250, 20)
        
        self.apiButton = QPushButton("Fetch Today's Data " + str(datetime.today().strftime('%m/%d/%Y')))
        self.apiButton.clicked.connect(self.fetchData)

        layout = QVBoxLayout()
        layout.addWidget(self.apiSymbol)
        layout.addWidget(self.apiSymbolInput)
        layout.addWidget(self.apiKeyLabel)
        layout.addWidget(self.apiKeyInput)
        # layout.addWidget(self.apiProgressBar)
        layout.addWidget(self.apiButton)
        layout.addStretch(1)
        
        self.topLeftGroupBox.setLayout(layout) 
 
    def createDbInputs(self):
        self.dbButton = QPushButton('DB Connection', self)
        self.dbButton.setGeometry(10, 10, 200, 50)
        self.dbButton.clicked.connect(self.DBConnection)

        self.dbLabel = QLabel(self)
        self.dbLabel.setText('Database: ')
        
        self.dbInput = QLineEdit(self)
        self.dbInput.setText('backtester')

        self.userLabel = QLabel(self)
        self.userLabel.setText('User: ')
        
        self.userInput = QLineEdit(self)
        self.userInput.setText('root')
        
        self.pwdLabel = QLabel(self)
        self.pwdLabel.setText('Password: ')
        
        self.pwdInput = QLineEdit(self)
        self.pwdInput.setText('root')
        self.pwdInput.setEchoMode(QLineEdit.Password)

    def fetchData(self):
        try:
            client_id = '6PML9SNDDS4UV2SRA5ASTV5BBKF6DSX9'

            endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(self.apiSymbolInput.text())

            # define the payload
            now = int(round(time.time() * 1000))
            yesterday = now - 86400000
            payload = {'apikey':client_id,
                    'periodType':'day',
                    'frequencyType':'minute',
                    'frequency':'1',
                    'endDate': str(now),
                    'startDate': str(yesterday)
                    }

            # make a request
            content = requests.get(url = endpoint, params = payload)

            # convert it dictionary object
            data = content.json()
            # query = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + self.apiSymbolInput.text() + "&outputsize=full&interval=1min&apikey=" + self.apiKeyInput.text()
            # print(query)
            # response = requests.get(query)
            # date = str(datetime.today().strftime('%Y-%m-%d'))
            # date = '2020-04-09'
            self.data = content.json()

            db = mdb.connect('localhost', self.userInput.text(), self.pwdInput.text(), self.dbInput.text())
            cursor = db.cursor()
            
            portfolio_columns = '(`Key` INT NOT NULL AUTO_INCREMENT,`Symbol` VARCHAR(45) NOT NULL,UNIQUE INDEX `Key_UNIQUE` (`Key` ASC) VISIBLE,PRIMARY KEY (`Symbol`));'
            cursor.execute("create table IF NOT EXISTS " + self.dbInput.text() + '.portfolio ' + portfolio_columns)
            cursor.execute("INSERT IGNORE INTO " + self.dbInput.text() + ".`portfolio`(`Symbol`) VALUES('" + self.apiSymbolInput.text() + "');")

            historical_columns = '(`Key` INT NOT NULL AUTO_INCREMENT,`Date` VARCHAR(45) NOT NULL,`Symbol` VARCHAR(45) NOT NULL,`Open` VARCHAR(45) NOT NULL,`High` VARCHAR(45) NOT NULL,`Low` VARCHAR(45) NOT NULL,`Close` VARCHAR(45) NOT NULL,`Volume` VARCHAR(45) NOT NULL,PRIMARY KEY (`Key`), INDEX `portfolio_symbol_idx` (`Symbol` ASC) VISIBLE, CONSTRAINT  `portfolio_symbol` FOREIGN KEY (`Symbol`) REFERENCES ' + self.dbInput.text() + '.`portfolio` (`Symbol`) ON DELETE CASCADE ON UPDATE CASCADE);'
            cursor.execute("create table IF NOT EXISTS " + self.dbInput.text() + '.historical_data ' + historical_columns)

            insert = ''
            insert = ''
            # print(response.json())
            # print(self.data)
            print(type(self.data))
            for item in self.data['candles']:
                insert += "INSERT INTO " + self.dbInput.text() + ".`historical_data` (`Date`,`Symbol`,`Open`,`High`,`Low`,`Close`,`Volume`)"
                insert += "SELECT * FROM (SELECT '" + str(item['datetime']) + "' as `Date`, '" + self.apiSymbolInput.text() + "' as `Symbol`, '" + str(item['open']) + "' as `Open`,'" + str(item['high']) + "' as `High`,'" + str(item['low']) + "' as `Low`,'" + str(item['close']) + "' as `Close`,'" + str(item['volume']) + "' as `Volume`) AS tmp "
                insert += "WHERE NOT EXISTS (SELECT `Date`, `Symbol` FROM " + self.dbInput.text() + ".`historical_data` WHERE `Date` = '" + str(item['datetime']) + "' AND `Symbol` = '" + self.apiSymbolInput.text() + "') LIMIT 1;"
            cursor.execute(insert)
            cursor.close()
            db.commit()
                
            QMessageBox.about(self, 'Data Fetch', 'Data Loaded Successfully')

        except requests.exceptions.RequestException as e:
            print(e)
            QMessageBox.about(self, 'Data Fetch', 'Failed To Fetch Data')
            sys.exit(1)




    def DBConnection(self):
        try:
            db = mdb.connect('localhost', self.userInput.text(), self.pwdInput.text())
            cursor = db.cursor()
            cursor.execute("create database IF NOT EXISTS " + self.dbInput.text())
            QMessageBox.about(self, 'Connection', 'Database Connected Successfully')
 
        except mdb.Error as e:
            print(e)
            QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
            sys.exit(1)
 
 
 
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
