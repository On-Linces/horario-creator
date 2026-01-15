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
            for i, dia_idx in enumerate(range(5, 10)):
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

# --- LÓGICA DE EVALUACIÓN ---
def evaluar_eficiencia(combinacion):
    total_gaps = 0
    total_span = 0
    
    for dia in range(5):
        horas_dia = []
        for materia in combinacion:
            for b in materia['horario']:
                if b['dia'] == dia:
                    horas_dia.append((b['ini'], b['fin']))
        
        if horas_dia:
            horas_dia.sort()
            entrada = horas_dia[0][0]
            salida = horas_dia[-1][1]
            span = salida - entrada
            
            duracion_clases = sum(fin - ini for ini, fin in horas_dia)
            gaps = span - duracion_clases
            
            total_gaps += gaps
            total_span += span
            
    return total_gaps, total_span

def imprimir_mejores_opciones(todas_las_combinaciones):
    # Evaluar y ordenar: Prioridad 1: Menos Gaps. Prioridad 2: Menor Span.
    evaluaciones = []
    for c in todas_las_combinaciones:
        gaps, span = evaluar_eficiencia(c)
        evaluaciones.append((gaps, span, c))
    
    evaluaciones.sort(key=lambda x: (x[0], x[1]))
    mejores_3 = evaluaciones[:3]
    
    dias_nombres = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]
    
    for rank, (gaps, span, comb) in enumerate(mejores_3, 1):
        print(f"\nRANKING {rank} [Horas muertas: {gaps}h | Permanencia: {span}h]")
        print("="*60)
        
        resumen_dia = {i: {'entrada': 24, 'salida': 0} for i in range(5)}
        
        for m in comb:
            nombre = m['materia'].upper()
            docente = m['docente'].upper()
            horarios_lista = []
            
            for b in m['horario']:
                if b['ini'] < resumen_dia[b['dia']]['entrada']:
                    resumen_dia[b['dia']]['entrada'] = b['ini']
                if b['fin'] > resumen_dia[b['dia']]['salida']:
                    resumen_dia[b['dia']]['salida'] = b['fin']
                
                dia_nom = dias_nombres[b['dia']]
                horarios_lista.append(f"{dia_nom} {b['ini']}-{b['fin']}")
            
            print(f"● {nombre} ({m['grupo']}) | {' '.join(horarios_lista)} | {docente}")

        print(f"\nHORARIOS DE ENTRADA Y SALIDA:")
        for i, dia in enumerate(dias_nombres):
            ent = resumen_dia[i]['entrada']
            sal = resumen_dia[i]['salida']
            if sal != 0:
                print(f"  {dia}: Entrada {ent:02d}:00 | Salida {sal:02d}:00")
        print("="*60)

# --- EJECUCIÓN ---
datos = parsear_sii_html("horarios_sii.html")
listas = [datos[m] for m in MATERIAS_OBJETIVO if datos[m]]
combinaciones = [c for c in itertools.product(*listas) if not hay_choque(c)]

if combinaciones:
    imprimir_mejores_opciones(combinaciones)
else:
    print("No se encontraron combinaciones válidas.")