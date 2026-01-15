# algoritm.py
import itertools
from bs4 import BeautifulSoup

MATERIAS_OBJETIVO = [
    "Cálculo Vectorial", "Fundamentos de Base de Datos", "Cultura Empresarial",
    "Principios Eléctricos y Aplicaciones Digitales", "Física General", "Taller de Administración"
]

def clean_time(time_str):
    try: return int(time_str.split(':')[0])
    except: return 0

def parsear_datos(contenido_html):
    soup = BeautifulSoup(contenido_html, 'html.parser')
    oferta = {m: [] for m in MATERIAS_OBJETIVO}
    tabla = soup.find('table', id='data-table')
    if not tabla: return {}
    
    for fila in tabla.find('tbody').find_all('tr'):
        cols = fila.find_all('td')
        if len(cols) < 5: continue
        nombre = cols[2].get_text(strip=True)
        if nombre in MATERIAS_OBJETIVO:
            grupo, docente = cols[3].text.strip(), cols[4].text.strip()
            bloques = []
            for i, dia_idx in enumerate(range(5, 10)):
                p_tags = cols[dia_idx].find_all('p')
                for p in p_tags:
                    text = p.text.strip()
                    t = text.split()
                    if len(t) >= 2:
                        campus = "C1" if "Campus 1" in text else "C2"
                        bloques.append({'dia': i, 'ini': clean_time(t[-2]), 'fin': clean_time(t[-1]), 'campus': campus})
            oferta[nombre].append({'materia': nombre, 'grupo': grupo, 'docente': docente, 'horario': bloques})
    return oferta

def hay_choque(comb, f_traslado):
    for i, m1 in enumerate(comb):
        for m2 in comb[i+1:]:
            for b1 in m1['horario']:
                for b2 in m2['horario']:
                    if b1['dia'] == b2['dia']:
                        if b1['ini'] < b2['fin'] and b2['ini'] < b1['fin']: return True
                        if f_traslado and b1['campus'] != b2['campus']:
                            if b1['fin'] == b2['ini'] or b2['fin'] == b1['ini']: return True
    return False

def obtener_mejores_opciones(contenido_html, f_traslado, f_7am, f_libre):
    datos = parsear_datos(contenido_html)
    listas = [datos[m] for m in MATERIAS_OBJETIVO if datos[m]]
    combinaciones = [c for c in itertools.product(*listas) if not hay_choque(c, f_traslado)]
    
    if f_7am:
        temp = [c for c in combinaciones if not any(b['ini'] == 7 for m in c for b in m['horario'])]
        if temp: combinaciones = temp
    
    if f_libre:
        temp = [c for c in combinaciones if len(set(b['dia'] for m in c for b in m['horario'])) < 5]
        if temp: combinaciones = temp

    # Calcular eficiencia y ordenar
    finales = []
    for c in combinaciones:
        gaps = 0
        resumen = {i: {'e': 24, 's': 0} for i in range(5)}
        for m in c:
            for b in m['horario']:
                if b['ini'] < resumen[b['dia']]['e']: resumen[b['dia']]['e'] = b['ini']
                if b['fin'] > resumen[b['dia']]['s']: resumen[b['dia']]['s'] = b['fin']
        
        for d in range(5):
            if resumen[d]['s'] != 0:
                span = resumen[d]['s'] - resumen[d]['e']
                clases = sum(b['fin'] - b['ini'] for m in c for b in m['horario'] if b['dia'] == d)
                gaps += (span - clases)
        finales.append({'gaps': gaps, 'materias': c, 'resumen': resumen})
    
    return sorted(finales, key=lambda x: x['gaps'])[:3]