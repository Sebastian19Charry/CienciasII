# Ciencias de la Computación II - Visualización de Estructuras

Este proyecto es una aplicación educativa interactiva desarrollada en **Python** con **PySide6**. Permite visualizar y gestionar diversas estructuras de datos y algoritmos de búsqueda a través de una interfaz moderna y estandarizada.

## 🚀 Características Principalas

- **🔎 Algoritmos de Búsqueda**: Implementaciones de búsqueda lineal (secuencial) y búsqueda binaria con visualización paso a paso.
- **🏗️ Estructuras de Datos**:
  - **Tablas Hash**: Gestión de colisiones y visualización de la estructura.
  - **Árboles Digitales**: Representación bit a bit.
  - **Árboles de Huffman**: Codificación y decodificación con estadísticas de compresión.
  - **Tries de Residuos**: Visualización clara de la estructura de prefijos.
- **💾 Persistencia Inteligente**:
  - Auto-guardado de cambios en archivos JSON.
  - Opciones de guardado y carga manual para gestionar diferentes estados.
- **🎨 Interfaz Premium**: Diseño limpio, botones estandarizados y visualizaciones de árboles de alta legibilidad con zoom y arrastre.

## 🛠️ Requisitos

- **Python 3.11+**
- **PySide6** (Biblioteca para la interfaz gráfica)

## 📦 Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   ```
2. Instala las dependencias necesarias:
   ```bash
   pip install PySide6
   ```
3. Ejecuta la aplicación principal:
   ```bash
   python main.py
   ```

## 📂 Estructura del Proyecto

- `modelo/`: Contiene la lógica y los datos de las estructuras (MVC).
- `vista/`: Define las interfaces de usuario y componentes gráficos.
- `controlador/`: Gestiona la interacción entre el usuario, el modelo y la vista.
- `data/`: Directorio donde se almacenan las persistencias en JSON.
- `main.py`: Punto de entrada de la aplicación.
