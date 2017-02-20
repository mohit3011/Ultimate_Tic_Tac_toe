


class Player6:
    # Player6 agent to play game.


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
        utility = get_utility()
        return (utility, best_row, best_coloumn)

    else:
        available_moves = give_available_moves()
        """
        NOT SURE ABOUT THIS
        if len(available_moves) == 0:       ##### No moves left at depth
            utility = get_utility()
            self.MaxDepth = max(depth, 3)
            return (utility, best_row, best_coloumn)
        """
        if depth == 0:     """ If at first level we have around 56 cells then decrease level by 1 """
            if len(moves) > 17:
                self.MaxDepth = min(MaxDepth, 3)

        for move in available_moves:  # assign player sign whose turn is this
            if node_type_maxnode:
                board[move[0]][move[1]] = player_sign
            else:
                board[move[0]][move[1]] = opponent_sign

            utility = MinMax() # agains call MinMax

            if node_type_maxnode: """ Rules for PRONING """
                if utility > alpha:
                    alpha = utility
                    best_row = move[0]
                    best_coloumn = move[1]
            else:   """ Rules for PRONING """
                if utility < beta:
                    beta = utility
                    best_row = move[0]
                    best_coloumn = move[1]
            board[move[0]][move[1]] = '-'

            if alpha > beta: """ Rules for PRONING """
                break;

        if node_type_maxnode:
            return (alpha, best_row, best_coloumn)
        else
            return (beta, best_row, best_coloumn)
