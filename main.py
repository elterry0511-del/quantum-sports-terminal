import math
import json

# =====================================================================
# 🎛️ PANEL DE INYECCIÓN MANUAL: ESTADOS UNIDOS vs BOSNIA
# =====================================================================
# Cambia únicamente los valores de este bloque con las cuotas de tu casa de
# apuestas y tus probabilidades estimadas. El sistema procesará el resto.

# 1. GANADOR DEL PARTIDO (MONEYLINE)
CUOTA_USA_GANADOR = "-165"          # Cuota americana para la victoria de USA
CUOTA_BOSNIA_GANADOR = "+450"       # Cuota americana para la victoria de Bosnia
PROB_PROYECTADA_USA = 0.65          # Tu probabilidad estimada para USA (0.0 a 1.0)
PROB_PROYECTADA_BOSNIA = 0.15       # Tu probabilidad estimada para Bosnia (0.0 a 1.0)

# 2. TOTAL DE GOLES (OVER / UNDER)
LINEA_GOLES = 2.5                   # Línea del mercado de goles
CUOTA_GOLES_OVER = "+110"           # Cuota para el Over (Más de)
CUOTA_GOLES_UNDER = "-135"          # Cuota para el Under (Menos de)
PROB_PROYECTADA_OVER_GOLES = 0.58   # Tu probabilidad estimada para el Over (0.0 a 1.0)
PROB_PROYECTADA_UNDER_GOLES = 0.42  # Tu probabilidad estimada para el Under (0.0 a 1.0)

# 3. AMBOS EQUIPOS MARCAN (BTTS - SÍ / NO)
CUOTA_BTTS_SI = "-115"              # Cuota para el "Sí marcan ambos"
CUOTA_BTTS_NO = "-105"              # Cuota para el "No marcan ambos"
PROB_PROYECTADA_BTTS_SI = 0.54      # Tu probabilidad estimada para el SÍ (0.0 a 1.0)
PROB_PROYECTADA_BTTS_NO = 0.46      # Tu probabilidad estimada para el NO (0.0 a 1.0)

# =====================================================================
# 🧠 MOTOR DE PROCESAMIENTO CUANTITATIVO (EDGE & CRITERIO DE KELLY)
# =====================================================================

def american_to_decimal(american_odds):
    """Convierte cuotas americanas a multiplicadores de ganancia neta."""
    try:
        odds = float(american_odds)
        if odds > 0:
            return odds / 100.0
        else:
            return 100.0 / abs(odds)
    except:
        return 0.0

def calculate_edge_and_kelly(p_proyectada, net_odds):
    """Calcula el Edge exacto y aplica la fracción de Quarter Kelly (25%)."""
    if net_odds <= 0:
        return 0.0, 0.0
    implied_p = 1.0 / (net_odds + 1.0)
    edge = p_proyectada - implied_p
    
    if edge > 0:
        q = 1.0 - p_proyectada
        kelly_completo = (p_proyectada * net_odds - q) / net_odds
        fractional_kelly = max(0.0, kelly_completo * 0.25) # Filtro de riesgo estricto
    else:
        fractional_kelly = 0.0
    return edge, fractional_kelly

def generate_clean_football_slate():
    # Conversión de cuotas netas
    b_usa = american_to_decimal(CUOTA_USA_GANADOR)
    b_bosnia = american_to_decimal(CUOTA_BOSNIA_GANADOR)
    b_over = american_to_decimal(CUOTA_GOLES_OVER)
    b_under = american_to_decimal(CUOTA_GOLES_UNDER)
    b_btts_si = american_to_decimal(CUOTA_BTTS_SI)
    b_btts_no = american_to_decimal(CUOTA_BTTS_NO)

    # Procesamiento estadístico de ventajas (Edge)
    edge_usa, kelly_usa = calculate_edge_and_kelly(PROB_PROYECTADA_USA, b_usa)
    
    edge_over, kelly_over = calculate_edge_and_kelly(PROB_PROYECTADA_OVER_GOLES, b_over)
    edge_under, kelly_under = calculate_edge_and_kelly(PROB_PROYECTADA_UNDER_GOLES, b_under)
    
    edge_btts_si, kelly_btts_si = calculate_edge_and_kelly(PROB_PROYECTADA_BTTS_SI, b_btts_si)
    edge_btts_no, kelly_btts_no = calculate_edge_and_kelly(PROB_PROYECTADA_BTTS_NO, b_btts_no)

    # Empaquetado estructural limpio para la interfaz
    props = [
        {
            "id": "fb_usa_ml",
            "name": "Línea de Dinero - Victoria USA",
            "team": "USA",
            "marketType": "goals",
            "line": 0,
            "oddsOver": CUOTA_USA_GANADOR,
            "oddsUnder": CUOTA_BOSNIA_GANADOR,
            "params": {
                "PA": 0,
                "hitProb": float(PROB_PROYECTADA_USA),
                "meanRuns": float(edge_usa),      # Se mapea directo a la columna 'Edge Limpio'
                "meanRBI": float(kelly_usa),       # Envía la sugerencia de tamaño de apuesta a la derecha
                "meanHR": 0
            }
        },
        {
            "id": "fb_usa_goles",
            "name": f"Total de Goles (Línea: {LINEA_GOLES})",
            "team": "TOTAL",
            "marketType": "combo",
            "line": float(LINEA_GOLES),
            "oddsOver": CUOTA_GOLES_OVER,
            "oddsUnder": CUOTA_GOLES_UNDER,
            "params": {
                "PA": 0,
                "hitProb": float(PROB_PROYECTADA_OVER_GOLES),
                "meanRuns": float(edge_over if edge_over >= edge_under else edge_under),
                "meanRBI": float(kelly_over if edge_over >= edge_under else kelly_under),
                "meanHR": 0
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
                "meanRuns": float(edge_btts_si if edge_btts_si >= edge_btts_no else edge_btts_no),
                "meanRBI": float(kelly_btts_si if edge_btts_si >= edge_btts_no else kelly_btts_no),
                "meanHR": 0
            }
        }
    ]

    return [{
        "id": "g_futbol_usa_bosnia",
        "sport": "futbol",
        "matchup": "Estados Unidos vs Bosnia (Mundial 2026)",
        "short": "USAvsBIH",
        "props": props
    }]

if __name__ == "__main__":
    print("[⚡] Compilando exclusivamente mercados principales de fútbol...")
    clean_data = generate_clean_football_slate()
    
    with open("slate_hoy.json", "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)
        
    print("[✨] Proceso completado con éxito. Pizarra simplificada generada.")
