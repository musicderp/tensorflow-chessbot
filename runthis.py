import time
import random
import tensorflow_chessbot
from stockfish import Stockfish
import cv2
import numpy as np
import pyautogui as pg
import chess

# EDIT THIS WITH YOUR OWN VALUES
BOARD_SIZE = 2402-1336
CELL_SIZE = int(BOARD_SIZE / 8)
BOARD_TOP_COORD = 146
BOARD_LEFT_COORD = 1336

stockfish = Stockfish(path='Stockfish/stockfish_15_x64_avx2.exe', parameters={"Threads": 8, "Hash": 10000, "Ponder": True, "Contempt": 20, "Minimum Thinking Time": 50})
print(stockfish.get_parameters())

x = BOARD_LEFT_COORD
y = BOARD_TOP_COORD
square_to_coords = [];
# loop over board rows
for row in range(8):
    # loop over board columns
    for col in range(8):
        # init square
        square = row * 8 + col

        # associate square with square center coordinates
        square_to_coords.append((int(x + CELL_SIZE / 2), int(y + CELL_SIZE / 2)))

        # increment x coord by cell size
        x += CELL_SIZE

    # restore x coord, increment y coordinate by cell size
    x = BOARD_LEFT_COORD
    y += CELL_SIZE

prev_pos = ""
global move_counter
move_counter = 0


def find_best_move(color, prev_pos):
    global move_counter
    get_square = [
        'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
        'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
        'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
        'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
        'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
        'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
        'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
        'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
    ]
    screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)
    crop_img = screenshot[BOARD_TOP_COORD:BOARD_TOP_COORD + BOARD_SIZE, BOARD_LEFT_COORD:BOARD_LEFT_COORD + BOARD_SIZE]
    cv2.imwrite('crap/img.png', crop_img)

    position = tensorflow_chessbot.image_to_fen('crap/img.png', color)
    board = chess.Board(position[0])
    print(position[1])
    if position[1] < 99.9 or board.is_valid() != True:
        find_best_move(color, prev_pos)

    gayqueers = position[0].split(" ")
    yeeters = gayqueers[0]
    print(yeeters, " yo yo ", prev_pos)
    if prev_pos != yeeters:
        print("analyzing position")
        stockfish.set_fen_position(position[0])

        if move_counter <= 8:
            best_move = stockfish.get_best_move()
        else:
            yomama = random.randint(0, 10000)
            best_move = stockfish.get_best_move_time(yomama)
        print(best_move)
        screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)
        crop_img = screenshot[BOARD_TOP_COORD:BOARD_TOP_COORD + BOARD_SIZE,
                   BOARD_LEFT_COORD:BOARD_LEFT_COORD + BOARD_SIZE]
        cv2.imwrite('crap/img.png', crop_img)

        position_check = tensorflow_chessbot.image_to_fen('crap/img.png', color)
        if position == position_check:
            stockfish.make_moves_from_current_position([best_move])
            temp = stockfish.get_fen_position().split(" ")
            prev_pos = temp[0]
            print(prev_pos)
            if color == "b":
                get_square.reverse()
            from_sq = square_to_coords[get_square.index(best_move[0] + best_move[1])]
            to_sq = square_to_coords[get_square.index(best_move[2] + best_move[3])]

            # make move on board
            pg.moveTo(from_sq)
            pg.click()
            pg.moveTo(to_sq)
            pg.click()
        else:
            print("position mismatch, trying again")
            find_best_move(color, prev_pos)
        move_counter += 1
    else:
        temp = position[0].split(" ")
        prev_pos = temp[0]
        print("position is same")

    # wait for 3 seconds
    # time.sleep(.4)
    find_best_move(color, prev_pos)


find_best_move("w", prev_pos)
