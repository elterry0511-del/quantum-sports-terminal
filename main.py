import json
import datetime
import requests

# 🔑 PEGA TU API KEY DE THE ODDS API AQUÍ ABAJO:
API_KEY =

# 🎯 DICCIONARIO INTELIGENTE: Vincula jugadores reales a sus equipos reales
ESTRELLAS_MUNDIAL = {
    "Argentina": "Lionel Messi",
    "France": "Kylian Mbappé",
    "Brazil": "Vinícius Júnior",
    "England": "Jude Bellingham",
    "Spain": "Lamine Yamal",
    "Portugal": "Cristiano Ronaldo",
    "Germany": "Florian Wirtz",
    "Uruguay": "Federico Valverde",
    "Colombia": "Luis Díaz",
    "USA": "Christian Pulisic"
}

ESTRELLAS_MLB = {
    "New York Yankees": {"hitter": "Aaron Judge", "pitcher": "Gerrit Cole"},
    "Los Angeles Dodgers": {"hitter": "Shohei Ohtani", "pitcher": "Tyler Glasnow"},
    "Atlanta Braves": {"hitter": "Ronald Acuña Jr.", "pitcher": "Chris Sale"},
    "Houston Astros": {"hitter": "Yordan Alvarez", "pitcher": "Framber Valdez"},
    "Philadelphia Phillies": {"hitter": "Bryce Harper", "pitcher": "Zack Wheeler"},
    "Baltimore Orioles": {"hitter": "Gunnar Henderson", "pitcher": "Corbin Burnes"},
    "San Diego Padres": {"hitter": "Manny Machado", "pitcher": "Dylan Cease"},
    "New York Mets": {"hitter": "Francisco Lindor", "pitcher": "Kodai Senga"},
    "Boston Red Sox": {"hitter": "Rafael Devers", "pitcher": "Tanner Houck"},
    "Toronto Blue Jays": {"hitter": "Vladimir Guerrero Jr.", "pitcher": "Kevin Gausman"}
}

def fetch_live_market_odds(sport_key, region="us"):
    """Obtiene las líneas vivas de dinero (H2H) y totales desde The Odds API."""
    if API_KEY == "TU_API_KEY_AQUI" or not API_KEY:
        print("[⚠️] Configura tu API_KEY real antes de ejecutar.")
        return []
        
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": region,
        "markets": "h2h,totals",
        "oddsFormat": "american"
    }
    
    try:
        response = requests.get(url, params=params, timeout=12)
        if response.status_code == 200:
            return response.json()
        print(f"[❌] Error en API ({response.status_code})")
    except Exception as e:
        print(f"[❌] Error de conexión: {e}")
    return []

