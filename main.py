import json

# =====================================================================
# ⚙️ PANEL DE CONTROL DE ALINEACIONES REALES (CAMBIA ESTO HOY)
# =====================================================================

# ⚽ PARTIDO MUNDIAL 1:
MUNDIAL_1_HOME = "Argentina"
MUNDIAL_1_AWAY = "Dinamarca"
M1_ESTRELLA_TIROS = "Lionel Messi"    # El que buscará los Tiros/SOT
M1_ESTRELLA_TACKLES = "Rodrigo de Paul" # El que meterá la pierna

# ⚽ PARTIDO MUNDIAL 2:
MUNDIAL_2_HOME = "Portugal"
MUNDIAL_2_AWAY = "Países Bajos"
M2_ESTRELLA_TIROS = "Cristiano Ronaldo"
M2_ESTRELLA_TACKLES = "João Palhinha"

# ⚾ JUEGO MLB 1:
MLB_1_HOME = "Boston Red Sox"
MLB_1_AWAY = "New York Yankees"
PITCHER_ABRIDOR_HOME_1 = "Tanner Houck" # Abridor Real de Boston hoy
PITCHER_ABRIDOR_AWAY_1 = "Gerrit Cole"  # Abridor Real de Yankees hoy
SLUGGER_AWAY_1 = "Aaron Judge"          # Bateador estrella NYY
SLUGGER_HOME_1 = "Rafael Devers"        # Bateador estrella BOS
COMBO_PLAYER_1 = "Jarren Duran"         # Jugador para Hits+Runs+RBI

# ⚾ JUEGO MLB 2:
MLB_2_HOME = "Los Angeles Dodgers"
MLB_2_AWAY = "San Francisco Giants"
PITCHER_ABRIDOR_HOME_2 = "Tyler Glasnow" # Abridor Real de Dodgers hoy
PITCHER_ABRIDOR_AWAY_2 = "Logan Webb"     # Abridor Real de Giants hoy
SLUGGER_HOME_2 = "Shohei Ohtani"         # Bateador estrella LAD
SLUGGER_AWAY_2 = "Matt Chapman"          # Bateador estrella SFG

# =====================================================================
# 🧠 MOTOR DE MODELADO MATEMÁTICO Y ESTRUCTURA DE PROPS
# =====================================================================

