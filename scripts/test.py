# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QButtonGroup
# from PyQt5.QtCore import Qt

# class MultiLayoutExample(QWidget):
#     def __init__(self):
#         super().__init__()
        
#         self.initUI()
        
#     def initUI(self):
#         # Create the main horizontal layout
#         hbox = QHBoxLayout()
        
#         # Create the first vertical layout with varying widgets
#         vbox1 = QVBoxLayout()
#         vbox1.addWidget(QLabel('Label 1'))
#         vbox1.addWidget(QLineEdit('Input 1'))
#         vbox1.addWidget(QPushButton('Button 1'))
        
#         # Create the second vertical layout with varying widgets
#         vbox2 = QVBoxLayout()
#         vbox2.addWidget(QLabel('Label 2'))
#         self.checkboxes1 = []
#         checkbox1_1 = QCheckBox('Checkbox 1.1')
#         checkbox1_1.setProperty('value', 'Value 1.1')
#         checkbox1_2 = QCheckBox('Checkbox 1.2')
#         checkbox1_2.setProperty('value', 'Value 1.2')
#         checkbox1_3 = QCheckBox('Checkbox 1.3')
#         checkbox1_3.setProperty('value', 'Value 1.3')
#         self.checkboxes1.extend([checkbox1_1, checkbox1_2, checkbox1_3])
#         for checkbox in self.checkboxes1:
#             checkbox.stateChanged.connect(self.update_checkboxes1)
#             vbox2.addWidget(checkbox)
#         vbox2.addWidget(QPushButton('Button 2'))
        
#         # Create the third vertical layout with varying widgets
#         vbox3 = QVBoxLayout()
#         vbox3.addWidget(QLabel('Label 3'))
#         vbox3.addWidget(QLineEdit('Input 2'))
#         vbox3.addWidget(QPushButton('Button 3'))
        
#         # Create the fourth vertical layout with varying widgets
#         vbox4 = QVBoxLayout()
#         vbox4.addWidget(QLabel('Label 4'))
#         self.checkboxes2 = []
#         checkbox2_1 = QCheckBox('Checkbox 2.1')
#         checkbox2_1.setProperty('value', 'Value 2.1')
#         checkbox2_2 = QCheckBox('Checkbox 2.2')
#         checkbox2_2.setProperty('value', 'Value 2.2')
#         checkbox2_3 = QCheckBox('Checkbox 2.3')
#         checkbox2_3.setProperty('value', 'Value 2.3')
#         self.checkboxes2.extend([checkbox2_1, checkbox2_2, checkbox2_3])
#         for checkbox in self.checkboxes2:
#             checkbox.stateChanged.connect(self.update_checkboxes2)
#             vbox4.addWidget(checkbox)
#         vbox4.addWidget(QPushButton('Button 4'))
        
#         # Create the fifth vertical layout with varying widgets
#         vbox5 = QVBoxLayout()
#         vbox5.addWidget(QLabel('Label 5'))
#         vbox5.addWidget(QLineEdit('Input 3'))
#         vbox5.addWidget(QPushButton('Button 5'))
        
#         # Add each vertical layout to the horizontal layout
#         hbox.addLayout(vbox1)
#         hbox.addLayout(vbox2)
#         hbox.addLayout(vbox3)
#         hbox.addLayout(vbox4)
#         hbox.addLayout(vbox5)
        
#         # Set the main layout of the window
#         self.setLayout(hbox)
        
#         # Set window title and show the window
#         self.setWindowTitle('Multiple Vertical Layouts in Horizontal Layout')
#         self.show()
    
#     def update_checkboxes1(self, state):
#         if state == Qt.Checked:
#             sender = self.sender()
#             for checkbox in self.checkboxes1:
#                 if checkbox != sender:
#                     checkbox.setChecked(False)
#             self.checked_value1 = sender.property('value')
#             print(f"Checked value in group 1: {self.checked_value1}")

#     def update_checkboxes2(self, state):
#         if state == Qt.Checked:
#             sender = self.sender()
#             for checkbox in self.checkboxes2:
#                 if checkbox != sender:
#                     checkbox.setChecked(False)
#             self.checked_value2 = sender.property('value')
#             print(f"Checked value in group 2: {self.checked_value2}")
    
#     def get_checkbox_value(self, checkbox):
#         return checkbox.isChecked()

# # Main function to run the application
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MultiLayoutExample()
#     sys.exit(app.exec_())
