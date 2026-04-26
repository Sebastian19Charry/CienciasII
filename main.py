import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from vista.pantalla_inicio import PantallaInicio

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ciencias de la Computación II")
        
        # Central Stacked Widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize Screens
        self.pantalla_inicio = PantallaInicio(self)

        # Add to stack
        self.stack.addWidget(self.pantalla_inicio) # Index 0

        self.showMaximized()

    def cambiar_pantalla(self, widget):
        # Check if widget is already in stack
        idx = self.stack.indexOf(widget)
        if idx == -1:
            idx = self.stack.addWidget(widget)
        
        self.stack.setCurrentIndex(idx)

    def volver_inicio(self):
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. Force a consistent style that obeys CSS better on Windows
    app.setStyle("Fusion")
    
    # 2. Apply a TRULY GLOBAL stylesheet to the entire application
    app.setStyleSheet("""
        QMainWindow, QWidget#centralwidget, QStackedWidget {
            background-color: #f0f7f4;
        }
        
        QLabel {
            color: #1b4332;
            font-size: 14px;
        }

        QLineEdit, QSpinBox, QTextEdit, QTableWidget {
            background-color: white;
            color: #081c15;
            border: 1px solid #d8e3dc;
            border-radius: 4px;
            padding: 5px;
        }

        /* --- SPINBOX ARROWS FIX --- */
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #f0f7f4;
            border: 1px solid #d8e3dc;
            width: 18px;
        }
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #e0ece6;
        }

        /* Using standard unicode-like symbols or letting default handle it */
        QSpinBox::up-arrow {
            width: 7px;
            height: 7px;
        }

        QSpinBox::down-arrow {
            width: 7px;
            height: 7px;
        }

        /* --- GLOBAL BUTTON STYLE FOR ALL PUSHBUTTONS --- */
        QPushButton {
            background-color: #2d6a4f;
            color: white;
            border: 1px solid #1b4332;
            border-radius: 6px;
            padding: 8px 15px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #40916c;
        }

        /* --- SPECIFIC RULES FOR DIALOGS (QInputDialog, QMessageBox) --- */
        QDialog {
            background-color: #f0f7f4;
        }

        /* Force dark text on ALL widgets inside a dialog */
        QDialog QLabel, QDialog QComboBox, QDialog QPushButton, 
        QDialog QListView, QDialog QLineEdit, QDialog QSpinBox {
            color: #081c15 !important;
        }

        QDialog QLabel {
            font-weight: bold;
            padding: 10px;
        }

        QDialog QPushButton {
            background-color: #f8fcf9;
            border: 1px solid #2d6a4f;
            min-width: 80px;
            height: 30px;
            font-weight: bold;
        }

        QDialog QPushButton:hover {
            background-color: #e0ece6;
        }
        
        QDialog QComboBox {
            background-color: white;
            border: 1px solid #2d6a4f;
            padding: 5px;
            min-width: 150px;
        }

        QHeaderView::section {
            background-color: #2d6a4f;
            color: white;
            font-weight: bold;
        }
    """)
    
    window = MainWindow()
    sys.exit(app.exec())
