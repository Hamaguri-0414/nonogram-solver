import copy
import numpy as np


class IllustLogic:

    def __init__(self, size, sample=False):
        self.size = size
        self.board = np.full([size, size], 'w')
        self.str_w = '.'
        self.str_c = '-'
        self.str_b = 'o'

        if sample:
            self.hint_row = [[1], [1], [5], [1], [1]]
            self.hint_col = [[1], [3], [1, 1, 1], [1], [1]]
        else:
            print('Input row numbers (split with spaces):')
            self.hint_row = self.input_hint()
            print('Input column numbers (split with spaces):')
            self.hint_col = self.input_hint()

    def input_hint(self):
        ans = list()
        for i in range(self.size):
            hint_i = list(map(int, input().split()))
            sum_i = sum(hint_i) + len(hint_i) - 1
            if sum_i > self.size:
                raise Exception('Input numbers are too large.')
            ans.append(hint_i)
        return ans

    def convert_board_to_str(self):
        board_str = copy.copy(self.board)
        np.place(board_str, board_str == 'w', self.str_w)
        np.place(board_str, board_str == 'c', self.str_c)
        np.place(board_str, board_str == 'b', self.str_b)
        ans = ''
        ans += '+' + '-' * (self.size * 2) + '\n'
        for i in range(self.size):
            ans += '| ' + ' '.join(board_str[i, :]) + '\n'
        return ans

    def convert_hint_to_str(self, hint):
        ans = '\n'.join([' '.join(map(str, h)) for h in hint])
        return ans

    def __str__(self):
        ans = 'Board:\n'
        ans += self.convert_board_to_str()
        ans += '\n\nRow hints:\n'
        ans += self.convert_hint_to_str(self.hint_row)
        ans += '\n\nColumn hints:\n'
        ans += self.convert_hint_to_str(self.hint_col)
        return ans

    def combn_cell_pattern(self, n_cell, n_gap):
        if n_cell == 0:
            return [[0] * n_gap]
        if n_gap == 1:
            return [[n_cell]]
        ans = []
        for n_cell_next in range(n_cell + 1):
            prev_ans = self.combn_cell_pattern(n_cell_next, n_gap - 1)
            ans += [[n_cell - n_cell_next] + ans_i for ans_i in prev_ans]
        return ans

    def combn_cross_cell(self, hint):
        n_cell = self.size - sum(hint) - len(hint) + 1
        n_gap = len(hint) + 1
        return self.combn_cell_pattern(n_cell, n_gap)

    def create_all_pattern(self, hint):
        n_cross = self.combn_cross_cell(hint)
        ans = []
        for i in range(len(n_cross)):
            ans_i = []
            for j in range(len(n_cross[i]) - 1):
                if j > 0:
                    ans_i += ['c']
                ans_i += ['c'] * n_cross[i][j]
                ans_i += ['b'] * hint[j]
            ans_i += ['c'] * n_cross[i][-1]
            ans.append(ans_i)
        return ans

    def compare_pattern(self, board, pattern):
        pattern0 = ['w' if b == 'w' else p for b, p in zip(board, pattern)]
        return board == pattern0

    def find_intersect(self, pattern):
        fixed_pat = ['w'] * self.size
        for i in range(self.size):
            pat_i = [p[i] for p in pattern]
            uniq_pat_i = list(set(pat_i))
            if len(uniq_pat_i) == 1:
                fixed_pat[i] = uniq_pat_i[0]
        return fixed_pat

    def solve(self, does_print=True):
        print('Creating all patterns...')
        all_row_pattern = [self.create_all_pattern(h) for h in self.hint_row]
        all_col_pattern = [self.create_all_pattern(h) for h in self.hint_col]

        print('Drawing board...')
        n_iter = 0
        while True:
            n_iter += 1
            board_prev = copy.copy(self.board)

            # find fixed cells
            all_row_fixed = [self.find_intersect(p) for p in all_row_pattern]
            all_col_fixed = [self.find_intersect(p) for p in all_col_pattern]
            board_fixed_row = np.array(all_row_fixed)
            board_fixed_col = np.array(all_col_fixed).transpose()

            # draw fixed cells
            new_board = copy.copy(board_fixed_row)
            new_board[new_board == 'w'] = board_fixed_col[new_board == 'w']
            self.board = copy.copy(new_board)

            # finish
            if np.array_equal(self.board, board_prev):
                print('Finished!')
                return

            # print process
            if does_print:
                print(f'iter={n_iter}')
                print(self.convert_board_to_str())

            # remove patterns which do not match with present board
            for i in range(self.size):
                all_row_pattern[i] = [
                    p for p in all_row_pattern[i]
                    if self.compare_pattern(board=list(self.board[i, :]), pattern=p)]
                all_col_pattern[i] = [
                    p for p in all_col_pattern[i]
                    if self.compare_pattern(board=list(self.board[:, i]), pattern=p)]


if __name__ == '__main__':
    size = 30
    ill = IllustLogic(size)
    ill.solve()
