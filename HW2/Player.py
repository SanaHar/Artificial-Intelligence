from Board import BoardUtility
import random
import math

class Player:
    def __init__(self, player_piece):
        self.player_piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth
        
    def standard_move(self, move):

        quadrant = move[0][0]
        quad_node = move[0][1]
        rotate_quadrant  = move[1][0]
        rotate_direction = move[1][1]
        ini_col = math.floor(((quadrant - 1) % 2) * 3)
        ini_row = math.floor(((quadrant - 1) / 2) * 3)
        
        if quadrant%2==0:
            ini_row = ini_row - 1
        if quad_node <= 3:
            row = ini_row
            col = ini_col + quad_node-1
        elif quad_node <= 6:
            row = ini_row + 1
            col = ini_col + quad_node - 4
        elif quad_node <= 9:
            row = ini_row + 2
            col = ini_col + quad_node - 7
        
        return  [[row, col], quadrant, rotate_direction]
        
        
    def copy_matrix(self, board):
        new_board = [[0 for x in range(6)] for x in range(6)]
        for i in range(6):
            for j in range(6):
                new_board[i][j] = board[i][j]
        return new_board
    
    
    def rotate(self, board, move):
        ini_col = math.floor(((move[0] - 1) % 2) * 3)
        ini_row = math.floor(((move[0] - 1) / 2) * 3)
        
        if move[0] % 2 == 0:
            ini_row = ini_row - 1
            
        new_board = self.copy_matrix(board)
        if move[1]=='clockwise':
            for i in range(ini_row, ini_row + 3):
                for j in range(ini_col, ini_col + 3):
                    new_board[j + ini_row - ini_col][2 - i + ini_row + ini_col] = board[i][j]
                    
        elif move[1]=='anticlockwise':
            for i in range(ini_row, ini_row + 3):
                for j in range(ini_col, ini_col + 3):
                    new_board[2 - j + ini_row + ini_col][i - ini_row + ini_col] = board[i][j]
                    
        return new_board
    
    
    def do_move(self, board, player_piece, move):
        
        ini_col = math.floor(((move[0] - 1) % 2) * 3)
        ini_row = math.floor(((move[0] - 1) / 2) * 3)
        if move[0] % 2==0:
            ini_row = ini_row - 1
            
        if move[1] <= 3:
            if board[ini_row][(ini_col + move[1] - 1)]==0:
                board[ini_row][(ini_col + move[1] - 1)] = player_piece
        elif move[1] <= 6:
            if board[ini_row + 1][(ini_col + move[1] - 4)]==0:
                board[ini_row + 1][(ini_col + move[1] - 4)] = player_piece
        elif move[1] <= 9:
            if board[ini_row + 2][(ini_col + move[1]) - 7]==0:
                board[ini_row + 2][(ini_col + move[1]) - 7] = player_piece
        return

    def heuristic_helper(self, mov_scr, player_piece, board, ptr):
        if ptr[0] >= 6 or ptr[1] >= 6:
            return mov_scr
        
        if mov_scr >= 5:
            return mov_scr
        
        if board[ptr[0]][ptr[1]]!=player_piece:
            return mov_scr
        
        else:
            scr1 = self.heuristic_helper(mov_scr + 1, player_piece, board, ((ptr[0] + 1), (ptr[1])))
            scr2 = self.heuristic_helper(mov_scr + 1, player_piece, board, ((ptr[0]), (ptr[1] + 1)))
            scr3 = self.heuristic_helper(mov_scr + 1, player_piece, board, ((ptr[0] + 1), (ptr[1] + 1)))
            return max(scr1, scr2, scr3, mov_scr)
    
    
    def matrix_heuristics(self, player_piece, board):
        mov_score = 0
        for i in range(6):
            for j in range(6):
                temp = 0
                if board[i][j]==player_piece:
                    temp = self.heuristic_helper(0, player_piece, board, (i, j))
                mov_score = max(mov_score, temp)
        return mov_score
    
    
    def generate_rand_move(self, board):
        quadrant = random.choice(range(1, 4))  # which quadrant the play piece is placed
        quad_node = random.choice(range(1, 9))  # which node within the quadrant the piece is placed
        valid = False
        while not valid:
            ini_col = math.floor(((quadrant - 1) % 2) * 3)  # starting column
            ini_row = math.floor(((quadrant - 1) / 2) * 3)  # starting row
            
            
            if quadrant % 2==0:
                ini_row = ini_row - 1
                
                
            if quad_node <= 3:
                if board[ini_row][(ini_col + quad_node - 1)]==0:
                    valid = True
                    break
                    
            elif quad_node <= 6:
                if board[ini_row + 1][(ini_col + quad_node - 4)]==0:
                    valid = True
                    break
                    
            elif quad_node <= 9:
                if board[ini_row + 2][(ini_col + quad_node - 7)]==0:
                    valid = True
                    break
                    
            quadrant = random.choice(range(1, 4))
            quad_node = random.choice(range(1, 9))
        
        rotate_quadrant = random.choice(range(1, 4))
        rotate_direction = random.choice(['anticlockwise', 'clockwise','skip'])
        
        move = ((quadrant, quad_node), (rotate_quadrant, rotate_direction))
        return move
    
    
    def available_moves(self, board):
        moves = []
        quad = 0  # quadrant 1,2,3,or 4
        pos = 0
        for i in range(6):
            for j in range(6):
                if board[i][j]==0:
                    if j < 3:
                        if i < 3:
                            quad = 1
                        else:
                            quad = 3
                    else:
                        if i < 3:
                            quad = 2
                        else:
                            quad = 4
                    ini_row = math.floor(((quad - 1) / 2) * 3)
                    ini_col = math.floor(((quad - 1) % 2) * 3)
                    if quad % 2 == 0:
                        ini_row = ini_row - 1
                    pos = (3 * (i - ini_row)) + (j - ini_col) + 1
                    
                    for x in [1, 2, 3, 4]:
                        moves.append(((quad, pos), (x, 'clockwise')))
                        moves.append(((quad, pos), (x, 'anticlockwise')))
                        moves.append(((quad, pos), (x, 'skip')))
        return moves
    
    def mini_max_algo(self, moves, player_piece, board, depth, alpha, beta, maximizing):
        
        colors = [1, 2]
        if moves==None or moves==[]:
            moves = []
            moves.append(self.generate_rand_move(board))
        if depth==0:
            return (moves[-1], (self.matrix_heuristics(player_piece, board)))
        if BoardUtility.is_terminal_state(board) or BoardUtility.is_draw(board):
            return (moves[-1], 5)
        
        if maximizing:
            best_move = (self.generate_rand_move(board), -5)
            for move in self.available_moves(board):
                tmp_board = self.copy_matrix(board)  # temporary matrix
                self.do_move(tmp_board, player_piece, move[0])
                tmp_board = self.rotate(tmp_board, move[1])
                moves.append(move)
                score = self.mini_max_algo(moves, player_piece, tmp_board, depth - 1, alpha, beta, False)[1]
                if best_move[1] < score:
                    best_move = (move, score)
                alpha = max(score, beta)
                if beta <= alpha:
                    break
            
            return best_move
        
        else:
            best_move = (self.generate_rand_move(board), 5)
            for move in self.available_moves(board):
                if moves == None:
                    moves = []
                tmp_board = self.copy_matrix(board)
                self.do_move(tmp_board, colors[-player_piece], move[0])
                tmp_board  = self.rotate(tmp_board , move[1])
                moves = moves.append(move)
                score = self.mini_max_algo(moves, player_piece, tmp_board, depth - 1, alpha, beta, True)[1]
                if best_move[1] > score:
                    best_move = (move, score)
                beta = min(score, beta)
                if beta <= alpha:
                    break

            return best_move
   
    
    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        move = self.mini_max_algo(list(), self.player_piece, board, self.depth, -5, 5, True)[0]
        return self.standard_move(move)
    
