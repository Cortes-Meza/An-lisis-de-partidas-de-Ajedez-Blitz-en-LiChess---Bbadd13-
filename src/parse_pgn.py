import os 
import re
import pandas as pd
import chess.pgn

# Rutas de los archivos
GAMES_FOLDER = r'D:\Chess\Analisis\data\games\blitz' # Parditas Blitz 
OUTPUT_CSV = r'D:\Chess\Analisis\data\processed\games_raw_black.csv' # Archivo CSV de salida

def parse_pgn_file(pgn_path):
    rows = []
    with open (pgn_path, encoding='utf-8') as f:
        while True:

            game = chess.pgn.read_game(f)
            if game is None:
                break

            headers = game.headers
            board =  game.board()
            ply = 0

            for node in game.mainline():

                if node.move is None:
                    continue

                move =  node.move
                time_tag = None

                if node.comment:
                    match = re.search(r"\[%clk ([0-9:]+)\]", node.comment)
                    if match:
                        time_tag = match.group(1)

                row = {
                    "game_id": headers.get("GameId", "NA"),
                    "date": headers.get("Date", "NA"),
                    "white": headers.get("White", "NA"),
                    "black": headers.get("Black", "NA"),
                    "white_elo": headers.get("WhiteElo", "NA"),
                    "black_elo": headers.get("BlackElo", "NA"),
                    "result": headers.get("Result", "NA"),
                    "opening": headers.get("Opening", "NA"),
                    "eco": headers.get("ECO", "NA"),
                    "move_number": ply + 1,
                    "player_to_move": "white" if board.turn else "black",
                    "move_san": board.san(move),
                    "fen_before": board.fen(),
                    "time_remaining": time_tag
                }

                rows.append(row)
                board.push(move)
                ply += 1
    return rows

def main():
    all_arrows = []

    for filename in os.listdir(GAMES_FOLDER):
        if filename.endswith(".pgn"):
            file_path = os.path.join(GAMES_FOLDER, filename)
            print(f"Parsing {filename}...")
            rows = parse_pgn_file(file_path)
            all_arrows.extend(rows)

    df = pd.DataFrame(all_arrows)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok = True)
    df.to_csv(OUTPUT_CSV, index = False)
    print(f"Data saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()



