import json
import datetime
import requests

def fetch_mlb_slate():
    # Obtiene la fecha actual de forma dinámica
    today = datetime.date.today().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}"
    
    try:
        response = requests.get(url, timeout=12)
        data = response.json()
    except Exception as e:
        print(f"Error en la conexión de red con MLB API: {e}")
        return get_backup_slate()

    slate = []
    dates = data.get("dates", [])
    if not dates:
        print("No hay partidos programados en la API para hoy. Cargando slate base de simulación...")
        return get_backup_slate()

    games = dates[0].get("games", [])
    for index, game in enumerate(games):
        game_id = f"g_mlb_{game.get('gamePk', index)}"
        away_team = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "Visitante")
        home_team = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "Home")
        
        away_short = away_team[:3].upper()
        home_short = home_team[:3].upper()
        matchup = f"{away_team} vs {home_team}"
        
        # Generación de perfiles analíticos base para el motor matemático del frontend
        props = [
            {
                "id": f"p_{game_id}_hits",
                "name": "Leadoff Hitter Pro",
                "team": away_short,
                "marketType": "hits",
                "line": 0.5,
                "oddsOver": "-145",
                "oddsUnder": "+115",
                "params": {"PA": 4.1, "hitProb": 0.265, "meanRuns": 0.45, "meanRBI": 0.35, "meanHR": 0.05}
            },
            {
                "id": f"p_{game_id}_pitcher",
                "name": "Starting Pitcher Ace",
                "team": home_short,
                "marketType": "pitcherKs",
                "line": 5.5,
                "oddsOver": "-110",
                "oddsUnder": "-110",
                "params": {"k9": 9.5, "ip": 5.2, "PA": 0, "hitProb": 0, "meanRuns": 0, "meanRBI": 0, "meanHR": 0}
            },
            {
                "id": f"p_{game_id}_combo",
                "name": "Cleanup Slugger",
                "team": away_short,
                "marketType": "combo",
                "line": 1.5,
                "oddsOver": "-120",
                "oddsUnder": "-110",
                "params": {"PA": 4.2, "hitProb": 0.240, "meanRuns": 0.55, "meanRBI": 0.65, "meanHR": 0.15}
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

def get_backup_slate():
    # Estructura de respaldo en caso de caídas de servidores externos o postemporada
    return [
        {
            "id": "g_mock_1",
            "sport": "mlb",
            "matchup": "New York Yankees vs Boston Red Sox",
            "short": "NYY@BOS",
            "props": [
                {
                    "id": "p_mock_1",
                    "name": "Aaron Judge",
                    "team": "NYY",
                    "marketType": "hits",
                    "line": 0.5,
                    "oddsOver": "-155",
                    "oddsUnder": "+125",
                    "params": {"PA": 4.3, "hitProb": 0.285, "meanRuns": 0.6, "meanRBI": 0.6, "meanHR": 0.18}
                },
                {
                    "id": "p_mock_2",
                    "name": "Gerrit Cole",
                    "team": "NYY",
                    "marketType": "pitcherKs",
                    "line": 6.5,
                    "oddsOver": "-115",
                    "oddsUnder": "-115",
                    "params": {"k9": 10.2, "ip": 6.0, "PA": 0, "hitProb": 0, "meanRuns": 0, "meanRBI": 0, "meanHR": 0}
                }
            ]
        }
    ]

if __name__ == "__main__":
    print("Iniciando extracción del pipeline de datos...")
    cron_slate = fetch_mlb_slate()
    
    # Guarda el archivo JSON que el index.html leerá de forma automática
    with open("slate_hoy.json", "w", encoding="utf-8") as f:
        json.dump(cron_slate, f, indent=2, ensure_ascii=False)
        
    print("¡Proceso exitoso! Archivo 'slate_hoy.json' actualizado y listo.")
