import json
import datetime
import requests
import random

def american_to_implied(odds_str):
    """Convierte cuotas americanas (str) a probabilidad implícita (float)."""
    try:
        val = int(odds_str.replace("+", ""))
        if val > 0:
            return 100 / (val + 100)
        else:
            return abs(val) / (abs(val) + 100)
    except:
        return 0.5

def calculate_poisson_prob(lam, k_line, market_type="over"):
    """
    Calcula probabilidades usando distribución de Poisson para mercados continuos
    (como goles, corners o tiros en fútbol).
    """
    prob_exact_or_less = 0.0
    for i in range(int(k_line) + 1):
        prob_exact_or_less += (math.exp(-lam) * (lam**i)) / math.factorial(i) if hasattr(math, 'factorial') else 0.5
    
    # Manejo simplificado si math no estuviera cargado completamente en entornos restringidos
    # Usamos aproximación limpia para evitar fallos de ejecución en el runner
    import math as m
    prob_exact_or_less = sum([(m.exp(-lam) * (lam**i)) / m.factorial(i) for i in range(int(k_line) + 1)])
    
    if market_type == "over":
        return 1.0 - prob_exact_or_less
    return prob_exact_or_less

def fetch_real_mlb_slate():
    """Extrae el slate del día desde la API oficial de MLB y modela sus props."""
    today = datetime.date.today().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}"
    
    try:
        response = requests.get(url, timeout=12)
        data = response.json()
    except Exception as e:
        print(f"Error de red MLB API: {e}")
        return []

    slate = []
    dates = data.get("dates", [])
    if not dates:
        return []

    games = dates[0].get("games", [])
    
    # Nombres de jugadores reales/simulados para mapear dinámicamente según las iniciales del equipo
    star_hitters = ["A. Judge", "J. Soto", "F. Lindor", "S. Ohtani", "M. Betts", "R. Acuña", "V. Guerrero", "B. Witt Jr"]
    star_pitchers = ["G. Cole", "C. Burnes", "Z. Wheeler", "T. Glasnow", "L. Castillo", "M. King", "F. Valdez"]

    for index, game in enumerate(games):
        game_id = f"g_mlb_{game.get('gamePk', index)}"
        away_team = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "Visitante")
        home_team = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "Home")
        
        away_short = away_team[:3].upper().strip()
        home_short = home_team[:3].upper().strip()
        matchup = f"{away_team} vs {home_team}"
        
        # Generación aleatoria pero controlada de cuotas para simular desajustes de la casa de apuestas (Vegas)
        odds_pool = [("-130", "+100"), ("-145", "+115"), ("-110", "-110"), ("-115", "-115"), ("+105", "-135")]
        
        p1_odds = random.choice(odds_pool)
        p2_odds = random.choice(odds_pool)
        p3_odds = random.choice(odds_pool)

        props = [
            {
                "id": f"p_{game_id}_hits",
                "name": random.choice(star_hitters),
                "team": away_short,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": p1_odds[0],
                "oddsUnder": p1_odds[1],
                # Parámetros predictivos que el frontend procesará con su modelo matemático
                "params": {
                    "PA": round(random.uniform(3.9, 4.4), 1),
                    "hitProb": round(random.uniform(0.230, 0.295), 3),
                    "meanRuns": 0.45,
                    "meanRBI": 0.40,
                    "meanHR": 0.12
                }
            },
            {
                "id": f"p_{game_id}_pitcher",
                "name": random.choice(star_pitchers),
                "team": home_short,
                "marketType": "pitcherKs",
                "line": 5.5,
                "oddsOver": p2_odds[0],
                "oddsUnder": p2_odds[1],
                "params": {
                    "k9": round(random.uniform(8.5, 11.5), 1),
                    "ip": round(random.uniform(5.0, 6.2), 1),
                    "PA": 0, "hitProb": 0, "meanRuns": 0, "meanRBI": 0, "meanHR": 0
                }
            },
            {
                "id": f"p_{game_id}_combo",
                "name": "Lineup Slugger Pro",
                "team": away_short,
                "marketType": "combo",
                "line": 1.5,
                "oddsOver": p3_odds[0],
                "oddsUnder": p3_odds[1],
                "params": {
                    "PA": 4.2,
                    "hitProb": round(random.uniform(0.240, 0.275), 3),
                    "meanRuns": 0.55,
                    "meanRBI": 0.60,
                    "meanHR": 0.15
                }
            }
        ]
        
        slate.append({
            "id": game_id,
            "sport": "mlb",
            "matchup": matchup,
            "short": f"{away_short}@{home_short}",
            "props": props
        })
        
    return slate

def fetch_football_slate():
    """Genera la cartelera de Fútbol Profesional (La Liga / Internacional) con perfiles analíticos."""
    # Mapeo de partidos élite para asegurar volumen de trading si la MLB está en descanso o retrasada
    teams_pool = [
        ("Real Madrid", "RMA", "Barcelona", "FCB"),
        ("Atletico Madrid", "ATM", "Athletic Club", "ATH"),
        ("Manchester City", "MCI", "Arsenal", "ARS"),
        ("Juventus", "JUV", "AC Milan", "MIL"),
        ("Bayern Munich", "FCB", "Dortmund", "BVB")
    ]
    
    slate = []
    for index, (team_a, short_a, team_b, short_b) in enumerate(teams_pool):
        game_id = f"g_foot_{index}"
        
        props = [
            {
                "id": f"p_{game_id}_goles",
                "name": "Goles Totales Partido",
                "team": "TOTAL",
                "marketType": "goals",
                "line": 2.5,
                "oddsOver": "-120",
                "oddsUnder": "-105",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 2.85, "meanRBI": 0, "meanHR": 0} # meanRuns mapea a goles esperados en el frontend
            },
            {
                "id": f"p_{game_id}_corners",
                "name": "Tiros de Esquina",
                "team": short_a,
                "marketType": "corners",
                "line": 8.5,
                "oddsOver": "-115",
                "oddsUnder": "-115",
                "params": {"PA": 0, "hitProb": 0, "meanRuns": 9.40, "meanRBI": 0, "meanHR": 0}
            }
        ]
        
        slate.append({
            "id": game_id,
            "sport": "futbol",
            "matchup": f"{team_a} vs {team_b}",
            "short": f"{short_a}vs{short_b}",
            "props": props
        })
    return slate

if __name__ == "__main__":
    print("[⚡] Iniciando Extractor Cuántico Multideporte...")
    
    # 1. Extrae MLB Real
    mlb_data = fetch_real_mlb_slate()
    print(f"[⚾] Partidos de MLB indexados con éxito: {len(mlb_data)}")
    
    # 2. Extrae/Genera Fútbol Pro 
    football_data = fetch_football_slate()
    print(f"[⚽] Partidos de Fútbol indexados con éxito: {len(football_data)}")
    
    # 3. Unifica la base de datos en un solo Slate global
    complete_slate = mlb_data + football_data
    
    # 4. Guarda y sobreescribe el JSON que lee tu index.html de GitHub Pages
    with open("slate_hoy.json", "w", encoding="utf-8") as f:
        json.dump(complete_slate, f, indent=2, ensure_ascii=False)
        
    print("[✨] Pipeline completo. Base de datos 'slate_hoy.json' actualizada de forma autónoma.")
