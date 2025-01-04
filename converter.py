import sys

from PySide6.QtCore import (QSize, Qt,)
from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QComboBox, QHBoxLayout, QLineEdit, QLabel,)


global current_input_unit


conversion_factors = {

    #imperial distances
    ("inches", "feet"): 1/12,
    ("feet", "inches"): 12,
    ("feet", "miles"): 1/5280,
    ("miles", "feet"): 5280,

    #imperial weights
    ("pound, ounce"): 16,
    ("ounce, pound"): 1/16,

    #metric distances
    ("centimetres", "metres"): 1/100,
    ("metres", "centimetres"): 100,
    ("metres", "kilometres"): 1/1000,
    ("kilometres","metres"): 1000,

    #metric weights
    ("grams", "kilograms"): 1/1000,
    ("kilograms", "grams"): 1000,

    #imperial <-> metric distances
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

    #imperial <-> metric weights
    ("pound, gram"): 453.6,
    ("gram", "pound"): 1/453.6,
    ("ounce", "gram"): 28.35,
    ("gram, ounce"): 1/28.35,
    ("pound", "kilogram"): 1/2.205,
    ("kilogram", "pound"): 2.205,
    ("ounce", "kilogram"): 1/35.274,
    ("kilogram", "ounce"): 35.274,

    #temperature
    ("celcius", "fahrenheit"): lambda x: (x * 9/5)+32,
    ("fahrenheit", "celcius"): lambda x: (x - 32) * 5/9,
}

def convert(input, input_unit, conversion_unit):
    key = (input_unit, conversion_unit)
    if key in conversion_factors:
        factor = conversion_factors[key]
        if callable(factor):
            return factor(input)
        return input*factor
    else:
        return input


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")
        
        layout = QHBoxLayout()

        input_combobox = QComboBox()
        input_combobox.addItems(["Inches", "Feet", "Miles", "Pounds", "Ounces", "Centimetres", "Metres", "Kilometres", "Grams", "Kilograms", "Celcius", "Fahrenheit"])
        input_combobox.currentTextChanged.connect(self.input_text_changed)
        input_combobox.setLayout(layout)
        self.setCentralWidget(input_combobox)


       
    
    def input_text_changed(self, text):
        global current_input_unit
        current_input_unit = text.lower()


app = QApplication(sys.argv)
window = Window()
window.show()

app.exec()