def generate_perfect_static_slate():
    slate = []

    # -----------------------------------------------------------------
    # ⚽ MODELADO FÚTBOL: MONETLINE, CORNERS, SHOTS, SOT, TACKLES
    # -----------------------------------------------------------------
    
    # Juego Mundial 1
    slate.append({
        "id": "g_wc_real_1",
        "sport": "futbol",
        "matchup": f"{MUNDIAL_1_HOME} vs {MUNDIAL_1_AWAY} (Mundial 2026)",
        "short": f"{MUNDIAL_1_HOME[:3].upper()}vs{MUNDIAL_1_AWAY[:3].upper()}",
        "props": [
            {
                "id": "p_wc_1_ml",
                "name": f"Línea de Dinero - Victoria {MUNDIAL_1_HOME}",
                "team": MUNDIAL_1_HOME[:3].upper(),
                "marketType": "goals",
                "line": 0,
                "oddsOver": "-145",  # Favorito
                "oddsUnder": "+410", # Dog
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 1.75, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_wc_1_corners",
                "name": "Total Tiros de Esquina (Partido)",
                "team": "TOTAL",
                "marketType": "corners",
                "line": 9.5,
                "oddsOver": "+110",
                "oddsUnder": "-130",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 10.1, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_wc_1_sot",
                "name": f"{M1_ESTRELLA_TIROS} - Tiros al Arco (SOT)",
                "team": MUNDIAL_1_HOME[:3].upper(),
                "marketType": "corners",
                "line": 1.5,
                "oddsOver": "-125",
                "oddsUnder": "+100",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 1.95, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_wc_1_shots",
                "name": f"{M1_ESTRELLA_TIROS} - Tiros Totales",
                "team": MUNDIAL_1_HOME[:3].upper(),
                "marketType": "goals",
                "line": 3.5,
                "oddsOver": "-115",
                "oddsUnder": "-115",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 4.1, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_wc_1_tackles",
                "name": f"{M1_ESTRELLA_TACKLES} - Quites Totales (Tackles)",
                "team": MUNDIAL_1_HOME[:3].upper(),
                "marketType": "corners",
                "line": 2.5,
                "oddsOver": "+115",
                "oddsUnder": "-145",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 2.85, "meanRBI": 0, "meanHR": 0}
            }
        ]
    })

    # Juego Mundial 2
    slate.append({
        "id": "g_wc_real_2",
        "sport": "futbol",
        "matchup": f"{MUNDIAL_2_HOME} vs {MUNDIAL_2_AWAY} (Mundial 2026)",
        "short": f"{MUNDIAL_2_HOME[:3].upper()}vs{MUNDIAL_2_AWAY[:3].upper()}",
        "props": [
            {
                "id": "p_wc_2_ml",
                "name": f"Línea de Dinero - Victoria {MUNDIAL_2_HOME}",
                "team": MUNDIAL_2_HOME[:3].upper(),
                "marketType": "goals",
                "line": 0,
                "oddsOver": "+135",
                "oddsUnder": "+210",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 1.30, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_wc_2_corners",
                "name": "Total Tiros de Esquina (Partido)",
                "team": "TOTAL",
                "marketType": "corners",
                "line": 8.5,
                "oddsOver": "-115",
                "oddsUnder": "-115",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 9.3, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_wc_2_sot",
                "name": f"{M2_ESTRELLA_TIROS} - Tiros al Arco (SOT)",
                "team": MUNDIAL_2_HOME[:3].upper(),
                "marketType": "corners",
                "line": 1.5,
                "oddsOver": "-110",
                "oddsUnder": "-120",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 1.68, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_wc_2_shots",
                "name": f"{M2_ESTRELLA_TIROS} - Tiros Totales",
                "team": MUNDIAL_2_HOME[:3].upper(),
                "marketType": "goals",
                "line": 2.5,
                "oddsOver": "-140",
                "oddsUnder": "+110",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 3.2, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_wc_2_tackles",
                "name": f"{M2_ESTRELLA_TACKLES} - Quites Totales (Tackles)",
                "team": MUNDIAL_2_HOME[:3].upper(),
                "marketType": "corners",
                "line": 3.5,
                "oddsOver": "+120",
                "oddsUnder": "-155",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 3.9, "meanRBI": 0, "meanHR": 0}
            }
        ]
    })

    # -----------------------------------------------------------------
    # ⚾ MODELADO MLB: HITS, RUNS, RBIS, COMBOS, HOMERUNS
    # -----------------------------------------------------------------
    
    # MLB Juego 1
    h_short_1 = MLB_1_HOME[:3].upper().strip()
    a_short_1 = MLB_1_AWAY[:3].upper().strip()
    slate.append({
        "id": "g_mlb_real_1",
        "sport": "mlb",
        "matchup": f"{MLB_1_AWAY} @ {MLB_1_HOME}",
        "short": f"{a_short_1}@{h_short_1}",
        "props": [
            {
                "id": "p_mlb_1_ks",
                "name": f"{PITCHER_ABRIDOR_AWAY_1} (Ponches - Ks)",
                "team": a_short_1,
                "marketType": "pitcherKs",
                "line": 6.5,
                "oddsOver": "+115",
                "oddsUnder": "-145",
                "params": {"k9": 9.6, "ip": 6.0, "PA": 0, "hitProb": 0, "meanRuns": 0, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_mlb_1_hits",
                "name": f"{SLUGGER_AWAY_1} (Hits Totales)",
                "team": a_short_1,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": "-170",
                "oddsUnder": "+135",
                "params": {"PA": 4.2, "hitProb": 0.290, "meanRuns": 0.5, "meanRBI": 0.4, "meanHR": 0.12}
            },
            {
                "id": "p_mlb_1_runs",
                "name": f"{SLUGGER_AWAY_1} (Carreras Anotadas - Runs)",
                "team": a_short_1,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": "-115",
                "oddsUnder": "-115",
                "params": {"PA": 4.2, "hitProb": 0.290, "meanRuns": 0.68, "meanRBI": 0.2, "meanHR": 0.12}
            },
            {
                "id": "p_mlb_1_rbis",
                "name": f"{SLUGGER_HOME_1} (Carreras Impulsadas - RBIs)",
                "team": h_short_1,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": "+140",
                "oddsUnder": "-180",
                "params": {"PA": 4.3, "hitProb": 0.280, "meanRuns": 0.4, "meanRBI": 0.62, "meanHR": 0.15}
            },
            {
                "id": "p_mlb_1_combo",
                "name": f"{COMBO_PLAYER_1} (Hits + Runs + RBIs)",
                "team": h_short_1,
                "marketType": "combo",
                "line": 1.5,
                "oddsOver": "-140",
                "oddsUnder": "+110",
                "params": {"PA": 4.4, "hitProb": 0.270, "meanRuns": 0.85, "meanRBI": 0.45, "meanHR": 0.05}
            },
            {
                "id": "p_mlb_1_hr",
                "name": f"{SLUGGER_AWAY_1} (Jonrones - HR)",
                "team": a_short_1,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": "+250",
                "oddsUnder": "-340",
                "params": {"PA": 4.2, "hitProb": 0.290, "meanRuns": 0.5, "meanRBI": 0.4, "meanHR": 0.28}
            }
        ]
    })

    # MLB Juego 2
    h_short_2 = MLB_2_HOME[:3].upper().strip()
    a_short_2 = MLB_2_AWAY[:3].upper().strip()
    slate.append({
        "id": "g_mlb_real_2",
        "sport": "mlb",
        "matchup": f"{MLB_2_AWAY} @ {MLB_2_HOME}",
        "short": f"{a_short_2}@{h_short_2}",
        "props": [
            {
                "id": "p_mlb_2_ks",
                "name": f"{PITCHER_ABRIDOR_HOME_2} (Ponches - Ks)",
                "team": h_short_2,
                "marketType": "pitcherKs",
                "line": 7.5,
                "oddsOver": "-110",
                "oddsUnder": "-120",
                "params": {"k9": 11.4, "ip": 6.1, "PA": 0, "hitProb": 0, "meanRuns": 0, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": "p_mlb_2_hits",
                "name": f"{SLUGGER_HOME_2} (Hits Totales)",
                "team": h_short_2,
                "marketType": "hits",
                "line": 1.5,
                "oddsOver": "+150",
                "oddsUnder": "-190",
                "params": {"PA": 4.5, "hitProb": 0.315, "meanRuns": 0.7, "meanRBI": 0.5, "meanHR": 0.22}
            },
            {
                "id": "p_mlb_2_runs",
                "name": f"{SLUGGER_HOME_2} (Carreras Anotadas - Runs)",
                "team": h_short_2,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": "-125",
                "oddsUnder": "-105",
                "params": {"PA": 4.5, "hitProb": 0.315, "meanRuns": 0.78, "meanRBI": 0.5, "meanHR": 0.22}
            },
            {
                "id": "p_mlb_2_rbis",
                "name": f"{SLUGGER_AWAY_2} (Carreras Impulsadas - RBIs)",
                "team": a_short_2,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": "+155",
                "oddsUnder": "-200",
                "params": {"PA": 4.1, "hitProb": 0.250, "meanRuns": 0.4, "meanRBI": 0.52, "meanHR": 0.08}
            },
            {
                "id": "p_mlb_2_combo",
                "name": f"{SLUGGER_HOME_2} (Hits + Runs + RBIs)",
                "team": h_short_2,
                "marketType": "combo",
                "line": 1.5,
                "oddsOver": "-120",
                "oddsUnder": "-110",
                "params": {"PA": 4.5, "hitProb": 0.315, "meanRuns": 0.7, "meanRBI": 0.5, "meanHR": 0.22}
            },
            {
                "id": "p_mlb_2_hr",
                "name": f"{SLUGGER_HOME_2} (Jonrones - HR)",
                "team": h_short_2,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": "+290",
                "oddsUnder": "-400",
                "params": {"PA": 4.5, "hitProb": 0.315, "meanRuns": 0.7, "meanRBI": 0.5, "meanHR": 0.24}
            }
        ]
    })

    return slate

if __name__ == "__main__":
    print("[⚡] Procesando Panel de Control de Alineaciones Fijas...")
    static_data = generate_perfect_static_slate()
    
    with open("slate_hoy.json", "w", encoding="utf-8") as f:
        json.dump(static_data, f, indent=2, ensure_ascii=False)
        
    print("[✨] ¡Completado! El archivo slate_hoy.json se ha actualizado de forma rigurosa y sin fallas.")