class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic
    
    def standard_move(self, move):

        quadrant = move[0][0]
        quad_node = move[0][1]
        rotate_quadrant  = move[1][0]
        rotate_direction = move[1][1]
        
        ini_col = math.floor(((quadrant - 1) % 2) * 3)
        ini_row = math.floor(((quadrant - 1) / 2) * 3)
        
        if quadrant % 2== 0:
            ini_row = ini_row - 1
        if quad_node <= 3:
            row = ini_row
            col = ini_col + quad_node-1
        elif quad_node <= 6:
            row = ini_row + 1
            col = ini_col + quad_node - 4
        elif quad_node <= 9:
            row = ini_row + 2
            col = ini_col + quad_node - 7
        
        return  [[row, col], quadrant, rotate_direction]
        
        
    def copy_matrix(self, board):
        new_board = [[0 for x in range(6)] for x in range(6)]
        for i in range(6):
            for j in range(6):
                new_board[i][j] = board[i][j]
        return new_board
    
    
    def rotate(self, board, move):
        ini_col = math.floor(((move[0] - 1) % 2) * 3)
        ini_row = math.floor(((move[0] - 1) / 2) * 3)
        
        if move[0] % 2 == 0:
            ini_row = ini_row - 1
            
        new_board = self.copy_matrix(board)
        if move[1] == 'clockwise':
            for i in range(ini_row, ini_row + 3):
                for j in range(ini_col, ini_col + 3):
                    new_board[j + ini_row - ini_col][2 - i + ini_row + ini_col] = board[i][j]
                    
        elif move[1] == 'anticlockwise':
            for i in range(ini_row, ini_row + 3):
                for j in range(ini_col, ini_col + 3):
                    new_board[2 - j + ini_row + ini_col][i - ini_row + ini_col] = board[i][j]
                    
        return new_board
    
    
    def do_move(self, board, player_piece, move):
        
        ini_col = math.floor(((move[0] - 1) % 2) * 3)
        ini_row = math.floor(((move[0] - 1) / 2) * 3)
        if move[0] % 2 == 0:
            ini_row = ini_row - 1
            
        if move[1] <= 3:
            if board[ini_row][(ini_col + move[1] - 1)]==0:
                board[ini_row][(ini_col + move[1] - 1)] = player_piece
        elif move[1] <= 6:
            if board[ini_row + 1][(ini_col + move[1] - 4)]==0:
                board[ini_row + 1][(ini_col + move[1] - 4)] = player_piece
        elif move[1] <= 9:
            if board[ini_row + 2][(ini_col + move[1]) - 7]==0:
                board[ini_row + 2][(ini_col + move[1]) - 7] = player_piece
        return

    def heuristic_helper(self, mov_scr, player_piece, board, ptr):
        if ptr[0] >= 6 or ptr[1] >= 6:
            return mov_scr
        
        if mov_scr >= 5:
            return mov_scr
        
        if board[ptr[0]][ptr[1]]!= player_piece:
            return mov_scr
        
        else:
            scr1 = self.heuristic_helper(mov_scr + 1, player_piece, board, ((ptr[0] + 1), (ptr[1])))
            scr2 = self.heuristic_helper(mov_scr + 1, player_piece, board, ((ptr[0]), (ptr[1] + 1)))
            scr3 = self.heuristic_helper(mov_scr + 1, player_piece, board, ((ptr[0] + 1), (ptr[1] + 1)))
            return max(scr1, scr2, scr3, mov_scr)
    
    
    def matrix_heuristics(self, player_piece, board):
        mov_score = 0
        for i in range(6):
            for j in range(6):
                temp = 0
                if board[i][j] == player_piece:
                    temp = self.heuristic_helper(0, player_piece, board, (i, j))
                mov_score = max(mov_score, temp)
        return mov_score
    
    def generate_rand_move(self, board):
        quadrant = random.choice(range(1, 4))  # which quadrant the play piece is placed
        quad_node = random.choice(range(1, 9))  # which node within the quadrant the piece is placed
        valid = False
        while not valid:
            ini_col = math.floor(((quadrant - 1) % 2) * 3)  # starting column
            ini_row = math.floor(((quadrant - 1) / 2) * 3)  # starting row
            
            
            if quadrant % 2 == 0:
                ini_row = ini_row - 1
                
                
            if quad_node <= 3:
                if board[ini_row][(ini_col + quad_node - 1)]==0:
                    valid = True
                    break
                    
            elif quad_node <= 6:
                if board[ini_row + 1][(ini_col + quad_node - 4)]==0:
                    valid = True
                    break
                    
            elif quad_node <= 9:
                if board[ini_row + 2][(ini_col + quad_node - 7)]==0:
                    valid = True
                    break
                    
            quadrant = random.choice(range(1, 4))
            quad_node = random.choice(range(1, 9))
        
        rotate_quadrant = random.choice(range(1, 4))
        rotate_direction = random.choice(['anticlockwise', 'clockwise','skip'])
        
        move = ((quadrant, quad_node), (rotate_quadrant, rotate_direction))
        return move
    
    
    def available_moves(self, board):
        moves = []
        quad = 0  # quadrant 1,2,3,or 4
        pos = 0
        for i in range(6):
            for j in range(6):
                if board[i][j]==0:
                    if j < 3:
                        if i < 3:
                            quad = 1
                        else:
                            quad = 3
                    else:
                        if i < 3:
                            quad = 2
                        else:
                            quad = 4
                    ini_row = math.floor(((quad - 1) / 2) * 3)
                    ini_col = math.floor(((quad - 1) % 2) * 3)
                    if quad % 2 == 0:
                        ini_row = ini_row - 1
                    pos = (3 * (i - ini_row)) + (j - ini_col) + 1
                    
                    for x in [1, 2, 3, 4]:
                        moves.append(((quad, pos), (x, 'clockwise')))
                        moves.append(((quad, pos), (x, 'anticlockwise')))
                        moves.append(((quad, pos), (x, 'skip')))
        return moves
    
    def mini_max_algo(self, moves, player_piece, board, depth, alpha, beta, maximizing, prob):
        colors = [1, 2]
        if moves==None or moves==[]:
            moves = []
            moves.append(self.generate_rand_move(board))
        if depth==0:
            return (moves[-1], (self.matrix_heuristics(player_piece, board)))
        if BoardUtility.is_terminal_state(board) or BoardUtility.is_draw(board):
            return (moves[-1], 5)
        
        if maximizing:
            best_move = (self.generate_rand_move(board), -5)
            p = random.uniform(0,1)
            if p>prob:
                for move in self.available_moves(board):
                    tmp_board = self.copy_matrix(board)  # temporary matrix
                    self.do_move(tmp_board, player_piece, move[0])
                    tmp_board = self.rotate(tmp_board, move[1])
                    moves.append(move)
                    score = self.mini_max_algo(moves, player_piece, tmp_board, depth - 1, alpha, beta, False, prob)[1]
                    if best_move[1] < score:
                        best_move = (move, score)
                    alpha = max(score, beta)
                    if beta <= alpha:
                        break
            return best_move
        
        else:
            best_move = (self.generate_rand_move(board), 5)
            for move in self.available_moves(board):
                if moves==None:
                    moves = []
                tmp_board = self.copy_matrix(board)
                self.do_move(tmp_board, colors[-player_piece], move[0])
                tmp_board  = self.rotate(tmp_board , move[1])
                moves = moves.append(move)
                score = self.mini_max_algo(moves, player_piece, tmp_board, depth - 1, alpha, beta, True, prob)[1]
                if best_move[1] > score:
                    best_move = (move, score)
                beta = min(score, beta)
                if beta <= alpha:
                    break
            return best_move
        
    
    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        move = self.mini_max_algo(list(), self.player_piece, board, self.depth, -5, 5, True, self.prob_stochastic)[0]
        return self.standard_move(move)