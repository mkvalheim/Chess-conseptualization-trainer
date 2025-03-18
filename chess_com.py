import requests
import re

def get_pgn_from_chess_com(url):
    try:
        # Extract username and game ID from URL
        # Example URL: https://www.chess.com/game/live/123456789
        # or https://www.chess.com/game/daily/123456789
        match = re.search(r'chess\.com/game/(?:live|daily)/(\d+)', url)
        if not match:
            print("Could not extract game ID from URL")
            return None
            
        game_id = match.group(1)
        print(f"Extracted game ID: {game_id}")
        
        # Use the correct API endpoint for games
        api_url = f"https://api.chess.com/pub/games/{game_id}"
        print(f"Requesting URL: {api_url}")
        
        response = requests.get(api_url)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")  # Print first 200 chars of response
        
        if response.status_code == 200:
            game_data = response.json()
            pgn = game_data.get('pgn')
            if pgn:
                print("Successfully retrieved PGN")
                return pgn
            else:
                print("No PGN found in response")
                return None
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error fetching PGN from chess.com API: {str(e)}")
        return None 