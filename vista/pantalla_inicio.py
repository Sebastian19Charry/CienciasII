from vista.ventana_grafos import VentanaGrafos
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt
from vista.ventana_busquedas import VentanaBusquedas
# from vista.ventana_grafos import VentanaGrafos  # Descomenta cuando la tengas


class PantallaInicio(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        contenedor = QFrame()
        contenedor.setStyleSheet("background-color:#f0f7f4;")  # Soft Mint background
        cont_layout = QVBoxLayout(contenedor)

        titulo = QLabel("Ciencias de la Computación II")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 42px;
            font-weight: bold;
            color: #1b4332;
            padding: 20px;
        """)

        subtitulo = QLabel("Seleccione una opción")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("""
            font-size: 22px;
            color: #2d6a4f;
            margin-bottom: 20px;
        """)

        # -------- BOTÓN BÚSQUEDAS --------
        btn_busquedas = QPushButton("  🔍  BÚSQUEDAS")
        btn_busquedas.setFixedSize(320, 90)
        btn_busquedas.setCursor(Qt.PointingHandCursor)
        btn_busquedas.setStyleSheet("""
            QPushButton {
                background-color: #40916c;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 20px;
                border: 2px solid #2d6a4f;
            }
            QPushButton:hover {
                background-color: #52b788;
                border: 2px solid #40916c;
            }
            QPushButton:pressed {
                background-color: #2d6a4f;
            }
        """)
        btn_busquedas.clicked.connect(self.abrir_busquedas)

        # -------- BOTÓN GRAFOS --------
        btn_grafos = QPushButton("  📈  GRAFOS")
        btn_grafos.setFixedSize(320, 90)
        btn_grafos.setCursor(Qt.PointingHandCursor)
        btn_grafos.setStyleSheet("""
            QPushButton {
                background-color: #1e6091;  /* Modular Ocean Blue */
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 20px;
                border: 2px solid #184e77;
            }
            QPushButton:hover {
                background-color: #1a759f;
                border: 2px solid #1e6091;
            }
            QPushButton:pressed {
                background-color: #184e77;
            }
        """)
        btn_grafos.clicked.connect(self.abrir_grafos)

        cont_layout.addStretch()
        cont_layout.addWidget(titulo)
        cont_layout.addWidget(subtitulo)
        cont_layout.addSpacing(20)
        cont_layout.addWidget(btn_busquedas, alignment=Qt.AlignCenter)
        cont_layout.addSpacing(25)
        cont_layout.addWidget(btn_grafos, alignment=Qt.AlignCenter)
        cont_layout.addStretch()

        layout.addWidget(contenedor)

    def abrir_busquedas(self):
        self.busquedas = VentanaBusquedas(self.main_window)
        self.main_window.cambiar_pantalla(self.busquedas)

    def abrir_grafos(self):
        # 2. Descomenta y usa la nueva clase
        self.grafos = VentanaGrafos(self.main_window)
        self.main_window.cambiar_pantalla(self.grafos)

