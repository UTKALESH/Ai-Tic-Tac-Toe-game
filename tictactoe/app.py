from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initialize the board
board = [""] * 9

def is_winner(board, player):
    """Check if the player has won."""
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_positions:
        if all(board[i] == player for i in combo):
            return combo
    return None

def minimax(board, is_ai):
    """AI using the Minimax algorithm."""
    if is_winner(board, "O"):
        return 1
    if is_winner(board, "X"):
        return -1
    if "" not in board:
        return 0

    if is_ai:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

def ai_move():
    """Determine the AI's move."""
    best_score = -float("inf")
    move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global board
    data = request.json
    player_move = data["position"]
    if board[player_move] == "":
        board[player_move] = "X"
        winner_combo = is_winner(board, "X")
        if winner_combo:
            return jsonify({"status": "win", "winner": "Player", "board": board, "combo": winner_combo})
        if "" not in board:
            return jsonify({"status": "draw", "board": board})
        ai_position = ai_move()
        board[ai_position] = "O"
        winner_combo = is_winner(board, "O")
        if winner_combo:
            return jsonify({"status": "win", "winner": "AI", "board": board, "combo": winner_combo})
        if "" not in board:
            return jsonify({"status": "draw", "board": board})
    return jsonify({"status": "ongoing", "board": board, "combo": None})

@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = [""] * 9
    return jsonify({"status": "reset", "board": board})

if __name__ == "__main__":
    app.run(debug=True)