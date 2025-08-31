import pandas as pd
import chess
import chess.engine
import os

#Rutas
INPUT_CSV = r'D:\Chess\Analisis\data\processed\games_raw_black.csv'
OUUTPUT_CSV = r'D:\Chess\Analisis\data\processed\games_with_analysis_black.csv'
STOCKFISH_PATH = r'D:\Chess\Analisis\engine\stockfish\stockfish-windows-x86-64-avx2.exe'

#Conexion con Stockfish
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

#Leer csv
df = pd.read_csv(INPUT_CSV)

#columnas para analisis
df['best_move'] = ""
df["eval_before"] = 0.0
df["eval_after"] = 0.0
df["centipawn_loss"] = 0.0

for i, row in df.iterrows():
    board = chess.Board(row['fen_before'])

    info_before = engine.analyse(board, chess.engine.Limit(depth=15))
    eval_before = info_before['score'].pov(board.turn).score(mate_score=10000)

    best_move = engine.play(board, chess.engine.Limit(depth=15)).move

    try:
        board.push_san(row['move_san'])
    except:
        continue

    info_after = engine.analyse(board, chess.engine.Limit(depth=15))
    eval_after = info_after['score'].pov(board.turn).score(mate_score=10000)

    centipawn_loss = eval_before - eval_after

    df.at[i, "best_move"] = best_move.uci()
    df.at[i, "eval_before"] = eval_before
    df.at[i, "eval_after"] = eval_after
    df.at[i, "centipawn_loss"] = centipawn_loss

    if i % 50 == 0:
        print(f"Analizadas {i} jugadas...")

df.to_csv(OUUTPUT_CSV, index=False)
print(f"Analisis completado y guardado en {OUUTPUT_CSV}")

engine.quit()
