"""
Fazer uma calculadora simples construída em Python e Pyside
"""

# para utilizar a função exit() que irá limpar o terminal
import sys

from PyQt6.QtCore import Qt
# importar as classes necessárias do PyQt6
from PyQt6.QtWidgets import (
    QApplication, 
    QGridLayout,
    QLineEdit,
    QMainWindow, 
    QPushButton,
    QVBoxLayout,
    QWidget)
from functools import partial

#constantes
ERROR_MSG = "ERROR"
WINDOW_SIZE = 300 # fixa o tamanho da janela
DISPLAY_HEIGHT = 35 # fica a altura do display
BUTTON_SIZE = 40 # fica o tamanho do button


# classe que providencia o GUI da app. Janela principal da PyCalc
class PyCalcWindow(QMainWindow):
    
    #Construtor da class
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyCalc') # titulo da janela
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        # estamos a criar um objecto QWidget e a colocá-lo como widget central na janela
        centralWidget = QWidget(self) 
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()
        
    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT) # estamos a fixar a altura
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight) # texto no display alinhado à direita
        self.display.setReadOnly(True) # read-only
        self.generalLayout.addWidget(self.display) # adiciona o display ao layout geral da calculadora.
        
    # para criar os buttons vamos utilizar um grid layout e vamos representar as coordenadas dos buttons nessa grid. Cada par de coordenadas corresponde a uma linha e uma coluna. Vamos usar uma lista de listas.Cada nested list vai representar uma linha.
    def _createButtons(self):
        self.buttonMap = {} # criamos um dict vazio
        buttonsLayout = QGridLayout()
        # lista de listas - cada linha (ou nested list) representa uma linha do grid layout e cada index de cada key label será representada pela coluna correspondente no layout
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]
        
        # dois loops. O primeiro itera as linhas e o segundo itera as colunas. Dentro do segundo loop criamos os buttons e adicionamo-los ao buttonMap e ao buttonsLayout. 
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        
        # No fim vamos incluir o buttonsLayout ao layout geral       
        self.generalLayout.addLayout(buttonsLayout)
     
    def setDisplayText(self, text):
        #Vai mostrar o texto no display relativo ao resultado.
        self.display.setText(text)
        self.display.setFocus() #colocar o focus do cursor no display
        
    def displayText(self):
        #Vai mostrar o texto que está a ser introduzido, quando clicamos no button = a app irá usar o valor do return do displayText() como a expressão matemática a ser calculada
        return self.display.text()
    
    def clearDisplay(self):
        #Limpar o display e vai ser triggered todas as vezes que pressionar o button C
        self.setDisplayText("")  
        
        
def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result  
    
class PyCalc:
    def __init__ (self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()
    
    def _calculateResult(self):
        result = self._evaluate(expression = self._view.displayText())
        self._view.setDisplayText(result)
    
    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)
    
    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(partial(self._buildExpression, keySymbol))
        
        self._view.buttonMap["="].clicked.connect(self._calculateResult)   
        self._view.display.returnPressed.connect(self._calculateResult)   
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)
          
          
        
def main():
    #Função main da PyCalc
    pycalcApp = QApplication([]) # Objecto QApplication chamada pycalcApp
    pycalcWindow = PyCalcWindow() # criar a instancia
    pycalcWindow.show() # mostra o GUI
    PyCalc(model=evaluateExpression, view=pycalcWindow)
    sys.exit(pycalcApp.exec()) # corre o event loop da app

if __name__ == "__main__":
    main()
