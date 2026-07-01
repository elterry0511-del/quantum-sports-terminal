import math
import json

# =====================================================================
# 📊 PANEL DE ENTRADA DE DATOS (ESTADOS UNIDOS vs BOSNIA)
# =====================================================================
# Introduce aquí las cuotas de tu casa de apuestas y tus proyecciones.

# 1. LÍNEA DE DINERO (MONEYLINE)
CUOTA_USA = "-165"          # Cuota americana para la victoria de USA (Over de la línea 0)
CUOTA_BOSNIA = "+425"       # Cuota americana para la victoria de Bosnia (Under de la línea 0)
PROB_PROYECTADA_USA = 0.62  # Tu probabilidad estimada de que gane USA (0.00 a 1.00)

# 2. TOTAL DE GOLES (OVER / UNDER)
LINEA_GOLES = 2.5
CUOTA_GOLES_OVER = "+110"
CUOTA_GOLES_UNDER = "-135"
PROYECCION_MEDIA_GOLES = 2.85 # Media de goles esperada (Lambda para Poisson)

# 3. AMBOS MARCAN (BTTS - BOTH TEAMS TO SCORE)
CUOTA_BTTS_SI = "-115"      # Cuota para el "Sí" (Mapeado como OVER)
CUOTA_BTTS_NO = "-105"      # Cuota para el "No" (Mapeado como UNDER)
PROB_PROYECTADA_BTTS_SI = 0.54 # Tu probabilidad estimada de que ambos anoten (0.00 a 1.00)

# =====================================================================
# 🧠 CORE MATEMÁTICO: LÓGICA DE APUESTAS Y MODELADO DE PROBABILIDAD
# =====================================================================

def american_to_decimal(american_odds):
    """Convierte cuotas americanas a multiplicadores decimales de pago neto."""
    try:
        odds = float(american_odds)
        if odds > 0:
            return odds / 100.0
        else:
            return 100.0 / abs(odds)
    except ZeroDivisionError:
        return 0.0

def poisson_probability(la, k):
    """Calcula la probabilidad exacta de un evento K usando distribución de Poisson."""
    return (pow(la, k) * math.exp(-la)) / math.factorial(k)

def calculate_poisson_under(la, line):
    """Calcula la probabilidad acumulada por debajo de la línea de goles."""
    prob_under = 0.0
    max_goles_under = math.ceil(line)
    for k in range(max_goles_under):
        prob_under += poisson_probability(la, k)
    return prob_under

def calculate_edge_and_kelly(p_proyectada, net_odds):
    """Calcula el Edge neto y la fracción de Kelly optimizada al 25%."""
    if net_odds <= 0:
        return 0.0, 0.0
    implied_p = 1.0 / (net_odds + 1.0)
    edge = p_proyectada - implied_p
    
    # Criterio de Kelly estándar: (p * b - q) / b -> Reducido al 25% de fracción (Quarter Kelly)
    if edge > 0:
        q = 1.0 - p_proyectada
        kelly_completo = (p_proyectada * net_odds - q) / net_odds
        fractional_kelly = max(0.0, kelly_completo * 0.25)
    else:
        fractional_kelly = 0.0
    return edge, fractional_kelly

def generate_quantum_slate():
    slate = []
    
    # Convertidores de pago neto (b) para las fórmulas
    b_usa = american_to_decimal(CUOTA_USA)
    b_bosnia = american_to_decimal(CUOTA_BOSNIA)
    b_goles_over = american_to_decimal(CUOTA_GOLES_OVER)
    b_goles_under = american_to_decimal(CUOTA_GOLES_UNDER)
    b_btts_si = american_to_decimal(CUOTA_BTTS_SI)
    b_btts_no = american_to_decimal(CUOTA_BTTS_NO)

    # 1. Procesar matemáticas de Moneyline
    edge_usa, kelly_usa = calculate_edge_and_kelly(PROB_PROYECTADA_USA, b_usa)
    prob_bosnia_proyectada = 1.0 - PROB_PROYECTADA_USA - 0.12 # Deducción estimada del empate técnico
    edge_bosnia, _ = calculate_edge_and_kelly(prob_bosnia_proyectada, b_bosnia)

    # 2. Procesar matemáticas de Goles mediante distribución de Poisson
    prob_under_goles = calculate_poisson_under(PROYECCION_MEDIA_GOLES, LINEA_GOLES)
    prob_over_goles = 1.0 - prob_under_goles
    edge_over, kelly_over = calculate_edge_and_kelly(prob_over_goles, b_goles_over)
    edge_under, kelly_under = calculate_edge_and_kelly(prob_under_goles, b_goles_under)

    # 3. Procesar matemáticas de Ambos Marcan
    edge_btts_si, kelly_btts_si = calculate_edge_and_kelly(PROB_PROYECTADA_BTTS_SI, b_btts_si)
    edge_btts_no, kelly_btts_no = calculate_edge_and_kelly(1.0 - PROB_PROYECTADA_BTTS_SI, b_btts_no)

    # Ensamblaje estructural del slate limpio para la Pizarra Activa
    props_partido = [
        {
            "id": "fb_usa_ml",
            "name": "Línea de Dinero - Victoria USA",
            "team": "USA",
            "marketType": "goals",
            "line": 0,
            "oddsOver": CUOTA_USA,
            "oddsUnder": CUOTA_BOSNIA,
            "params": {
                "PA": 0, 
                "hitProb": float(PROB_PROYECTADA_USA), 
                "meanRuns": float(edge_usa), # Inyecta el cálculo de edge directo en la matriz
                "meanRBI": float(kelly_usa),  # Pasa la fracción de Kelly al renderizador del panel derecho
                "meanHR": 0
            }
        },
        {
            "id": "fb_usa_goles",
            "name": "Total de Goles (Over/Under)",
            "team": "TOTAL",
            "marketType": "combo",
            "line": float(LINEA_GOLES),
            "oddsOver": CUOTA_GOLES_OVER,
            "oddsUnder": CUOTA_GOLES_UNDER,
            "params": {
                "PA": 0, 
                "hitProb": float(prob_over_goles), 
                "meanRuns": float(edge_over if edge_over > edge_under else edge_under),
                "meanRBI": float(kelly_over if edge_over > edge_under else kelly_under),
                "meanHR": float(PROYECCION_MEDIA_GOLES)
            }
        },
        {
            "id": "fb_usa_btts",
            "name": "Ambos Equipos Marcan (Sí/No)",
            "team": "TOTAL",
            "marketType": "combo",
            "line": 0.5,
            "oddsOver": CUOTA_BTTS_SI,
            "oddsUnder": CUOTA_BTTS_NO,
            "params": {
                "PA": 0, 
                "hitProb": float(PROB_PROYECTADA_BTTS_SI), 
                "meanRuns": float(edge_btts_si),
                "meanRBI": float(kelly_btts_si),
                "meanHR": 0
            }
        }
    ]

    slate.append({
        "id": "g_futbol_usa_bosnia",
        "sport": "futbol",
        "matchup": "Estados Unidos vs Bosnia (Mundial 2026)",
        "short": "USAvsBIH",
        "props": props_partido
    })

    return slate

if __name__ == "__main__":
    print("[⚡] Ejecutando el Motor del Modelo Quant de Fútbol...")
    output_data = generate_quantum_slate()
    
    with open("slate_hoy.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print("[✨] 'slate_hoy.json' sobrescrito con éxito. Los tres mercados analíticos están calculados.")
