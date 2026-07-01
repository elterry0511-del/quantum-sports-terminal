import json

# =====================================================================
# 🎛️ PANEL DE CONTROL MANUAL: ESTADOS UNIDOS vs BOSNIA
# =====================================================================
# Cambia los nombres, líneas, cuotas y proyecciones estadísticas aquí abajo.
# El sistema usará la "proyeccion_esperada" para calcular el Edge matemático.

# 1. GANADOR DEL PARTIDO (MONEYLINE)
CUOTA_USA_GANADOR = "-165"
CUOTA_BOSNIA_GANADOR = "+450"
PROYECCION_GOLES_USA = 2.10    # Cuántos goles esperas que meta USA hoy

# 2. TIROS DE ESQUINA (CORNERS)
LINEA_CORNERS = 9.5
CUOTA_CORNERS_OVER = "+110"
CUOTA_CORNERS_UNDER = "-135"
PROYECCION_CORNERS_TOTALES = 10.4  # Los corners que tu análisis proyecta

# 3. TIROS A PUERTA (SHOTS ON TARGET)
JUGADOR_SOT = "Christian Pulisic"
LINEA_SOT = 1.5
CUOTA_SOT_OVER = "-120"
CUOTA_SOT_UNDER = "-110"
PROYECCION_SOT_JUGADOR = 1.95  # Tiros al arco esperados para este jugador

# 4. TIROS TOTALES (TOTAL SHOTS)
JUGADOR_TIROS = "Christian Pulisic"
LINEA_TIROS = 3.5
CUOTA_TIROS_OVER = "+105"
CUOTA_TIROS_UNDER = "-130"
PROYECCION_TIROS_TOTALES = 4.20  # Intentos de tiro totales esperados

# 5. ENTRADAS EFECTIVAS (TACKLES)
JUGADOR_TACKLES = "Weston McKennie"
LINEA_TACKLES = 2.5
CUOTA_TACKLES_OVER = "+115"
CUOTA_TACKLES_UNDER = "-145"
PROYECCION_TACKLES_JUGADOR = 2.90 # Tackles/Quites esperados hoy

# =====================================================================
# 🧠 MOTOR CUÁNTICO DE ENSAMBLAJE (NO MODIFICAR ESTA SECCIÓN)
# =====================================================================

def build_manual_football_slate():
    return [{
        "id": "g_wc_usa_bih",
        "sport": "futbol",
        "matchup": "Estados Unidos vs Bosnia (Mundial 2026)",
        "short": "USAvsBIH",
        "props": [
            {
                "id": "p_fb_ml",
                "name": "Línea de Dinero - Victoria USA",
                "team": "USA",
                "marketType": "goals",
                "line": 0,
                "oddsOver": CUOTA_USA_GANADOR,
                "oddsUnder": CUOTA_BOSNIA_GANADOR,
                "params": {"PA": 0, "hitProb": 0, "meanRuns": float(PROYECCION_GOLES_USA), "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_fb_corners",
                "name": "Total Tiros de Esquina (Partido)",
                "team": "TOTAL",
                "marketType": "corners",
                "line": float(LINEA_CORNERS),
                "oddsOver": CUOTA_CORNERS_OVER,
                "oddsUnder": CUOTA_CORNERS_UNDER,
                "params": {"PA": 0, "hitProb": 0, "meanRuns": float(PROYECCION_CORNERS_TOTALES), "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_fb_sot",
                "name": f"{JUGADOR_SOT} - Tiros a Puerta (SOT)",
                "team": "USA",
                "marketType": "corners",
                "line": float(LINEA_SOT),
                "oddsOver": CUOTA_SOT_OVER,
                "oddsUnder": CUOTA_SOT_UNDER,
                "params": {"PA": 0, "hitProb": 0, "meanRuns": float(PROYECCION_SOT_JUGADOR), "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_fb_shots",
                "name": f"{JUGADOR_TIROS} - Tiros Totales",
                "team": "USA",
                "marketType": "goals",
                "line": float(LINEA_TIROS),
                "oddsOver": CUOTA_TIROS_OVER,
                "oddsUnder": CUOTA_TIROS_UNDER,
                "params": {"PA": 0, "hitProb": 0, "meanRuns": float(PROYECCION_TIROS_TOTALES), "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_fb_tackles",
                "name": f"{JUGADOR_TACKLES} - Quites Totales (Tackles)",
                "team": "USA",
                "marketType": "corners",
                "line": float(LINEA_TACKLES),
                "oddsOver": CUOTA_TACKLES_OVER,
                "oddsUnder": CUOTA_TACKLES_UNDER,
                "params": {"PA": 0, "hitProb": 0, "meanRuns": float(PROYECCION_TACKLES_JUGADOR), "meanRBI": 0, "meanHR": 0}
            }
        ]
    }]

if __name__ == "__main__":
    print("[⚡] Compilando datos manuales para USA vs Bosnia...")
    data = build_manual_football_slate()
    
    with open("slate_hoy.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print("[✨] ¡Éxito! Tu pizarra de fútbol personalizada está lista y cargada.")
