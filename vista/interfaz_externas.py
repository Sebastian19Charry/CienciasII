from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
# Importamos la clase desde el archivo físico que veo en tu imagen
from vista.VistaSecuencialExterna import VistaSecuencialExterna
from vista.VistaBinariaExterna import VistaBinariaExterna
from vista.VistaHashExterna import VistaHashExterna

class InterfazExternas(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.vistas_cargadas = {}
        self.main_window = main_window
        self.anterior = anterior

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setFixedWidth(330)
        sidebar.setStyleSheet("background-color:#1b4332;")
        s = QVBoxLayout(sidebar)
        s.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("BÚSQUEDAS EXTERNAS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color:white; font-size:22px; font-weight:bold; padding:40px 20px;")
        s.addWidget(titulo)

        # Opciones principales (Agrupamos las Hash en un solo botón)
        opciones = [
            ("  🔑  Funciones Hash", "HASH_MENU"),
            ("  🗄️  Estructuras dinámicas", "CUBETAS_MENU"),
            ("  ⚖️  Binaria externa", "Binaria externa"),
            ("  🔢  Secuencial externa", "Secuencial externa")
        ]

        # Dentro de InterfazExternas, en el bucle donde creas los botones:
        for texto_mostrar, op in opciones:
            btn = self.boton(texto_mostrar)
            if op == "HASH_MENU":
                btn.clicked.connect(lambda: self.main_window.cambiar_pantalla(InterfazHash(self.main_window, self)))
            elif op == "CUBETAS_MENU":
                # ESTA ES LA CONEXIÓN CLAVE:
                btn.clicked.connect(lambda: self.main_window.cambiar_pantalla(InterfazCubetas(self.main_window, self)))
            else:
                btn.clicked.connect(lambda checked=False, o=op: self.mostrar_algoritmo(o))
            s.addWidget(btn)

        s.addStretch()
        s.addWidget(self.volver())

        # --- STACK DE CONTENIDO ---
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background:#f0f7f4;")
        
        bienvenida = QWidget()
        b_layout = QVBoxLayout(bienvenida)
        self.lbl_mensaje = QLabel("Seleccione un método de búsqueda externa")
        self.lbl_mensaje.setAlignment(Qt.AlignCenter)
        self.lbl_mensaje.setStyleSheet("font-size:26px; color:#1b4332; font-weight:bold;")
        b_layout.addStretch()
        b_layout.addWidget(self.lbl_mensaje)
        b_layout.addStretch()
        
        self.local_stack.addWidget(bienvenida)

        layout.addWidget(sidebar)
        layout.addWidget(self.local_stack)

    def mostrar_algoritmo(self, nombre):
        # 1. Verificar si es una de nuestras interfaces reales
        if nombre == "Secuencial externa" or nombre == "Binaria externa":
            
            # Si la vista no ha sido creada todavía, la instanciamos
            if nombre not in self.vistas_cargadas:
                if nombre == "Secuencial externa":
                    nueva_vista = VistaSecuencialExterna(self.main_window)
                else:
                    nueva_vista = VistaBinariaExterna(self.main_window)
                
                # La guardamos y la añadimos al stack
                indice = self.local_stack.addWidget(nueva_vista)
                self.vistas_cargadas[nombre] = indice
            
            # 2. Mostramos la vista correspondiente usando su índice guardado
            self.local_stack.setCurrentIndex(self.vistas_cargadas[nombre])
            
        else:
            # 3. Para los algoritmos que aún no programas (Hash, etc.)
            self.local_stack.setCurrentIndex(0) # El widget de bienvenida con el label
            self.lbl_mensaje.setText(f"Interfaz para:\n{nombre}\n(En desarrollo)")

    def boton(self, t):
        b = QPushButton(t)
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedHeight(55)
        b.setStyleSheet("""
            QPushButton{
                background:#2d6a4f;
                color:white;
                padding-left:30px;
                text-align:left;
                border:none;
                font-size:15px;
                font-weight:500;
            }
            QPushButton:hover{
                background:#40916c;
            }
        """)
        return b

    def volver(self):
        b = QPushButton("  ⬅  Volver al Inicio")
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedHeight(60)
        b.setStyleSheet("QPushButton{ background:#1b4332; color:white; padding-left:30px; text-align:left; font-size:15px; border-top: 1px solid #40916c; } QPushButton:hover{ background:#2d6a4f; }")
        b.clicked.connect(lambda: self.main_window.cambiar_pantalla(self.anterior))
        return b


# === NUEVA INTERFAZ PARA EL SUB-MENÚ DE HASH ===

class InterfazHash(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.main_window = main_window
        self.anterior = anterior
        self.vistas_cargadas = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- SIDEBAR (Mismo estilo que InterfazExternas) ---
        sidebar = QFrame()
        sidebar.setFixedWidth(330)
        sidebar.setStyleSheet("background-color:#1b4332;")
        s = QVBoxLayout(sidebar)
        s.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("FUNCIONES HASH")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color:white; font-size:22px; font-weight:bold; padding:40px 20px;")
        s.addWidget(titulo)

        # Opciones extraídas de tu imagen
        opciones = [
            ("  ÷  Función módulo", "módulo"),
            ("  ²  Función cuadrado", "cuadrado"),
            ("  ✂  Función truncamiento", "truncamiento"),
            ("  📖  Función plegamiento", "plegamiento")
        ]

        for texto, clave in opciones:
            btn = self.boton_metodo(texto)
            # Aquí conectarías a la lógica de visualización de cada hash
            btn.clicked.connect(lambda checked=False, c=clave: self.mostrar_metodo_hash(c))
            s.addWidget(btn)

        s.addStretch()
        
        # Botón para regresar a la pantalla de Búsquedas Externas
        btn_volver = QPushButton("  ⬅  Volver a Externas")
        btn_volver.setCursor(Qt.PointingHandCursor)
        btn_volver.setFixedHeight(60)
        btn_volver.setStyleSheet("""
            QPushButton{ 
                background:#1b4332; color:white; padding-left:30px; 
                text-align:left; font-size:15px; border-top: 1px solid #40916c; 
            } 
            QPushButton:hover{ background:#2d6a4f; }
        """)
        btn_volver.clicked.connect(lambda: self.main_window.cambiar_pantalla(self.anterior))
        s.addWidget(btn_volver)

        # --- STACK DE CONTENIDO ---
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background:#f0f7f4;")
        
        bienvenida = QWidget()
        b_layout = QVBoxLayout(bienvenida)
        self.lbl_mensaje = QLabel("Seleccione una función hash del menú lateral")
        self.lbl_mensaje.setAlignment(Qt.AlignCenter)
        self.lbl_mensaje.setStyleSheet("font-size:26px; color:#1b4332; font-weight:bold;")
        b_layout.addStretch()
        b_layout.addWidget(self.lbl_mensaje)
        b_layout.addStretch()
        
        self.local_stack.addWidget(bienvenida)

        layout.addWidget(sidebar)
        layout.addWidget(self.local_stack)

    def boton_metodo(self, t):
        b = QPushButton(t)
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedHeight(55)
        # Estilo idéntico al de tu imagen
        b.setStyleSheet("""
            QPushButton{
                background:#2d6a4f;
                color:white;
                padding-left:30px;
                text-align:left;
                border:none;
                font-size:15px;
                font-weight:500;
                margin: 5px 15px;
                border-radius: 10px;
            }
            QPushButton:hover{
                background:#40916c;
            }
        """)
        return b

    def mostrar_metodo_hash(self, nombre):
        """
        Crea o muestra la instancia de VistaHashExterna según el método seleccionado.
        """
        # Verificamos si la vista para este método ya existe en el diccionario
        if nombre not in self.vistas_cargadas:
            # Si no existe, creamos la instancia de la clase detallada
            # Nota: Usamos el nombre de la clase que pusiste abajo (VistaHashExterna)
            nueva_vista = VistaHashExterna(self.main_window, nombre)
            
            # La añadimos al stack de la derecha
            indice = self.local_stack.addWidget(nueva_vista)
            
            # Guardamos el índice para no volver a crearla después
            self.vistas_cargadas[nombre] = indice
        
        # Cambiamos el índice del Stack para mostrar la vista real, no el mensaje de bienvenida
        self.local_stack.setCurrentIndex(self.vistas_cargadas[nombre])

class InterfazCubetas(QWidget):
    def __init__(self, main_window, anterior):
        super().__init__()
        self.main_window = main_window
        self.anterior = anterior
        self.vistas_cargadas = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setFixedWidth(330)
        sidebar.setStyleSheet("background-color:#1b4332;")
        s = QVBoxLayout(sidebar)

        titulo = QLabel("ESTRUCTURAS\nDINÁMICAS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color:white; font-size:22px; font-weight:bold; padding:40px 20px;")
        s.addWidget(titulo)

        # Opciones de expansión
        opciones = [
            ("  📊  Expansión y reducción total", "total"),
            ("  📉  Expansión y reducción parcial", "parcial")
        ]

        for texto, clave in opciones:
            btn = self.boton_metodo(texto)
            btn.clicked.connect(lambda checked=False, c=clave: self.mostrar_metodo_cubetas(c))
            s.addWidget(btn)

        s.addStretch()
        
        # Botón Volver
        btn_volver = self.boton_metodo("  ⬅  Volver a Externas")
        btn_volver.clicked.connect(lambda: self.main_window.cambiar_pantalla(self.anterior))
        s.addWidget(btn_volver)

        # --- STACK DE CONTENIDO ---
        self.local_stack = QStackedWidget()
        self.local_stack.setStyleSheet("background:#f0f7f4;")
        
        bienvenida = QWidget()
        b_layout = QVBoxLayout(bienvenida)
        self.lbl_mensaje = QLabel("Seleccione un método de expansión")
        self.lbl_mensaje.setAlignment(Qt.AlignCenter)
        self.lbl_mensaje.setStyleSheet("font-size:24px; color:#1b4332; font-weight:bold;")
        b_layout.addStretch(); b_layout.addWidget(self.lbl_mensaje); b_layout.addStretch()
        
        self.local_stack.addWidget(bienvenida)
        layout.addWidget(sidebar); layout.addWidget(self.local_stack)

    def boton_metodo(self, t):
        b = QPushButton(t)
        b.setFixedHeight(55)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet("""
            QPushButton{
                background:#2d6a4f; color:white; text-align:left;
                padding-left:20px; border:none; font-size:14px;
                margin: 5px 15px; border-radius: 10px;
            }
            QPushButton:hover{ background:#40916c; }
        """)
        return b

    def mostrar_metodo_cubetas(self, nombre):
        if nombre == "total":
            from vista.VistaCubetasTotal import VistaCubetasTotal
            vista = VistaCubetasTotal(self.main_window)
            idx = self.local_stack.addWidget(vista)
            self.local_stack.setCurrentIndex(idx)
        elif nombre == "parcial":
            # AHORA SÍ CARGAMOS LA PARCIAL
            from vista.VistaCubetasParcial import VistaCubetasParcial
            vista = VistaCubetasParcial(self.main_window)
            idx = self.local_stack.addWidget(vista)
            self.local_stack.setCurrentIndex(idx)