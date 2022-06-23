import pygame, sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 900

FONT = pygame.font.Font("assets/Roboto-Regular.ttf", 100)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

BOARD = pygame.image.load("assets/Board.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")

BG_COLOR = (214, 201, 227)

SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (64, 64))

pygame.display.update()


def render_board(board, graphical_board):
    for i in range(3):
        for j in range(3):
            if board[i*3 + j + 1] == 'X':
                graphical_board[i][j][0] = X_IMG
                graphical_board[i][j][1] = X_IMG.get_rect(center=(j*300+150, i*300+150))
            elif board[i*3 + j + 1] == 'O':
                graphical_board[i][j][0] = O_IMG
                graphical_board[i][j][1] = O_IMG.get_rect(center=(j*300+150, i*300+150))


def player_move(board, graphical_board):
    current_pos = pygame.mouse.get_pos()
    converted_x = (current_pos[0] - 16) / 900 * 3
    converted_y = (current_pos[1]) / 900 * 3
    if board[math.floor(converted_y)*3 + math.floor(converted_x) + 1] == ' ':
        board[math.floor(converted_y)*3 + math.floor(converted_x) + 1] = 'O'

    render_board(board, graphical_board)

    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    
    return board


def insert_letter(board, letter, pos):
    board[pos] = letter


def is_winner(board, letter):
    return ((board[7] == letter and board[8] == letter and board[9] == letter) or # horizontally
            (board[4] == letter and board[5] == letter and board[6] == letter) or 
            (board[1] == letter and board[2] == letter and board[3] == letter) or
            (board[1] == letter and board[4] == letter and board[7] == letter) or # vertically
            (board[2] == letter and board[5] == letter and board[8] == letter) or 
            (board[3] == letter and board[6] == letter and board[9] == letter) or
            (board[1] == letter and board[5] == letter and board[9] == letter) or # diagonally
            (board[3] == letter and board[5] == letter and board[7] == letter))


def is_draw(board):
    return list(board.values()).count(' ') == 0 and not is_winner(board, 'X') and not is_winner(board, 'O')



def select_random(l: list):
    import random
    ln = len(l)
    r = random.randrange(0, ln)
    return l[r]


# def comp_move_simple_ai(board, graphical_board):
#     move_found = False
#     possible_moves = []
#     for i in range(len(board)):
#         for j in range(len(board)):
#             if board[i][j] != 'O' and board[i][j] != 'X':
#                 possible_moves.append([i, j])

#     for l in ['O', 'X']:
#         for i, j in possible_moves:
#             board_copy = [cpy[:] for cpy in board[:]]
#             board_copy[i][j] = l
#             if is_winner(board_copy, l):
#                 move = [i, j]
#                 move_found = True

#     if not move_found:
#         corners_open = []
#         for i in possible_moves:
#             if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
#                 corners_open.append(i)
#         if len(corners_open) > 0:
#             move = select_random(corners_open)
#             move_found = True

#     if not move_found:
#         if [1, 1] in possible_moves:
#             move = [1, 1]
#             move_found = True

#     if not move_found:
#         edges_open = []
#         for i in possible_moves:
#             if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
#                 edges_open.append(i)
#         if len(edges_open) > 0:
#             move = select_random(edges_open)
#             move_found = True
    
#     board[move[0]][move[1]] = 'X'
#     render_board(board, graphical_board)
#     for i in range(3):
#         for j in range(3):
#             if graphical_board[i][j][0] is not None:
#                 SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
#     return board


def minimax(board, depth, is_maximizing):
    if is_winner(board, 'X') and depth == 0:
        return 10
    if is_winner(board, 'X'):   # computer
        return 1
    elif is_winner(board, 'O'): # player
        return -1
    elif is_draw(board):
        return 0
    
    if is_maximizing:
        best_score = -1000

        for key in board.keys():
            if board[key] == ' ':
                board[key] = 'X'
                score = minimax(board, depth + 1, False)
                board[key] = ' '
                if score > best_score:
                    best_score = score
        return best_score
    
    else:
        best_score = 1000

        for key in board.keys():
            if board[key] == ' ':
                board[key] = 'O'
                score = minimax(board, depth + 1, True)
                board[key] = ' '
                if score < best_score:
                    best_score = score
        return best_score


