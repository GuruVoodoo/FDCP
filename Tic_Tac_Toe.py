"""
FDCP Tic-Tac-Toe: Jon's Approach - Simplified

Navigate state space once. Store. O(1) forever after.

The insight: Tic-tac-toe is FINITE. 
Don't manage randomness. Don't evaluate heuristics.
Just KNOW the answer.
"""

WIN_LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
    [0, 4, 8], [2, 4, 6]              # diagonals
]

# THE CACHE - filled once, used forever
CACHE = {}

def check_winner(board):
    for line in WIN_LINES:
        if board[line[0]] == board[line[1]] == board[line[2]] != 0:
            return board[line[0]]
    return None

def get_empty(board):
    return [i for i in range(9) if board[i] == 0]

def minimax(board, is_maximizing):
    """
    Standard minimax with memoization.
    The memo IS the lookup table.
    First time through: compute.
    Every time after: O(1).
    """
    key = (tuple(board), is_maximizing)
    if key in CACHE:
        return CACHE[key]
    
    winner = check_winner(board)
    if winner == 1:  # X wins
        return (10, None)
    if winner == 2:  # O wins
        return (-10, None)
    
    empty = get_empty(board)
    if not empty:
        return (0, None)  # Draw
    
    if is_maximizing:  # X's turn
        best_score = -100
        best_move = empty[0]
        for move in empty:
            board[move] = 1
            score, _ = minimax(board, False)
            board[move] = 0
            if score > best_score:
                best_score = score
                best_move = move
        result = (best_score, best_move)
    else:  # O's turn
        best_score = 100
        best_move = empty[0]
        for move in empty:
            board[move] = 2
            score, _ = minimax(board, True)
            board[move] = 0
            if score < best_score:
                best_score = score
                best_move = move
        result = (best_score, best_move)
    
    CACHE[key] = result
    return result

def get_ai_move(board, ai_is_x):
    """
    Get optimal move. O(1) after first computation.
    """
    is_maximizing = ai_is_x  # X maximizes, O minimizes
    _, move = minimax(list(board), is_maximizing)
    return move

def play_game_ai_vs_random(ai_is_x=True):
    """AI plays against random opponent."""
    import random
    
    board = [0] * 9
    is_x_turn = True
    
    while True:
        winner = check_winner(board)
        if winner:
            return winner
        
        empty = get_empty(board)
        if not empty:
            return 0  # Draw
        
        ai_turn = (is_x_turn and ai_is_x) or (not is_x_turn and not ai_is_x)
        
        if ai_turn:
            move = get_ai_move(board, ai_is_x)
        else:
            move = random.choice(empty)
        
        board[move] = 1 if is_x_turn else 2
        is_x_turn = not is_x_turn

def test_unbeatable(n_games=1000):
    """
    Run n games. AI should NEVER lose.
    """
    import random
    random.seed(42)  # For reproducibility
    
    print(f"Testing {n_games} games...")
    
    wins = 0
    losses = 0
    draws = 0
    
    # AI as X (first mover advantage)
    for i in range(n_games // 2):
        result = play_game_ai_vs_random(ai_is_x=True)
        if result == 1:  # X wins, AI wins
            wins += 1
        elif result == 2:  # O wins, AI loses
            losses += 1
        else:
            draws += 1
    
    # AI as O (second mover)
    for i in range(n_games // 2):
        result = play_game_ai_vs_random(ai_is_x=False)
        if result == 2:  # O wins, AI wins
            wins += 1
        elif result == 1:  # X wins, AI loses
            losses += 1
        else:
            draws += 1
    
    print(f"\nCache size: {len(CACHE)} positions")
    print(f"\nResults over {n_games} games:")
    print(f"  AI Wins:   {wins}")
    print(f"  AI Losses: {losses}")
    print(f"  Draws:     {draws}")
    
    if losses == 0:
        print("\n✓ UNBEATABLE")
        print("  0 losses out of", n_games, "games")
        print("  Navigate once. Store. Never recompute.")
        print("  The professor was right: you can't beat it.")
    else:
        print(f"\n✗ Something wrong - {losses} losses")
    
    return wins, losses, draws

if __name__ == "__main__":
    test_unbeatable(1000)