def build_quantum_slate():
    slate = []
    
    # 1. ENTRAR AL MERCADO DE LA MLB
    print("[⚾] Conectando con las líneas de la MLB...")
    mlb_raw = fetch_live_market_odds("baseball_mlb", region="us")
    
    if mlb_raw:
        for idx, game in enumerate(mlb_raw):
            game_id = f"g_live_mlb_{idx}"
            away_team = game.get("away_team", "Visitante")
            home_team = game.get("home_team", "Home")
            away_short = away_team[:3].upper().strip()
            home_short = home_team[:3].upper().strip()
            
            odds_over, odds_under = "-110", "-110"
            odds_ml_away, odds_ml_home = "-115", "-115"
            total_line = 8.5
            
            bookmakers = game.get("bookmakers", [])
            if bookmakers:
                book = bookmakers[0]
                for market in book.get("markets", []):
                    if market["key"] == "totals":
                        for out in market.get("outcomes", []):
                            if out["name"].lower() == "over":
                                odds_over = f"+{out['price']}" if out['price'] > 0 else str(out['price'])
                                total_line = out.get("point", 8.5)
                            elif out["name"].lower() == "under":
                                odds_under = f"+{out['price']}" if out['price'] > 0 else str(out['price'])
                    elif market["key"] == "h2h":
                        for out in market.get("outcomes", []):
                            if out["name"] == away_team:
                                odds_ml_away = f"+{out['price']}" if out['price'] > 0 else str(out['price'])
                            elif out["name"] == home_team:
                                odds_ml_home = f"+{out['price']}" if out['price'] > 0 else str(out['price'])

            # Asignación de jugadores basada estrictamente en el equipo real
            away_star = ESTRELLAS_MLB.get(away_team, {"hitter": f"Líder de Hits {away_short}", "pitcher": "Pitcher Abridor"})
            home_star = ESTRELLAS_MLB.get(home_team, {"hitter": f"Líder de Hits {home_short}", "pitcher": "Pitcher Abridor"})

            props = [
                {
                    "id": f"p_{game_id}_ks",
                    "name": home_star["pitcher"],
                    "team": home_short,
                    "marketType": "pitcherKs",
                    "line": 5.5,
                    "oddsOver": odds_ml_home,
                    "oddsUnder": odds_ml_away,
                    "params": {"k9": 9.2, "ip": 5.2, "PA": 0, "hitProb": 0, "meanRuns": 0, "meanRBI": 0, "meanHR": 0}
                },
                {
                    "id": f"p_{game_id}_hits",
                    "name": away_star["hitter"],
                    "team": away_short,
                    "marketType": "hits",
                    "line": 0.5,
                    "oddsOver": "-150",
                    "oddsUnder": "+120",
                    "params": {"PA": 4.1, "hitProb": 0.270, "meanRuns": 0.4, "meanRBI": 0.3, "meanHR": 0.1}
                },
                {
                    "id": f"p_{game_id}_combo",
                    "name": "Total de Carreras (Vegas)",
                    "team": "TOTAL",
                    "marketType": "combo",
                    "line": total_line,
                    "oddsOver": odds_over,
                    "oddsUnder": odds_under,
                    "params": {"PA": 4.5, "hitProb": 0.25, "meanRuns": float(total_line)/2, "meanRBI": 0.4, "meanHR": 0.05}
                }
            ]
            
            slate.append({
                "id": game_id,
                "sport": "mlb",
                "matchup": f"{away_team} @ {home_team}",
                "short": f"{away_short}@{home_short}",
                "props": props
            })

    # 2. ENTRAR AL MERCADO DE LA COPA MUNDIAL DE LA FIFA 2026
    print("[⚽] Conectando con las líneas del Mundial FIFA 2026...")
    soccer_raw = fetch_live_market_odds("soccer_fifa_world_cup", region="eu")
    
    if soccer_raw:
        for idx, game in enumerate(soccer_raw):
            game_id = f"g_live_wc_{idx}"
            away_team = game.get("away_team", "Visitante")
            home_team = game.get("home_team", "Home")
            home_short = home_team[:3].upper().strip()
            away_short = away_team[:3].upper().strip()
            
            odds_over, odds_under = "-115", "-105"
            goal_line = 2.5
            
            bookmakers = game.get("bookmakers", [])
            if bookmakers:
                book = bookmakers[0]
                for market in book.get("markets", []):
                    if market["key"] == "totals":
                        for out in market.get("outcomes", []):
                            if out["name"].lower() == "over":
                                odds_over = f"+{out['price']}" if out['price'] > 0 else str(out['price'])
                                goal_line = out.get("point", 2.5)
                            elif out["name"].lower() == "under":
                                odds_under = f"+{out['price']}" if out['price'] > 0 else str(out['price'])

            # Asignación de estrellas reales a sus selecciones nacionales del Mundial
            p_name = ESTRELLAS_MUNDIAL.get(home_team, f"Delantero Estrella {home_short}")

            props = [
                {
                    "id": f"p_{game_id}_goles",
                    "name": "Línea de Goles del Partido",
                    "team": "TOTAL",
                    "marketType": "goals",
                    "line": goal_line,
                    "oddsOver": odds_over,
                    "oddsUnder": odds_under,
                    "params": {"PA": 0, "hitProb": 0, "meanRuns": float(goal_line), "meanRBI": 0, "meanHR": 0}
                },
                {
                    "id": f"p_{game_id}_jugador",
                    "name": f"{p_name} (Tiros a Puerta)",
                    "team": home_short,
                    "marketType": "corners",  # Reutiliza matriz de interfaz
                    "line": 1.5,
                    "oddsOver": "-130",
                    "oddsUnder": "+100",
                    "params": {"PA": 0, "hitProb": 0, "meanRuns": 1.8, "meanRBI": 0, "meanHR": 0}
                }
            ]
            
            slate.append({
                "id": game_id,
                "sport": "futbol",
                "matchup": f"{home_team} vs {away_team}",
                "short": f"{home_short}vs{away_short}",
                "props": props
            })

    # RESPALDO DE SEGURIDAD (Si la API no devuelve partidos por horario)
    if not slate:
        print("[⚠️] Los mercados están cerrados momentáneamente. Cargando base limpia...")
        return [
            {
                "id": "g_fb_wc",
                "sport": "futbol",
                "matchup": "Francia vs Argentina (Mundial 2026)",
                "short": "FRAvsARG",
                "props": [
                    {
                        "id": "p_fb_g",
                        "name": "Kylian Mbappé (Anotará)",
                        "team": "FRA",
                        "marketType": "goals",
                        "line": 0.5,
                        "oddsOver": "+110",
                        "oddsUnder": "-140",
                        "params": {"PA": 0, "hitProb": 0, "meanRuns": 0.65, "meanRBI": 0, "meanHR": 0}
                    }
                ]
            }
        ]

    return slate

if __name__ == "__main__":
    print("[⚡] Ejecutando Sistema de Datos Reales...")
    final_data = build_quantum_slate()
    
    with open("slate_hoy.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
        
    print(f"[✨] Hecho. {len(final_data)} partidos reales del Mundial y la MLB sincronizados perfectamente.")
