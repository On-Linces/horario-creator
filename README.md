# Generador de Horarios - SII TecNM Celaya

## Descripción General

Esta herramienta ofrece una solución integral para la gestión y planificación de horarios académicos del Sistema Integral de Información (SII) del TecNM en Celaya. El sistema combina la automatización de la extracción de datos con un potente algoritmo de generación de combinaciones, accesible tanto a través de scripts de consola como de una interfaz web intuitiva.

Su objetivo es optimizar el proceso de inscripción permitiendo a los estudiantes visualizar todas las combinaciones posibles de materias, minimizando conflictos y permitiendo filtrar por preferencias como días libres o campus específicos.

## Funcionalidades Principales

1.  **Extracción Automatizada**: Scraping seguro y autenticado de la oferta académica actual.
2.  **Interfaz Web**: Aplicación amigable para cargar datos y visualizar horarios generados.
3.  **Filtrado Inteligente**:
    *   Detección de choques de horario.
    *   Optimización de tiempos de traslado entre campus.
    *   Priorización de horarios matutinos (evitar clases a las 7:00 AM).
    *   Búsqueda de días libres.

## Tecnologías Utilizadas

El proyecto utiliza un stack tecnológico robusto basado en Python 3:

*   **Flask**: Microframework para el despliegue de la interfaz web.
*   **Playwright**: Automatización moderna de navegadores para la extracción de datos.
*   **BeautifulSoup (bs4)**: Análisis eficiente de documentos HTML.
*   **AsyncIO**: Gestión de concurrencia para operaciones de red.

## Estructura del Proyecto

*   `app.py`: Servidor web Flask que gestiona la interfaz de usuario y el procesamiento de archivos.
*   `scrap.py`: Módulo de extracción de datos que interactúa con el portal del SII.
*   `utils/algoritm.py`: Núcleo lógico para el cálculo de combinaciones y filtrado.
*   `templates/`: Directorio que contiene las plantillas HTML de la interfaz web.

## Requisitos e Instalación

### Prerrequisitos
*   Python 3.8 o superior.
*   Navegador Firefox (gestionado automáticamente por Playwright).

### Instalación

Se recomienda instalar las dependencias en un entorno virtual aislado:

```bash
# Instalación de paquetes Python
pip install -r requirements.txt

# Instalación de binarios del navegador
playwright install firefox
```

## Guía de Uso

El sistema opera en dos etapas: Extracción y Generación.

### Fase 1: Extracción de Datos

Utilice el script `scrap.py` para obtener la oferta académica más reciente.

```bash
python scrap.py
```
> **Nota**: Se abrirá una ventana de navegador donde deberá iniciar sesión manualmente en el portal del SII. Una vez cargada la tabla de horarios, el script guardará automáticamente la información en `horarios_sii.html`.

### Fase 2: Generación de Horarios

#### Opción A: Interfaz Web (Recomendada)
Para una experiencia visual e interactiva:

1.  Inicie la aplicación web:
    ```bash
    python app.py
    ```
2.  Abra su navegador en `http://127.0.0.1:5000`.
3.  Suba el archivo `horarios_sii.html` generado en la fase anterior.
4.  Seleccione sus preferencias (evitar traslados, días libres, etc.) y genere las opciones.

#### Opción B: Consola
Para procesamiento directo o integración:

1.  Configure las materias deseadas en `utils/algoritm.py`.
2.  Ejecute el algoritmo:
    ```bash
    python utils/algoritm.py
    ```

## Configuración Avanzada

Para modificar las materias objetivo sin usar la interfaz web, edite la lista `MATERIAS_OBJETIVO` en el archivo `utils/algoritm.py`:

```python
MATERIAS_OBJETIVO = [
    "Cálculo Vectorial",
    "Fundamentos de Base de Datos",
    # ... agregue sus materias aquí
]
```

## Aviso Legal

Esta es una herramienta de apoyo académico desarrollada por terceros y no tiene afiliación oficial con el Tecnológico Nacional de México ni con el SII. El uso de credenciales es local y no se transmite a servidores externos.
