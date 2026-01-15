# Generador de Horarios - SII TecNM Celaya

## Descripción General

Esta herramienta automatizada permite la extracción, análisis y generación de combinaciones de horarios escolares a partir del Sistema Integral de Información (SII) del TecNM en Celaya. Su propósito principal es facilitar la planificación académica mediante la detección automática de conflictos de horario y la visualización de resúmenes diarios de entrada y salida.

El sistema opera en dos fases secuenciales:
1.  **Extracción de Datos**: Obtención del código fuente de la oferta académica mediante scraping autenticado.
2.  **Procesamiento y Generación**: Análisis sintáctico del HTML para construir combinaciones válidas de materias.

## Tecnologías Utilizadas

El proyecto está construido utilizando Python 3 y las siguientes bibliotecas:

*   **Playwright (async)**: Para la automatización del navegador y la interacción con el portal cautivo del SII.
*   **BeautifulSoup (bs4)**: Para el análisis sintáctico (parsing) del documento HTML.
*   **itertools**: Para la generación eficiente de productos cartesianos de combinaciones de grupos.
*   **AsyncIO**: Para el manejo de operaciones asíncronas de entrada/salida.

## Estructura del Proyecto

*   `scrap.py`: Script encargado de iniciar la sesión en el navegador, navegar al módulo de reinscripciones y capturar el código HTML de la tabla de horarios.
*   `algoritm.py`: Núcleo lógico que procesa el archivo HTML descargado, extrae la información de grupos y docentes, y calcula las combinaciones posibles sin superposición de horarios.
*   `horarios_sii.html`: Archivo intermedio generado por `scrap.py` que contiene los datos crudos del SII.
*   `README.md`: Documentación técnica del proyecto.

## Requisitos Previos

*   Python 3.8 o superior.
*   Navegador Firefox instalado (requerido por Playwright).

### Instalación de Dependencias

Se recomienda utilizar un entorno virtual. Instale las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
playwright install firefox
```

## Guía de Uso

### 1. Configuración de Materias

Antes de ejecutar la generación, debe definir las materias de interés en el archivo `algoritm.py`. Modifique la lista `MATERIAS_OBJETIVO`:

```python
MATERIAS_OBJETIVO = [
    "Cálculo Vectorial",
    "Fundamentos de Base de Datos",
    "Cultura Empresarial",
    # Agregue aquí el nombre exacto de la materia según el SII
]
```

### 2. Extracción de Datos (Fase 1)

Ejecute el script de scraping. Esto abrirá una instancia de Firefox para que realice el inicio de sesión manual.

```bash
python scrap.py
```

*   El navegador se abrirá en modo visible (no headless).
*   Inicie sesión con sus credenciales institucionales.
*   El script detectará automáticamente la tabla de horarios y guardará el archivo `horarios_sii.html`.
*   El navegador se cerrará automáticamente al finalizar.

### 3. Generación de Horarios (Fase 2)

Una vez obtenido el archivo HTML, ejecute el algoritmo de procesamiento:

```bash
python algoritm.py
```

El sistema imprimirá en consola:
*   Todas las combinaciones de grupos posibles.
*   Horarios detallados por día.
*   Nombre del docente por materia.
*   Resumen de horas de entrada y salida diarias.
*   Alerta de días libres si los hubiera.

## Notas Técnicas

*   **Seguridad**: El script no almacena ni gestiona credenciales de acceso. El inicio de sesión es totalmente manual y gestionado por el usuario en la instancia del navegador.
*   **Compatibilidad**: El parser depende de la estructura HTML actual del SII. Cambios en el diseño web de la institución podrían requerir actualizaciones en los selectores de `BeautifulSoup`.
