import itertools
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN ---
MATERIAS_OBJETIVO = [
    "Cálculo Vectorial",
    "Fundamentos de Base de Datos",
    "Cultura Empresarial",
    "Principios Eléctricos y Aplicaciones Digitales",
    "Física General",
    "Taller de Administración"
]

def clean_time(time_str):
    try: return int(time_str.split(':')[0])
    except: return 0

def parsear_sii_html(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
    oferta = {m: [] for m in MATERIAS_OBJETIVO}
    tabla = soup.find('table', id='data-table')
    
    if not tabla: return {}

    filas = tabla.find('tbody').find_all('tr')
    for fila in filas:
        cols = fila.find_all('td')
        if len(cols) < 5: continue
        nombre = cols[2].get_text(strip=True)
        if nombre in MATERIAS_OBJETIVO:
            grupo = cols[3].text.strip()
            docente = cols[4].text.strip()
            bloques = []
            for i, dia_idx in enumerate(range(5, 10)): # 5=Lunes, 9=Viernes
                p_tags = cols[dia_idx].find_all('p')
                for p in p_tags:
                    t = p.text.split()
                    if len(t) >= 2:
                        bloques.append({'dia': i, 'ini': clean_time(t[-2]), 'fin': clean_time(t[-1])})
            oferta[nombre].append({'materia': nombre, 'grupo': grupo, 'docente': docente, 'horario': bloques})
    return oferta

def hay_choque(comb):
    for i, m1 in enumerate(comb):
        for m2 in comb[i+1:]:
            for b1 in m1['horario']:
                for b2 in m2['horario']:
                    if b1['dia'] == b2['dia'] and (b1['ini'] < b2['fin'] and b2['ini'] < b1['fin']):
                        return True
    return False

# --- FUNCIÓN DE IMPRESIÓN CON RESUMEN ---
def imprimir_opciones(opciones):
    dias_nombres = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]
    
    for idx, comb in enumerate(opciones, 1):
        print(f"\n{'='*20} OPCIÓN {idx} {'='*20}")
        
        # Diccionario para rastrear entrada/salida por día
        resumen_dia = {i: {'entrada': 24, 'salida': 0} for i in range(5)}
        
        for m in comb:
            nombre = m['materia'].upper()
            docente = m['docente'].upper()
            horarios_lista = []
            
            for b in m['horario']:
                # Actualizar resumen de entrada/salida
                if b['ini'] < resumen_dia[b['dia']]['entrada']:
                    resumen_dia[b['dia']]['entrada'] = b['ini']
                if b['fin'] > resumen_dia[b['dia']]['salida']:
                    resumen_dia[b['dia']]['salida'] = b['fin']
                
                # Formato de línea de materia
                dia_nom = dias_nombres[b['dia']]
                horarios_lista.append(f"{dia_nom} {b['ini']}-{b['fin']}")
            
            print(f"● {nombre} ({m['grupo']}) | {' '.join(horarios_lista)} | {docente}")

        # Imprimir el resumen solicitado
        print(f"\n--- RESUMEN DE TIEMPOS (OPCIÓN {idx}) ---")
        for i, dia in enumerate(dias_nombres):
            ent = resumen_dia[i]['entrada']
            sal = resumen_dia[i]['salida']
            if sal == 0: # No hay clases ese día
                print(f"  {dia}: LIBRE")
            else:
                print(f"  {dia}: Entrada {ent:02d}:00 | Salida {sal:02d}:00")
        print("="*50)

# --- EJECUCIÓN ---
print("🔍 Procesando 30 combinaciones para el TecNM Celaya...")
datos = parsear_sii_html("horarios_sii.html")
listas = [datos[m] for m in MATERIAS_OBJETIVO if datos[m]]
combinaciones = [c for c in itertools.product(*listas) if not hay_choque(c)]

imprimir_opciones(combinaciones)