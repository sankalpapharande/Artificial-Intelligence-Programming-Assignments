#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import json
import sys
import time
ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def next_empty_position(board, empty_position):
    for key in board.keys():
        if board[key] == 0:
            empty_position.append(str(key)[0])
            empty_position.append(str(key)[1])
            return True
    return False


def is_correct_row_assignment(board, row, assignment):
    row_positions = []
    for i in range(1, 10):
        row_positions.append(row + str(i))
    for key in row_positions:
        if board[key] == assignment:
            return False
    return True


def is_correct_column_assignment(board, column, assignment):
    column_positions = []
    for i in list(ROW):
        column_positions.append(str(i) + str(column))
    for key in column_positions:
        if board[key] == assignment:
            return False
    return True


def is_correct_box_assignment(board, row, column, assignment):
    column = int(column) - 1
    top_right_corner = int(column) - (int(column) % 3)
    columns_to_check = [top_right_corner + 1, top_right_corner + 2, top_right_corner + 3]

    starting_row_index = list(ROW).index(row)
    starting_row_index = starting_row_index - starting_row_index % 3
    rows_to_check = [list(ROW)[starting_row_index], list(ROW)[starting_row_index + 1],
                     list(ROW)[starting_row_index + 2]]

    for r in rows_to_check:
        for c in columns_to_check:
            if board[r + str(c)] == assignment:
                return False
    return True


def is_assigned_value_correct(board, empty_position, assignment):
    if is_correct_row_assignment(board, empty_position[0], assignment) and \
            is_correct_column_assignment(board, empty_position[1], assignment) and \
            is_correct_box_assignment(board, empty_position[0], empty_position[1], assignment):
        return True
    else:
        return False


def backtracking(board):
    """Takes a board and returns solved board."""
    empty_position = []
    is_empty_position = next_empty_position(board, empty_position)
    if is_empty_position is False:
        return True
    else:
        current_empty_position = empty_position
    # print("current_empty_position is:{}".format(current_empty_position))

    for i in range(1, 10):
        if is_assigned_value_correct(board, empty_position, i):
            board["".join(empty_position)] = i

            if backtracking(board):
                solved_board = board
                return solved_board

            board["".join(empty_position)] = 0
    return False



if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}
        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        board_no = 1
        solved_boards = 0
        time_statistics_name = 'time_statistics.txt'
        time_statistics_file = open(time_statistics_name, "w")

        solved_board_numbers = 'solved_board_numbers.txt'
        solved_board_numbers_file = open(solved_board_numbers, "w")
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            print("Solving board no:{}".format(board_no))
            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            # print_board(board)

            # Solve with backtracking
            start_time = time.time()
            solved_board = backtracking(board)
            time_taken = time.time() - start_time
            string_to_write = json.dumps({board_no: time_taken})
            time_statistics_file.write(string_to_write)
            time_statistics_file.write('\n')
            if solved_boards is not False:
                solved_boards =  solved_boards + 1
                solved_board_numbers_file.write("Board No:{}".format(board_no))
                solved_board_numbers_file.write('\n')
            # Print solved board. TODO: Comment this out when timing runs.
            # print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
            board_no = board_no + 1
        print("Finishing all boards in file.")
