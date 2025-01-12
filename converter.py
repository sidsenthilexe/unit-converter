import sys

# import ui modules
from PySide6.QtCore import (QSize, Qt,)
from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QComboBox, QHBoxLayout, QLineEdit, QLabel,)

# define factors for unit conversion
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

# define function to convert between units
def convert(input, input_unit, conversion_unit):
    input = float(input)
    key = (input_unit, conversion_unit)
    if key in conversion_factors:
        factor = conversion_factors[key]
        if callable(factor):
            return factor(input)
        else:
            return input * factor
    else:
        return input

# define main window class
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # set window title
        self.setWindowTitle("Unit Converter")
        layout = QHBoxLayout()

        # initialize output value
        self.output_value = 0

        # create input lineedit
        self.input_lineedit = QLineEdit()
        self.input_lineedit.textChanged.connect(self.text_changed_lineedit)
        layout.addWidget(self.input_lineedit)

        # create input combobox
        self.comboBox1 = QComboBox()
        self.comboBox1.addItems(["Inches", "Feet", "Miles", "Pounds", "Ounces", "Centimetres", "Metres", "Kilometres", "Grams", "Kilograms", "Celcius", "Fahrenheit"])
        self.comboBox1.currentTextChanged.connect(self.text_changed_output)
        layout.addWidget(self.comboBox1)

        # equal sign label
        equal_sign = QLabel()
        equal_sign.setText(" = ")
        layout.addWidget(equal_sign)
        
        # create output value label
        self.output_text = QLabel()
        self.output_text.setText(str(self.output_value))
        layout.addWidget(self.output_text)

        # create output combobox
        self.comboBox2 = QComboBox()
        self.comboBox2.addItems(["Inches", "Feet", "Miles", "Pounds", "Ounces", "Centimetres", "Metres", "Kilometres", "Grams", "Kilograms", "Celcius", "Fahrenheit"])
        self.comboBox2.currentTextChanged.connect(self.text_changed_input)
        layout.addWidget(self.comboBox2)

        # set layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # define function to update output value
    def text_changed_lineedit(self):

        # take the input value or skip to an empty string if invalid
        input_value = self.input_lineedit.text()
        if input_value == "":
            self.output_text.setText("")
            return

        # find the current input and output units and prepare for conversion function
        input_unit = self.comboBox1.currentText()
        input_unit = input_unit.lower()
        output_unit = self.comboBox2.currentText()
        output_unit = output_unit.lower()

        # call the conversion function and round the output value
        output_value = convert(input_value, input_unit, output_unit)
        output_value = round(output_value, 2)

        # set the output value in the label
        self.output_text.setText(str(output_value))

    # define function to update output unit combobox based on input unit combobox
    def text_changed_output(self):
        self.comboBox2.blockSignals(True)
        input_text_output = self.comboBox1.currentText()
        current_output = self.comboBox2.currentText()
        self.comboBox2.clear()
        valid_units = []
        if input_text_output == "Inches":
            valid_units = ["Feet", "Miles", "Centimetres", "Metres"]
        elif input_text_output == "Feet":
            valid_units = ["Inches", "Miles", "Metres", "Kilometres"]
        elif input_text_output == "Miles":
            valid_units = ["Feet", "Kilometres"]
        elif input_text_output == "Pounds":
            valid_units = ["Ounces", "Grams", "Kilograms"]
        elif input_text_output == "Ounces":
            valid_units = ["Pounds", "Grams", "Kilograms"]
        elif input_text_output == "Centimetres":
            valid_units = ["Inches", "Metres"]
        elif input_text_output == "Metres":
            valid_units = ["Inches", "Feet", "Kilometres"]
        elif input_text_output == "Kilometres":
            valid_units = ["Feet", "Miles", "Metres"]
        elif input_text_output == "Grams":
            valid_units = ["Pounds", "Ounces", "Kilograms"]
        elif input_text_output == "Kilograms":
            valid_units = ["Pounds", "Ounces", "Grams"]
        elif input_text_output == "Celcius":
            valid_units = ["Fahrenheit"]
        elif input_text_output == "Fahrenheit":
            valid_units = ["Celcius"]
        self.comboBox2.addItems(valid_units)
        if current_output in valid_units:
            self.comboBox2.setCurrentText(current_output)
        self.comboBox2.blockSignals(False)
        self.text_changed_lineedit()

    # define function to update input unit combobox based on output unit combobox
    def text_changed_input(self):
        self.comboBox1.blockSignals(True)
        output_text_input = self.comboBox2.currentText()
        current_input = self.comboBox1.currentText()
        self.comboBox1.clear()
        valid_units = []
        if output_text_input == "Inches":
            valid_units = ["Feet", "Miles", "Centimetres", "Metres"]
        elif output_text_input == "Feet":
            valid_units = ["Inches", "Miles", "Metres", "Kilometres"]
        elif output_text_input == "Miles":
            valid_units = ["Feet", "Kilometres"]
        elif output_text_input == "Pounds":
            valid_units = ["Ounces", "Grams", "Kilograms"]
        elif output_text_input == "Ounces":
            valid_units = ["Pounds", "Grams", "Kilograms"]
        elif output_text_input == "Centimetres":
            valid_units = ["Inches", "Metres"]
        elif output_text_input == "Metres":
            valid_units = ["Inches", "Feet", "Kilometres"]
        elif output_text_input == "Kilometres":
            valid_units = ["Feet", "Miles", "Metres"]
        elif output_text_input == "Grams":
            valid_units = ["Pounds", "Ounces", "Kilograms"]
        elif output_text_input == "Kilograms":
            valid_units = ["Pounds", "Ounces", "Grams"]
        elif output_text_input == "Celcius":
            valid_units = ["Fahrenheit"]
        elif output_text_input == "Fahrenheit":
            valid_units = ["Celcius"]
        self.comboBox1.addItems(valid_units)
        if current_input in valid_units:
            self.comboBox1.setCurrentText(current_input)
        self.comboBox1.blockSignals(False)
        self.text_changed_lineedit() 

# create application
app = QApplication(sys.argv)
window = Window()

window.show()

app.exec()