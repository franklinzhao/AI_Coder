#```python
import random

# The game board
board = [' ' for _ in range(9)]

# Function to insert an 'X' or 'O' at a specified position
def insert_letter(pos, letter):
    board[pos] = letter
    return board

# Function to check if space is free
def space_is_free(pos):
    return board[pos] == ' '

# Function to print the board
def print_board(board):
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])

# Function to check if the board is full
def is_board_full(board):
    return board.count(' ') == 0

# Function to check for a win
def is_winner(bo, le):
    winning_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for combo in winning_combos:
        if bo[combo[0]] == le and bo[combo[1]] == le and bo[combo[2]] == le:
            return True
    return False

# Function to check for a tie
def is_tie(board):
    return ' ' not in board and not is_winner(board, 'X') and not is_winner(board, 'O')

# Minimax algorithm for AI move
def minimax(board, depth, is_maximizing):
    if is_winner(board, 'O'):
        return 10
    elif is_winner(board, 'X'):
        return -10
    elif is_tie(board):
        return 0

    if is_maximizing:
        best_score = -1000
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Main game loop
def main():
    try:
        print("Welcome to Tic Tac Toe!")
        while True:
            print_board(board)
            move = input("Enter your move (1-9): ")
            if space_is_free(int(move) - 1):
                insert_letter(int(move) - 1, 'X')
                if is_winner(board, 'X'):
                    print_board(board)
                    print("You win!")
                    break
                elif is_tie(board):
                    print_board(board)
                    print("It's a tie!")
                    break
                else:
                    # AI's move
                    best_score = -1000
                    best_move = 0
                    for i in range(len(board)):
                        if board[i] == ' ':
                            board[i] = 'O'
                            score = minimax(board, 0, False)
                            board[i] = ' '
                            if score > best_score:
                                best_score = score
                                best_move = i
                    insert_letter(best_move, 'O')
                    if is_winner(board, 'O'):
                        print_board(board)
                        print("O wins!")
                        break
            else:
                print("Invalid move, try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Game over.")
        
if __name__ == "__main__":
    main()
#```