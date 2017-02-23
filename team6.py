import random
import sys
import copy
import time

class Player6:
    # Player6 agent to play game.
    def __init__(self):
        self.ply
        #Rest of the variables will be defined

    # Function implementing minmax algorithm with alph-beta pruning.
    def MinMax(self, board, status_blocks, old_move, node_type_maxnode, player_sign, opponent_sign, depth, alpha, beta, best_row, best_coloumn):
    """
    board :- 16*16 matrix representing game board
    status_blocks :- bool flags list for all block give their status_blocks
    old_move :- list[2] contain x,y
    node_type_maxnode :- bool if 1 reffers to maxnode and 0 to minnode
    player_sign :- represent x or o of player
    opponent_sign :- represent x or o of opponent
    depth :- int represent current depth
    """

    if depth == self.MaxDepth:
        utility = self.get_utility(board,block,player_sign,opponent_sign)
        return (utility, best_row, best_coloumn)

    else:
        available_moves = find_valid_move_cells(board, block, old_move)

        NOT SURE ABOUT THIS
        if len(available_moves) == 0:       ##### No moves left at depth
            utility = get_utility()
            self.MaxDepth = max(depth, 3)
            return (utility, best_row, best_coloumn)

        if depth == 0:     """ If at first level we have around 56 cells then decrease level by 1 """
            if len(moves) > 17:
                self.MaxDepth = min(MaxDepth, 3)

        for move in available_moves:  # assign player sign whose turn is this
            if node_type_maxnode:
                board[move[0]][move[1]] = player_sign
            else:
                board[move[0]][move[1]] = opponent_sign

            utility = MinMax() # agains call MinMax

            if node_type_maxnode: """ Rules for PRUNING """
                if utility > alpha:
                    alpha = utility
                    best_row = move[0]
                    best_coloumn = move[1]
            else:   """ Rules for PRUNING """
                if utility < beta:
                    beta = utility
                    best_row = move[0]
                    best_coloumn = move[1]
            board[move[0]][move[1]] = '-'

            if alpha > beta: """ Rules for PRUNING """
                break;

        if node_type_maxnode:
            return (alpha, best_row, best_coloumn)
        else
            return (beta, best_row, best_coloumn)

    def move(self, board, block, old_move, player_flag):
        """
        :param board: is the list of lists that represents the 9x9 grid
        :param block: is a list that represents if a block is won or available to play in
        :param old_move: is a tuple of integers representing co-ordintates of the last move made
        :param flag: is player marker. it can be 'x' or 'o'.
        board[i] can be 'x' or 'o'. block[i] can be 'x' or 'o'
        Chooses a move based on minimax and alphabeta-pruning algorithm and returns it
        :rtype tuple: the co-ordinates in 9X9 board
        """
        self.isp = 0
        if old_move == (-1, -1):
            return (4, 4)
        startt = time.clock()
        if player_flag == 'o':
            flag2 = 'x'
        else:
            flag2 = 'o'
        self.num += 1
        max_ply = 5
        self.cntp = block.count(player_flag)
        self.cnto = block.count(flag2)
        if self.cnto - self.cntp > 1 or self.num > 25 or self.cntp == 2:
            self.ply = max_ply
        temp_board = copy.deepcopy(board)
        temp_block = copy.deepcopy(block)
        next_move = self.minimax(temp_board, temp_block, old_move, True, player_flag, flag2, 0, -100000.0, 100000.0, -1,
                                 -1)
        elapsed = (time.clock() - startt)
        # print "Finally :", next_move, "Took:", elapsed
        return (next_move[1], next_move[2])


    def get_utility(self, board, block, playerFlag, opFlag):
    """
    Function to find and return utility of a block 
    :param board: is the list of lists that represents the 9x9 grid
    :param block: is a list that represents if a block is won or available to play in
    :param playerFlag: player marker
    :param opFlag: Opponent Marker
    """

        utility_values_block = [0 for i in range(16)]
        for i in range(16):
            utility_values_block[i] = self.calc_utility(board, i, playerFlag)
        gain = 0
        lim = 100.0
        for i in range(16):
            utility_values_block[i] /= lim
        for i in range(4):
            p = 0
            positive = 0
            negative = 0
            for j in range(4):
                p += utility_values_block[j * 4 + i]
                if block[j * 4 + i] == playerFlag:
                    positive += 1
                elif block[j * 4 + i] == opFlag:
                    negative += 1
            gain = self.get_factor(p, gain)
            gain = self.get_new(positive, negative, gain)
        for j in range(4):
            p = 0
            positive = 0
            negative = 0
            for i in range(4):
                p += utility_values_block[j * 3 + i]
                if block[j * 4 + i] == playerFlag:
                    positive += 1
                elif block[j * 4 + i] == opFlag:
                    negative += 1
            gain = self.get_factor(p, gain)
            gain = self.get_new(positive, negative, gain)

        p = 0
        positive = 0
        negative = 0
        for i in range(4):
            p += utility_values_block[4 * i + i]
            if block[i * 4 + i] == playerFlag:
                positive += 1
            elif block[i * 4 + i] == opFlag:
                negative += 1
        gain = self.get_factor(p, gain)
        gain = self.get_new(positive, negative, gain)

        p = 0
        positive = 0
        negative = 0
        for i in range(1, 4):
            p += utility_values_block[2 * i]
            if block[i * 2] == playerFlag:
                positive += 1
            elif block[i * 2] == opFlag:
                negative += 1
        gain = self.get_new(positive, negative, gain)
        gain = self.get_factor(p, gain)

        if self.cntp < 2:
            if block[4] == playerFlag:
                gain += 10
            elif block[4] != '-':
                gain -= 10
        cnt1 = block.count(playerFlag)
        cnt2 = block.count(opFlag)
        if self.cntp < cnt1 and cnt2 == self.cnto:
            gain += 50
        elif cnt1 > self.cntp and (cnt1 - self.cntp) < (cnt2 - self.cnto):
            gain -= 20
        elif cnt1 < self.cntp and cnt2 > self.cnto:
            gain -= 50
        return gain


    def calc_utility(self, board, boardno, playerFlag):

        gain = 0
        startx = boardno / 4
        starty = boardno % 4
        starty *= 4
        startx *= 4
        for i in range(startx, startx + 4):
            positive = 0
            negative = 0
            neutral = 0
            for j in range(starty, starty + 4):
                if board[i][j] == '-':
                    neutral += 1
                elif board[i][j] == playerFlag:
                    positive += 1
                else:
                    negative += 1
            gain = self.calc(positive, negative, gain)

        for j in range(starty, starty + 4):
            positive = 0
            negative = 0
            neutral = 0
            for i in range(startx, startx + 4):
                if board[i][j] == '-':
                    neutral += 1
                elif board[i][j] == playerFlag:
                    positive += 1
                else:                                   
                    negative += 1
            gain = self.calc(positive, negative, gain)
        positive = 0
        neutral = 0
        negative = 0
        for i in range(0, 4):
            if board[startx + i][starty + i] == playerFlag:
                positive += 1
            elif board[startx + i][starty + i] == '-':
                neutral += 1
            else:
                negative += 1
        gain = self.calc(positive, negative, gain)
        for i in range(0, 4):
            if board[startx + i][starty + 2 - i] == playerFlag:
                positive += 1
            elif board[startx + i][starty + 2 - i] == '-':
                neutral += 1
            else:
                negative += 1
        gain = self.calc(positive, negative, gain)
        return gain
    def calc(self, cx, co, gain):
        if cx == 4:
            gain += 1000
        if cx == 3:
            gain += 100
        if cx == 2:
            gain += 10
        if cx == 1:
            gain += 1

        if co == 4:
            gain -= 1000
        if co == 3:
            gain -= 100
        if co == 2:
            gain -= 10
        if co == 1:
            gain -= 1
        return gain

    def get_factor(self, p, gain):
        if p < 1 and p >= -1:
            gain += p
        if p >= 1 and p < 2:
            val = 1
            val += (p - 1) * 9
            gain += val
        if p >= 2 and p < 3:
            val = 10
            val += (p - 2) * 90
            gain += val
        if p >= 3 and p < 4:
            val = 100
            val += (p - 3) * 900
            gain += val
        if p >= 4:
            val = 1000
            val += (p - 4) * 9000
            gain += val

        if p >= -2 and p < -1:
            val = -1
            val -= (abs(p) - 1) * 9
            gain += val
        if p >= -3 and p < -2:
            val = -10
            val -= (abs(p) - 2) * 90
            gain += val
        if p < -3 and p >=-4:
            val = -100
            val -= (abs(p) - 3) * 900
            gain += val
        if p < -4:
            val = -1000
            val -= (abs(p) - 4) * 9000
            gain += val
        return gain

    def get_new(self, cx, co, gain):
        
        if cx == 4:
            gain += 10000
        if cx == 3:
            gain += 1000
        if cx == 2:
            gain += 100
        if cx == 1:
            gain += 10

        if co == 4:
            gain -= 10000    
        if co == 3:
            gain -= 1000
        if co == 2:
            gain -= 100
        if co == 1:
            gain -= 10

        return gain

