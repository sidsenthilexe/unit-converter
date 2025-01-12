import sys

from PySide6.QtCore import (QSize, Qt,)
from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QComboBox, QHBoxLayout, QLineEdit, QLabel,)

conversion_factors = {
    # imperial distances
    ("inches", "feet"): 1/12,
    ("feet", "inches"): 12,
    ("feet", "miles"): 1/5280,
    ("miles", "feet"): 5280,

    # imperial weights
    ("pounds", "ounces"): 16,
    ("ounces", "pounds"): 1/16,

    # metric distances
    ("centimetres", "metres"): 1/100,
    ("metres", "centimetres"): 100,
    ("metres", "kilometres"): 1/1000,
    ("kilometres", "metres"): 1000,

    # metric weights
    ("grams", "kilograms"): 1/1000,
    ("kilograms", "grams"): 1000,

    # imperial <-> metric distances
    ("inches", "centimetres"): 2.54,
    ("centimetres", "inches"): 1/2.54,
    ("inches", "metres"): 1/39.37,
    ("metres", "inches"): 39.37,
    ("feet", "metres"): 1/3.281,
    ("metres", "feet"): 3.281,
    ("feet", "kilometres"): 1/3281,
    ("kilometres", "feet"): 3281,
    ("miles", "kilometres"): 1.609,
    ("kilometres", "miles"): 1/1.609,

    # imperial <-> metric weights
    ("pounds", "grams"): 453.6,
    ("grams", "pounds"): 1/453.6,
    ("ounces", "grams"): 28.35,
    ("grams", "ounces"): 1/28.35,
    ("pounds", "kilograms"): 1/2.205,
    ("kilograms", "pounds"): 2.205,
    ("ounces", "kilograms"): 1/35.274,
    ("kilograms", "ounces"): 35.274,

    # temperature
    ("celcius", "fahrenheit"): lambda x: (x * 9/5)+32,
    ("fahrenheit", "celcius"): lambda x: (x - 32) * 5/9,
}

def convert(input, input_unit, conversion_unit):
    key = (input_unit, conversion_unit)
    if key in conversion_factors:
        factor = conversion_factors[key]
        if callable(factor):
            return factor(input)
        else:
            return input * factor
    else:
        return input

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.output_value = 15
        layout = QHBoxLayout()

        self.input_lineedit = QLineEdit()
        self.input_lineedit.textChanged.connect(self.text_changed_lineedit)
        layout.addWidget(self.input_lineedit)

        self.comboBox1 = QComboBox()
        self.comboBox1.addItems(["Inches", "Feet", "Miles", "Pounds", "Ounces", "Centimetres", "Metres", "Kilometres", "Grams", "Kilograms", "Celcius", "Fahrenheit"])
        self.comboBox1.currentTextChanged.connect(self.text_changed_output)
        self.comboBox1.currentTextChanged.connect(self.text_changed_lineedit)
        layout.addWidget(self.comboBox1)

        equal_sign = QLabel()
        equal_sign.setText(" = ")
        layout.addWidget(equal_sign)

        self.output_text = QLabel()
        self.output_text.setText(str(self.output_value))
        layout.addWidget(self.output_text)

        self.comboBox2 = QComboBox()
        self.comboBox2.addItems(["Inches", "Feet", "Miles", "Pounds", "Ounces", "Centimetres", "Metres", "Kilometres", "Grams", "Kilograms", "Celcius", "Fahrenheit"])
        self.comboBox2.currentTextChanged.connect(self.text_changed_input)
        self.comboBox2.currentTextChanged.connect(self.text_changed_lineedit)
        layout.addWidget(self.comboBox2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def text_changed_lineedit(self):
        input_value = self.input_lineedit.text()
        input_unit = self.comboBox1.currentText()
        input_unit = input_unit.lower()
        output_unit = self.comboBox2.currentText()
        output_unit = output_unit.lower()

        output_value = convert(input_value, input_unit, output_unit)

        self.output_text.setText(str(output_value))

    def text_changed_output(self):
        self.comboBox2.blockSignals(True)
        input_text_output = self.comboBox1.currentText()
        self.comboBox2.clear()
        if input_text_output == "Inches":
            self.comboBox2.addItems(["Feet", "Miles", "Centimetres", "Metres"])
        elif input_text_output == "Feet":
            self.comboBox2.addItems(["Inches", "Miles", "Metres", "Kilometres"])
        elif input_text_output == "Miles":
            self.comboBox2.addItems(["Feet", "Kilometres"])
        elif input_text_output == "Pounds":
            self.comboBox2.addItems(["Ounces", "Grams", "Kilograms"])
        elif input_text_output == "Ounces":
            self.comboBox2.addItems(["Pounds", "Grams", "Kilograms"])
        elif input_text_output == "Centimetres":
            self.comboBox2.addItems(["Inches", "Metres"])
        elif input_text_output == "Metres":
            self.comboBox2.addItems(["Inches", "Feet", "Kilometres"])
        elif input_text_output == "Kilometres":
            self.comboBox2.addItems(["Feet", "Miles", "Metres"])
        elif input_text_output == "Grams":
            self.comboBox2.addItems(["Pounds", "Ounces", "Kilograms"])
        elif input_text_output == "Kilograms":
            self.comboBox2.addItems(["Pounds", "Ounces", "Grams"])
        elif input_text_output == "Celcius":
            self.comboBox2.addItems(["Fahrenheit"])
        elif input_text_output == "Fahrenheit":
            self.comboBox2.addItems(["Celcius"])
        self.comboBox2.blockSignals(False)

    def text_changed_input(self):
        self.comboBox1.blockSignals(True)
        output_text_input = self.comboBox2.currentText()
        self.comboBox1.clear()
        if output_text_input == "Inches":
            self.comboBox1.addItems(["Feet", "Miles", "Centimetres", "Metres"])
        elif output_text_input == "Feet":
            self.comboBox1.addItems(["Inches", "Miles", "Metres", "Kilometres"])
        elif output_text_input == "Miles":
            self.comboBox1.addItems(["Feet", "Kilometres"])
        elif output_text_input == "Pounds":
            self.comboBox1.addItems(["Ounces", "Grams", "Kilograms"])
        elif output_text_input == "Ounces":
            self.comboBox1.addItems(["Pounds", "Grams", "Kilograms"])
        elif output_text_input == "Centimetres":
            self.comboBox1.addItems(["Inches", "Metres"])
        elif output_text_input == "Metres":
            self.comboBox1.addItems(["Inches", "Feet", "Kilometres"])
        elif output_text_input == "Kilometres":
            self.comboBox1.addItems(["Feet", "Miles", "Metres"])
        elif output_text_input == "Grams":
            self.comboBox1.addItems(["Pounds", "Ounces", "Kilograms"])
        elif output_text_input == "Kilograms":
            self.comboBox1.addItems(["Pounds", "Ounces", "Grams"])
        elif output_text_input == "Celcius":
            self.comboBox1.addItems(["Fahrenheit"])
        elif output_text_input == "Fahrenheit":
            self.comboBox1.addItems(["Celcius"])
        self.comboBox1.blockSignals(False)

    def input_text_changed(self, text):
        self.current_input_unit = text.lower()

app = QApplication(sys.argv)
window = Window()

window.show()

app.exec()