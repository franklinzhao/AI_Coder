import random

# The game board
board = [' ' for _ in range(9)]

# Function to display the board
def display_board():
    """Display the current state of the board."""
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])

# Function to insert an element at a given position
def insert_board(position, element):
    """Insert an element at a given position on the board."""
    if board[position] == ' ':
        board[position] = element
        return True
    return False

# Function to check if the board is full
def is_board_full():
    """Check if the board is full."""
    return ' ' not in board

# Function to check for a win
def is_winner(player):
    """Check if a player has won."""
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Function to handle player move
def player_move():
    """Handle player move."""
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move < 0 or move >= 9:
                print("Invalid move. Please enter a number between 1 and 9.")
            elif not insert_board(move, 'X'):
                print("Position already occupied. Please choose another position.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

# Minimax algorithm to choose the best move
def minimax(is_maximizing):
    """Minimax algorithm to choose the best move."""
    if is_winner('O'):
        return 1
    elif is_winner('X'):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Function to handle computer move with strategy
def computer_move():
    """Handle computer move using Minimax strategy."""
    best_move = None
    best_score = -float('inf')
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i

    if best_move is not None:
        insert_board(best_move, 'O')

# Main game loop
def main():
    """Main function to run the Tic Tac Toe game."""
    while True:
        display_board()

        # Player move
        player_move()

        # Check if player has won
        if is_winner('X'):
            display_board()
            print("You win!")
            break

        # Check if the board is full
        if is_board_full():
            display_board()
            print("It's a tie!")
            break

        # Computer move
        computer_move()

        # Check if computer has won
        if is_winner('O'):
            display_board()
            print("Computer wins!")
            break

if __name__ == "__main__":
    main()
