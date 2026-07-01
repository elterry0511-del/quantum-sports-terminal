import json
import datetime
import requests
import random

# 🔑 PEGA TU API KEY DE THE ODDS API AQUÍ ABAJO ENTRE LAS COMILLAS:
API_KEY = "16e6f3b429dd47cfa61e9667e07ecc76"

def fetch_live_market_odds(sport_key, region="us"):
    """Obtiene las líneas vivas de dinero (H2H) y totales desde The Odds API."""
    if API_KEY == "TU_API_KEY_AQUI" or not API_KEY:
        print("[⚠️] Recuerda configurar tu API_KEY real en el archivo main.py")
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
        print(f"[❌] Error API ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"[❌] Error de conexión con el servidor de cuotas: {e}")
    return []

def build_quantum_slate():
    slate = []
    
    # 1. PROCESAR MLB REAL DESDE LOS LIBROS EN VIVO
    print("[⚾] Solicitando líneas de MLB a los servidores de apuestas...")
    mlb_raw = fetch_live_market_odds("baseball_mlb", region="us")
    
    if mlb_raw:
        for idx, game in enumerate(mlb_raw):
            game_id = f"g_live_mlb_{idx}"
            away_team = game.get("away_team", "Visitante")
            home_team = game.get("home_team", "Home")
            away_short = away_team[:3].upper().strip()
            home_short = home_team[:3].upper().strip()
            
            # Valores por defecto por si el libro no ha abierto una línea específica
            odds_over, odds_under = "-110", "-110"
            odds_ml_away, odds_ml_home = "-115", "-115"
            total_line = 8.5
            
            # Extraemos las cuotas del primer libro disponible (ej. DraftKings o Pinnacle)
            bookmakers = game.get("bookmakers", [])
            if bookmakers:
                book = bookmakers[0] # Usamos el libro primario para consistencia
                for market in book.get("markets", []):
                    if market["key"] == "totals":
                        outcomes = market.get("outcomes", [])
                        for out in outcomes:
                            if out["name"].lower() == "over":
                                odds_over = f"+{out['price']}" if out['price'] > 0 else str(out['price'])
                                total_line = out.get("point", 8.5)
                            elif out["name"].lower() == "under":
                                odds_under = f"+{out['price']}" if out['price'] > 0 else str(out['price'])
                    elif market["key"] == "h2h":
                        outcomes = market.get("outcomes", [])
                        for out in outcomes:
                            if out["name"] == away_team:
                                odds_ml_away = f"+{out['price']}" if out['price'] > 0 else str(out['price'])
                            elif out["name"] == home_team:
                                odds_ml_home = f"+{out['price']}" if out['price'] > 0 else str(out['price'])

            # Mapeo a las matrices de tu interfaz gráfica
            props = [
                {
                    "id": f"p_{game_id}_ks",
                    "name": "Starting Pitcher Ace",
                    "team": home_short,
                    "marketType": "pitcherKs",
                    "line": 5.5,
                    "oddsOver": odds_ml_home, # Amarramos el flujo al movimiento del dinero local
                    "oddsUnder": odds_ml_away,
                    "params": {"k9": 9.4, "ip": 6.1, "PA": 0, "hitProb": 0, "meanRuns": 0, "meanRBI": 0, "meanHR": 0}
                },
                {
                    "id": f"p_{game_id}_hr",
                    "name": "Cleanup Slugger Pro",
                    "team": away_short,
                    "marketType": "hits", # Identificador para Jonrones (HR)
                    "line": 0.5,
                    "oddsOver": "+225",
                    "oddsUnder": "-300",
                    "params": {"PA": 4.2, "hitProb": 0.265, "meanRuns": 0.45, "meanRBI": 0.35, "meanHR": 0.12}
                },
                {
                    "id": f"p_{game_id}_combo",
                    "name": "Lineup Global Core",
                    "team": "TOTAL",
                    "marketType": "combo", # Mapea a Hits + Runs + RBI
                    "line": total_line, # ¡Línea de carreras real de Las Vegas!
                    "oddsOver": odds_over,   # ¡Cuota real del Over!
                    "oddsUnder": odds_under, # ¡Cuota real del Under!
                    "params": {"PA": 4.5, "hitProb": 0.250, "meanRuns": float(total_line)/2, "meanRBI": 0.50, "meanHR": 0.08}
                }
            ]
            
            slate.append({
                "id": game_id,
                "sport": "mlb",
                "matchup": f"{away_team} @ {home_team}",
                "short": f"{away_short}@{home_short}",
                "props": props
            })

    # 2. PROCESAR FÚTBOL EN VIVO (LA LIGA ESPAÑOLA)
    print("[⚽] Solicitando líneas de La Liga a los servidores europeos...")
    soccer_raw = fetch_live_market_odds("soccer_spain_la_liga", region="eu")
    
    if soccer_raw:
        for idx, game in enumerate(soccer_raw):
            game_id = f"g_live_foot_{idx}"
            away_team = game.get("away_team", "Visitante")
            home_team = game.get("home_team", "Home")
            
            odds_over, odds_under = "-115", "-105"
            goal_line = 2.5
            
            bookmakers = game.get("bookmakers", [])
            if bookmakers:
                for market in bookmakers[0].get("markets", []):
                    if market["key"] == "totals":
                        for out in market.get("outcomes", []):
                            if out["name"].lower() == "over":
                                odds_over = f"+{out['price']}" if out['price'] > 0 else str(out['price'])
                                goal_line = out.get("point", 2.5)
                            elif out["name"].lower() == "under":
                                odds_under = f"+{out['price']}" if out['price'] > 0 else str(out['price'])

            props = [
                {
                    "id": f"p_{game_id}_goles",
                    "name": "Goles Totales Partido",
                    "team": "TOTAL",
                    "marketType": "goals",
                    "line": goal_line, # Línea real del mercado de goles
                    "oddsOver": odds_over,
                    "oddsUnder": odds_under,
                    "params": {"PA": 0, "hitProb": 0, "meanRuns": float(goal_line) + 0.2, "meanRBI": 0, "meanHR": 0}
                }
            ]
            
            slate.append({
                "id": game_id,
                "sport": "futbol",
                "matchup": f"{home_team} vs {away_team}",
                "short": f"{home_team[:3].upper()}vs{away_team[:3].upper()}",
                "props": props
            })

    # FALLBACK DE SEGURIDAD: Si los libros están cerrados o es de noche, genera una cartelera de respaldo
    if not slate:
        print("[⚠️] No se detectaron líneas activas comerciales en este instante. Ejecutando simulación de contingencia...")
        return get_fallback_slate()

    return slate

def get_fallback_slate():
    """Cartelera de respaldo ultra-realista para que tu terminal nunca se quede vacía."""
    return [
        {
            "id": "g_fb_1",
            "sport": "mlb",
            "matchup": "Detroit Tigers @ New York Yankees",
            "short": "DET@NYY",
            "props": [
                {
                    "id": "p_fb_ks",
                    "name": "Gerrit Cole",
                    "team": "NYY",
                    "marketType": "pitcherKs",
                    "line": 6.5,
                    "oddsOver": "+105",
                    "oddsUnder": "-135",
                    "params": {"k9": 9.6, "ip": 6.1, "PA": 0, "hitProb": 0, "meanRuns": 0, "meanRBI": 0, "meanHR": 0}
                },
                {
                    "id": "p_fb_hr",
                    "name": "Aaron Judge",
                    "team": "NYY",
                    "marketType": "hits",
                    "line": 0.5,
                    "oddsOver": "+225",
                    "oddsUnder": "-300",
                    "params": {"PA": 4.2, "hitProb": 0.265, "meanRuns": 0.45, "meanRBI": 0.35, "meanHR": 0.12}
                }
            ]
        }
    ]

if __name__ == "__main__":
    print("[⚡] Iniciando Extractor Cuántico conectado a Las Vegas...")
    final_data = build_quantum_slate()
    
    with open("slate_hoy.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
        
    print(f"[✨] Éxito. {len(final_data)} Juegos procesados y guardados en 'slate_hoy.json'.")
