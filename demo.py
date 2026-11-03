"""Offline demonstration using newly authored synthetic input."""
from app.normalize import normalize_for_game
from app.public_games import public_games_payload

if __name__ == '__main__':
    print(normalize_for_game('  الْكِتَاب  '))
    print(public_games_payload([{'game_id': 1, 'target_words': ['synthetic']}], 1))
