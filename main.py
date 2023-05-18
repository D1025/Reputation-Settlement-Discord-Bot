import sys
from PySide6 import QtCore, QtWidgets, QtGui
from functools import partial
import sqlite3
import paiting
import nextcord



class Module(QtWidgets.QWidget):
    def __init__(self, name, channel_ip, url):
        super().__init__()
        
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        c.execute("SELECT s.reputation, s.population, s.food, s.outlook , s.defences FROM settlements s, ch_set c WHERE s.name = ? AND c.channel_id = ? AND c.settlement_id = s.id", (name, channel_ip))
        settle = c.fetchone()
        print(settle)
        if not settle:
            c.execute("INSERT INTO settlements (name, reputation, population, food, outlook, defences) VALUES(?, ?, ?, ?,?,?)", (name, 2, str(4), 2, 2, 0))
            c.execute("INSERT INTO ch_set (channel_id, settlement_id, message_id) VALUES (?, ?, ?)", (channel_ip, c.lastrowid, 0))
            conn.commit()
            c.execute("SELECT s.reputation, s.population, s.food, s.outlook, s.defences FROM settlements s, ch_set c WHERE s.name = ? AND c.channel_id = ? AND c.settlement_id = s.id", (name, channel_ip))
            settle = c.fetchone()
        conn.close()
        print(settle)
        

        self.name = name
        self.channel = channel_ip

        self.module_entries = []

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.module_values = QtWidgets.QLabel()
        layout.addWidget(self.module_values)
        lebeltext = ["Population", "Food Supply", "Denizen Outlook", "Defences"]
        for _ in range(4):
            label = QtWidgets.QLabel(lebeltext[_])
            layout.addWidget(label)
            entry = QtWidgets.QLineEdit()
            entry.textChanged.connect(self.update_values)
            self.module_entries.append(entry)
            layout.addWidget(entry)
        for i in range(4):
            self.module_entries[i].setText(str(settle[i+1]))

        image_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(image_layout)

        self.image_paths_low = [
            "data/radiobutton/low_image_1.png",
            "data/radiobutton/low_image_2.png",
            "data/radiobutton/low_image_3.png",
            "data/radiobutton/low_image_4.png",
            "data/radiobutton/low_image_5.png",
            "data/radiobutton/low_image_6.png",
        ]

        self.image_paths_high = [
            "data/radiobutton/high_image_1.png",
            "data/radiobutton/high_image_2.png",
            "data/radiobutton/high_image_3.png",
            "data/radiobutton/high_image_4.png",
            "data/radiobutton/high_image_5.png",
            "data/radiobutton/high_image_6.png",
        ]

        self.buttons = []
        self.checked = settle[0]

        for i in range(6):
            button = QtWidgets.QPushButton()
            button.setFixedSize(30, 30)
            if i == self.checked:
                button.setIcon(QtGui.QIcon(self.image_paths_high[i]))
            else:
                button.setIcon(QtGui.QIcon(self.image_paths_low[i]))
            button.setIconSize(QtCore.QSize(30, 30))
            button.clicked.connect(partial(self.set_button_state, i))
            image_layout.addWidget(button)
            self.buttons.append(button)

        push_button = QtWidgets.QPushButton("Push")
        push_button.setMaximumWidth(400)  # Set maximum width
        push_button.clicked.connect(self.push_values)
        layout.addWidget(push_button)

        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
                padding: 5px;
                margin-bottom: 5px;
            }

            QLabel {
                color: #333333;
                font-weight: bold;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                padding: 3px;
            }

            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        push_button.setStyleSheet("""
                QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: none;
            }

            QPushButton:hover {
                background-color: #45a049;
            }""")

    def push_values(self):
        values = [entry.text() for entry in self.module_entries]
        print(f"{self.name} values:", values)
        
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        c.execute("SELECT message_id, settlement_id FROM ch_set WHERE channel_id = ? AND settlement_id = (SELECT s.id FROM settlements s, ch_set c WHERE c.channel_id = ? AND s.name = ? AND c.settlement_id = s.id)", (self.channel, self.channel, self.name))
        message = c.fetchone()
        print(message)
        c.execute("SELECT ch.name, ch.url FROM channels ch, ch_set c WHERE c.settlement_id = ? AND ch.id = c.channel_id", (message[1],))
        essentian = c.fetchone()
        webhook = nextcord.SyncWebhook.from_url(essentian[1])
        paiting.createImage(int(self.checked), self.name, values[0], int(values[1]), int(values[2]), int(values[3]), essentian[0])
        if message[0] == 0:
            f = webhook.send("", file=nextcord.File(f'data/temp/{essentian[0]}_{self.name}.png'), wait=True)
            c.execute("UPDATE ch_set SET message_id = ? WHERE settlement_id = ?", (int(f.id),message[1]))
            conn.commit()
        else:
            webhook.edit_message(message[0], file=nextcord.File(f'data/temp/{essentian[0]}_{self.name}.png'))
        c.execute("UPDATE settlements SET reputation = ?, population = ?, food = ?, outlook = ?, defences = ? WHERE id = ?", (self.checked, values[0], int(values[1]), int(values[2]), int(values[3]), message[1]))
        conn.commit()
        conn.close()

        
        
        
        
        
        
        

    def update_values(self):
        values = [entry.text() for entry in self.module_entries]
        self.module_values.setText(f"{self.name} values: " + ", ".join(values))

    def set_button_state(self, index):
        print(index)
        self.checked = index
        for i, button in enumerate(self.buttons):
            if i == index:
                button.setIcon(QtGui.QIcon(self.image_paths_high[i]))
            else:
                button.setIcon(QtGui.QIcon(self.image_paths_low[i]))


