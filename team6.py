import random
import sys
import copy
import time

class Player6():
    # Player6 agent to play game.
    def __init__(self):
        self.MaxDepth = 4
        #self.block = ['-' for i in range(16)]
        self.num = 0
        self.cntp = 0 # how many blocks won by player
        self.cnto = 0 # how many blocks won by opponent
        self.var = 1
        pass
        #Rest of the variables will be defined

    # Function implementing minmax algorithm with alph-beta pruning.
    def MinMax(self, board, old_move, node_type_maxnode, player_sign, opponent_sign, depth, alpha, beta, best_row, best_coloumn):
        """
        board :- 16*16 matrix representing game board
        status_blocks :- bool flags list for all block give their status_blocks
        old_move :- list[2] contain x,y
        node_type_maxnode :- bool if 1 reffers to maxnode and 0 to minnode
        player_sign :- represent x or o of player
        opponent_sign :- represent x or o of opponent
        depth :- int represent current depth
        """
        #print "depth-->", depth
        if depth == self.MaxDepth:
            utility = self.get_utility(board, player_sign, opponent_sign)
            #print " Returning utility", utility, best_row, best_coloumn
            return (utility, best_row, best_coloumn)

        else:
            available_moves = board.find_valid_move_cells(old_move)
            #print "available moves-->",available_moves

            #NOT SURE ABOUT THIS
            if len(available_moves) == 0:       ##### No moves left at depth
                utility = self.get_utility(board, player_sign, opponent_sign)
                self.MaxDepth = max(depth, 2)
                return (utility, best_row, best_coloumn)
            #print "Minmax ke andar"

            if depth == 0:      #If at first level we have around 56 cells then decrease level by 1 """
                #print "depth and moves available is :", depth , len(available_moves)
                if len(available_moves) > 17:
                    self.MaxDepth = min(MaxDepth, 2)

            for move in available_moves:  # assign player sign whose turn is this
                #print "move--->",move
                temp_board = board
                """
                if node_type_maxnode:
                    board.board_status[move[0]][move[1]] = player_sign
                else:
                    board.board_status[move[0]][move[1]] = opponent_sign
                """
                sign = player_sign
                if not node_type_maxnode:   sign = opponent_sign

                board.update(old_move, move, sign)

                if node_type_maxnode==True:
                    node_type_maxnode1 = False
                else:
                    node_type_maxnode1 = True

                utility = self.MinMax(board, move, node_type_maxnode1, player_sign, opponent_sign, depth+1 , alpha, beta, best_row, best_coloumn) # agains call MinMax

                #print node_type_maxnode
                if node_type_maxnode:  #Rules for PRUNING
                    #print "Minmax ke deep andar"
                    if utility[0] > alpha:
                        alpha = utility[0]
                        best_row = move[0]
                        best_coloumn = move[1]
                        #print "Minmax ke deep andar if"
                else:  # Rules for PRUNING """
                    if utility[0] < beta:
                        beta = utility[0]
                        best_row = move[0]
                        best_coloumn = move[1]
                        #print "Minmax ke deep andar else"

                #print "Board check passed!!!!!"
                board.board_status[move[0]][move[1]] = '-'
                #print "Board check passed!!!!!"

                if alpha > beta: # Rules for PRUNING """
                    break;
            #print alpha , beta
            if node_type_maxnode:
                return (alpha, best_row, best_coloumn)
            else:
                return (beta, best_row, best_coloumn)

    def move(self, board, old_move, player_flag):
        """
        :param board: is the list of lists that represents the 9x9 grid
        :param block: is a list that represents if a block is won or available to play in
        :param old_move: is a tuple of integers representing co-ordintates of the last move made
        :param flag: is player marker. it can be 'x' or 'o'.
        board[i] can be 'x' or 'o'. block[i] can be 'x' or 'o'
        Chooses a move based on minimax and alphabeta-pruning algorithm and returns it
        :rtype tuple: the co-ordinates in 9X9 board
        """
        #print "Move me ayaaa ayaa ayaa"
        self.isp = 0
        if old_move == (-1, -1):
            return (4, 4)
        startt = time.clock()
        if player_flag == 'o':
            flag2 = 'x'
        else:
            flag2 = 'o'
        self.num += 1
        max_MaxDepth = 4
        self.cntp = sum(blocks.count(player_flag) for blocks in board.block_status)
        self.cnto = sum(blocks.count(flag2) for blocks in board.block_status)
        #if self.cnto - self.cntp > 1 or self.num > 25 or self.cntp == 2:
            #self.MaxDepth = max_MaxDepth
        #print "yaha pe ayaaaa"
        temp_board = copy.deepcopy(board)
        #print "bich me ayaayaya"
        #temp_block = copy.deepcopy(board.block_status)
        #print "minmax me ayaaaaa!"
        next_move = self.MinMax(temp_board, old_move, True, player_flag, flag2, 0, -1000000.0, 1000000.0, -1,
                                 -1)
        #print "minmax se bahar ayayayyayayay\n\n"
        elapsed = (time.clock() - startt)
        # #print "Finally :", next_move, "Took:", elapsed
        ##print " Lets see kaha huga   " ,next_move[0], "      ", next_move[1] , "\n\n\n\n\n\n\n"
        #print "#printing next move: " , next_move[1] , next_move[2]
        return (next_move[1], next_move[2])


    def get_utility(self, board, playerFlag, opFlag):
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
        lim = 1000.0
        for i in range(16):
            utility_values_block[i] /= lim
        for i in range(4):
            p = 0
            positive = 0
            negative = 0
            for j in range(4):
                p += utility_values_block[j * 4 + i]
                if board.block_status[j][i] == playerFlag:
                    positive += 1
                elif board.block_status[j][i] == opFlag:
                    negative += 1
            gain = self.get_factor(p, gain)
            gain = self.get_new(positive, negative, gain)
        for j in range(4):
            p = 0
            positive = 0
            negative = 0
            for i in range(4):
                p += utility_values_block[j * 3 + i]
                if board.block_status[j][i] == playerFlag:
                    positive += 1
                elif board.block_status[j][i] == opFlag:
                    negative += 1
            #print "\n\n\nFound utility at cell level." , self.var
            self.var+=1;
            gain = self.get_factor(p, gain)
            gain = self.get_new(positive, negative, gain)

        p = 0
        positive = 0
        negative = 0
        for i in range(4):
            p += utility_values_block[4 * i + i]
            if board.block_status[i][i] == playerFlag:
                positive += 1
            elif board.block_status[i][i] == opFlag:
                negative += 1

        gain = self.get_factor(p, gain)
        gain = self.get_new(positive, negative, gain)

        p = 0
        positive = 0
        negative = 0
        for i in range(4):
            p += utility_values_block[(4 * i) + 3 -i]
            if board.block_status[i][3-i] == playerFlag:
                positive += 1
            elif board.block_status[i][3-i] == opFlag:
                negative += 1

        gain = self.get_new(positive, negative, gain)
        gain = self.get_factor(p, gain)
        """
        if self.cntp < 2:
            if self.block[4] == playerFlag:
                gain += 10
            elif self.block[4] != '-':
                gain -= 10
        """
        #print " calc for all calculated!!!! " , board.block_status, sum(blocks.count(playerFlag) for blocks in board.block_status)
        cnt1 = sum(blocks.count(playerFlag) for blocks in board.block_status)
        cnt2 = sum(blocks.count(opFlag) for blocks in board.block_status)
        if self.cntp < cnt1 and cnt2 == self.cnto:
            gain += 50
        elif cnt1 > self.cntp and (cnt1 - self.cntp) < (cnt2 - self.cnto):
            gain -= 20
        elif cnt1 < self.cntp and cnt2 > self.cnto:
            gain -= 50
        #print "Gain Returned by Get utility is: ", gain
        return gain


    def calc_utility(self, board, boardno, playerFlag):

        gain = 0
        startx = boardno / 4
        starty = boardno % 4
        starty *= 4
        startx *= 4
        #print "Starting x",startx,"Starting y",starty
        for i in range(startx, startx + 4):
            positive = 0
            negative = 0
            neutral = 0
            for j in range(starty, starty + 4):
                if board.board_status[i][j] == '-':
                    neutral += 1
                elif board.board_status[i][j] == playerFlag:
                    positive += 1
                else:
                    negative += 1
            gain = self.calc(positive, negative, gain)

        for j in range(starty, starty + 4):
            positive = 0
            negative = 0
            neutral = 0
            for i in range(startx, startx + 4):
                if board.board_status[i][j] == '-':
                    neutral += 1
                elif board.board_status[i][j] == playerFlag:
                    positive += 1
                else:
                    negative += 1
            gain = self.calc(positive, negative, gain)
        positive = 0
        neutral = 0
        negative = 0
        for i in range(0, 4):
            if board.board_status[startx + i][starty + i] == playerFlag:
                positive += 1
            elif board.board_status[startx + i][starty + i] == '-':
                neutral += 1
            else:
                negative += 1
        gain = self.calc(positive, negative, gain)
        for i in range(0, 4):
            if board.board_status[startx + i][starty + 2 - i] == playerFlag:
                positive += 1
            elif board.board_status[startx + i][starty + 2 - i] == '-':
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
        #print "Gain Returned by Get Factor is: ", gain
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
        #print "Gain Returned by Get New is: ", gain
        return gain