def comp_move_minimax(board: dict, graphical_board):
    best_score = -1000
    best_move = 0

    for key in board.keys():
        if board[key] == ' ':
            board[key] = 'X'
            score = minimax(board, 0, False)
            board[key] = ' '
            if score > best_score:
                best_score = score
                best_move = key
    insert_letter(board, 'X', best_move)
    render_board(board, graphical_board)
    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    return board


def check_win(board, graphical_board):
    winner = None
    for row in range(0, 3):
        if((board[row*3+0+1] == board[row*3+1+1] == board[row*3+2+1]) and (board [row*3+0+1] != ' ')):
            winner = board[row*3+0+1]
            for i in range(0, 3):
                graphical_board[row][i][0] = pygame.image.load(f"assets/Winning {winner}.png")
                SCREEN.blit(graphical_board[row][i][0], graphical_board[row][i][1])
            pygame.display.update()
            return winner

    for col in range(0, 3):
        if((board[0*3+col+1] == board[1*3+col+1] == board[2*3+col+1]) and (board[0*3+col+1] !=' ')):
            winner =  board[0*3+col+1]
            for i in range(0, 3):
                graphical_board[i][col][0] = pygame.image.load(f"assets/Winning {winner}.png")
                SCREEN.blit(graphical_board[i][col][0], graphical_board[i][col][1])
            pygame.display.update()
            return winner
   
    if (board[1] == board[5] == board[9]) and (board[1] != ' '):
        winner =  board[1]
        graphical_board[0][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[0][0][0], graphical_board[0][0][1])
        graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[1][1][0], graphical_board[1][1][1])
        graphical_board[2][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[2][2][0], graphical_board[2][2][1])
        pygame.display.update()
        return winner
          
    if (board[3] == board[5] == board[7]) and (board[3] != ' '):
        winner =  board[3]
        graphical_board[0][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[0][2][0], graphical_board[0][2][1])
        graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[1][1][0], graphical_board[1][1][1])
        graphical_board[2][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[2][0][0], graphical_board[2][0][1])
        pygame.display.update()
        return winner
    
    if winner == None:
        for i in range(len(board)//3):
            for j in range(len(board)//3):
                if board[i*3+j+1] == ' ':
                    return None
        return "DRAW"


def main():
    board = {
            1: ' ', 2: ' ', 3: ' ',
            4: ' ', 5: ' ', 6: ' ',
            7: ' ', 8: ' ', 9: ' '}

    graphical_board = [[[None, None], [None, None], [None, None]], 
                        [[None, None], [None, None], [None, None]], 
                        [[None, None], [None, None], [None, None]]]

    game_finished = False
    user_starts = True
    if user_starts == False:
        board = comp_move_minimax(board, graphical_board)
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            check_board = board.copy()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_finished:
                    board = {
                            1: ' ', 2: ' ', 3: ' ',
                            4: ' ', 5: ' ', 6: ' ',
                            7: ' ', 8: ' ', 9: ' '}

                    graphical_board = [[[None, None], [None, None], [None, None]], 
                                        [[None, None], [None, None], [None, None]], 
                                        [[None, None], [None, None], [None, None]]]

                    SCREEN.fill(BG_COLOR)
                    SCREEN.blit(BOARD, (64, 64))

                    game_finished = False
                    if user_starts == False:
                        board = comp_move_minimax(board, graphical_board)
                        pygame.display.update()
                    else:
                        pygame.display.update()
                    continue
                
                board = player_move(board, graphical_board)
                pygame.display.update()

                if check_win(board, graphical_board) is not None:
                    game_finished = True
                else:
                    if check_board != board:
                        board = comp_move_minimax(board, graphical_board)
                        pygame.display.update()

                    if check_win(board, graphical_board) is not None:
                        game_finished = True
            

if __name__ == '__main__':
    main()