class MainWindow(QtWidgets.QWidget):
    def __init__(self, channel_id):
        super().__init__()
        
        
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM channels WHERE id = ?", (channel_id,))
        channel = c.fetchall()
        # if not c.fetchone():
            
        #     c.execute("INSERT INTO channels(id) VALUES (?)", (channel_id,))
        #     conn.commit()
        conn.close()
        

        self.module_widgets = []

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.left_module = QtWidgets.QWidget()
        self.left_module.setMaximumWidth(200)
        layout.addWidget(self.left_module)

        left_layout = QtWidgets.QVBoxLayout()
        self.left_module.setLayout(left_layout)

        self.module_list = QtWidgets.QListWidget()
        self.module_list.setStyleSheet("""
            QListWidget {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
                padding: 5px;
            }

            QListWidget::item {
                background-color: white;
                padding: 5px;
            }

            QListWidget::item:selected {
                background-color: #DDDDDD;
            }
        """)
        left_layout.addWidget(self.module_list)

        self.module_list.itemClicked.connect(self.select_module)

        input_text = QtWidgets.QLineEdit()
        input_text.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                padding: 3px;
            }
        """)
        left_layout.addWidget(input_text)

        add_module_button = QtWidgets.QPushButton("Add Module")
        add_module_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: none;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        print(channel, channel_id)
        add_module_button.clicked.connect(lambda: self.add_module(input_text.text(), input_text, channel_id, channel[0][2]))
        left_layout.addWidget(add_module_button)

        self.right_module = QtWidgets.QWidget()
        layout.addWidget(self.right_module)

        self.module_stack = QtWidgets.QStackedWidget()
        right_layout = QtWidgets.QVBoxLayout()
        self.right_module.setLayout(right_layout)
        right_layout.addWidget(self.module_stack)
        
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        c.execute("SELECT s.name, ch.url  FROM settlements s, ch_set c, channels ch WHERE c.channel_id = ? AND s.id = c.settlement_id AND ch.id=c.channel_id", (channel_id,))
        settlements = c.fetchall()
        conn.close()
        print(settlements)
        for settle in settlements:
            self.add_module(settle[0],input_text,channel_id, settle[1])
        
        

    def add_module(self, module_name, input_text, channel_id, url):
        module = Module(module_name, channel_id, url)
        self.module_widgets.append(module)
        module_item = QtWidgets.QListWidgetItem(module_name)
        self.module_list.addItem(module_item)
        self.module_stack.addWidget(module)
        input_text.setText('')

    def select_module(self, item):
        index = self.module_list.row(item)
        if index < self.module_stack.count():
            self.module_stack.setCurrentIndex(index)


class AdditionalWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        label = QtWidgets.QLabel("Main Window")
        layout.addWidget(label)

        conn = sqlite3.connect("data/database.db")
        c = conn.cursor()
        c.execute("SELECT name FROM channels")
        names = c.fetchall()
        flat_names = [item for sublist in names for item in sublist]
        

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(flat_names)
        self.combo_box.setStyleSheet("""
    QComboBox {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
        padding: 5px;
        min-width: 150px;
        font-size: 12px;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left-width: 1px;
        border-left-color: #CCCCCC;
        border-left-style: solid;
        background: #F0F0F0;
    }

    QComboBox QAbstractItemView {
        border: 1px solid #CCCCCC;
        selection-background-color: #DDDDDD;
    }
""")
        layout.addWidget(self.combo_box)

        button = QtWidgets.QPushButton("Connect")
        button.clicked.connect(self.go_back)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: none;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(button)
        
        label1 = QtWidgets.QLabel("Name:")
        layout.addWidget(label1)

        self.name = QtWidgets.QLineEdit()
        layout.addWidget(self.name)
        
        label2 = QtWidgets.QLabel("Url:")
        layout.addWidget(label2)
        self.url = QtWidgets.QLineEdit()
        layout.addWidget(self.url)
        
        addelement = QtWidgets.QPushButton("Add")
        addelement.clicked.connect(self.showAddWindow)
        addelement.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: none;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(addelement)
        

    def go_back(self):
        mainwindow = MainWindow(self.combo_box.currentIndex()+1)
        mainwindow.show()
        self.close()
        
    def showAddWindow(self):
        if self.url.text() == "" or self.name.text() == "":
            return
        conn = sqlite3.connect("data/database.db")
        c = conn.cursor()
        c.execute("INSERT INTO channels(name, url) VALUES(? , ?)", (self.name.text(), self.url.text()))
        conn.commit()
        c.execute("SELECT name FROM channels")
        names = c.fetchall()
        flat_names = [item for sublist in names for item in sublist]
        self.combo_box.clear()
        self.combo_box.addItems(flat_names)
        conn.close()
        
        


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    additional_window = AdditionalWindow()
    additional_window.show()

    sys.exit(app.exec())
