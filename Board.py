import pygame
import sys
import time
import string

# starts pygame, sets screen size, and renames it to Chess Board
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Chess Board')

# colors/block size that will be used
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
block_size = 50

# this dictionary is used to import the images
# https://greenchess.net/info.php?item=downloads
images_dict = {
    "BRook": '', "BKnight": '', "BBishop": '', "BQueen": '', "BKing": '', "BBishop": '', "BKnight": '', "BRook": '',
    "BPawn": '', "BPawn": '', "BPawn": '', "BPawn": '', "BPawn": '', "BPawn": '', "BPawn": '', "BPawn": '',
    "WPawn": '', "WPawn": '', "WPawn": '', "WPawn": '', "WPawn": '', "WPawn": '', "WPawn": '', "WPawn": '',
    "WRook": '', "WKnight": '', "WBishop": '', "WQueen": '', "WKing": '', "WBishop": '', "WKnight": '', "WRook": '',
    '': ''
}

# keeps track of pieces and their coordinates
pieces_dict = {
    (0, 0): 'BRook', (0, 50): 'BPawn', (0, 100): '', (0, 150): '', (0, 200): '', (0, 250): '', (0, 300): 'WPawn',
    (0, 350): 'WRook',
    (50, 0): 'BKnight', (50, 50): 'BPawn', (50, 100): '', (50, 150): '', (50, 200): '', (50, 250): '',
    (50, 300): 'WPawn', (50, 350): 'WKnight',
    (100, 0): 'BBishop', (100, 50): 'BPawn', (100, 100): '', (100, 150): '', (100, 200): '', (100, 250): '',
    (100, 300): 'WPawn', (100, 350): 'WBishop',
    (150, 0): 'BQueen', (150, 50): 'BPawn', (150, 100): '', (150, 150): '', (150, 200): '', (150, 250): '',
    (150, 300): 'WPawn', (150, 350): 'WQueen',
    (200, 0): 'BKing', (200, 50): 'BPawn', (200, 100): '', (200, 150): '', (200, 200): '', (200, 250): '',
    (200, 300): 'WPawn', (200, 350): 'WKing',
    (250, 0): 'BBishop', (250, 50): 'BPawn', (250, 100): '', (250, 150): '', (250, 200): '', (250, 250): '',
    (250, 300): 'WPawn', (250, 350): 'WBishop',
    (300, 0): 'BKnight', (300, 50): 'BPawn', (300, 100): '', (300, 150): '', (300, 200): '', (300, 250): '',
    (300, 300): 'WPawn', (300, 350): 'WKnight',
    (350, 0): 'BRook', (350, 50): 'BPawn', (350, 100): '', (350, 150): '', (350, 200): '', (350, 250): '',
    (350, 300): 'WPawn', (350, 350): 'WRook'
}

c_coord_dict = {
    0: 'a',
    50: 'b',
    100: 'c',
    150: 'd',
    200: 'e',
    250: 'f',
    300: 'g',
    350: 'h'
}
r_coord_dict = {0: 8,
                50: 7,
                100: 6,
                150: 5,
                200: 4,
                250: 3,
                300: 2,
                350: 1}
# sets up images, and board
def initialize_board():
    # name of the images
    image_names = ["WRook", "WKnight", "WBishop", "WQueen", "WKing", "WPawn", "BRook", "BKnight", "BBishop", "BQueen",
                   "BKing", "BPawn"]

    # Goes through each name, loads the image, scales it, then adds it to images_dict
    for i in image_names:
        image = pygame.image.load(f"C:\\Users\\ascn1\\Desktop\\Projects\\Chess\\chess images\\{i}.png").convert_alpha()
        image = pygame.transform.scale(image, (block_size, block_size))
        images_dict[i] = image

    # Creates the board using pygame.draw, first for loop creates a row, second creates the column
    for i in range(8):
        for j in range(8):
            color = green if (i + j) % 2 == 0 else red
            # chess_board_dict[(string.ascii_lowercase[row],col+1)] = 0

            pygame.draw.rect(screen, color, (j * block_size, i * block_size, block_size, block_size))


# draws the pieces using
def draw_pieces():

    for location in pieces_dict:

        if images_dict[pieces_dict[location]] == '':
            continue

        # image is acquired from images_dict as pieces_dict gives the name of it
        screen.blit(images_dict[pieces_dict[location]], location)


# moves pieces after correct input fc = first col, fr = first row
def update_pieces_dict(fc, fr, c, r):

    # gets name of piece that is being moved, sets that place = '', then puts the new name in the new spot
    piece_name = pieces_dict[(fc * block_size, fr * block_size)]
    pieces_dict[(fc * block_size, fr * block_size)] = ''

    # makes the captured piece disappear
    if pieces_dict[(c * block_size, r * block_size)] != '':
        box_color = green if (c + r) % 2 == 0 else red
        pygame.draw.rect(screen, box_color, (c * block_size, r * block_size, 50, 50))

    pieces_dict[(c * block_size, r * block_size)] = piece_name

    box_color = green if (fc + fr) % 2 == 0 else red

    # draws the box of the piece that was moved
    pygame.draw.rect(screen, box_color, (fc * block_size, fr * block_size, 50, 50))

    # draws the piece to the place it was moved
    screen.blit(images_dict[piece_name], (c*block_size, r * block_size))


def legal_moves(fc, fr, c, r):
    og_piece = pieces_dict[(fc * block_size, fr * block_size)]
    target_piece = [0]

    if len(pieces_dict[(c * block_size, r * block_size)]) > 0:
        target_piece = pieces_dict[(c * block_size, r * block_size)]

    # Makes it so if pieces try to attack the same color, fails
    if og_piece[0] == "W" and target_piece[0] == "W":
        return False
    if og_piece[0] == "B" and target_piece[0] == "B":
        return False

    # Move logic for white pawns - add en passant
    if og_piece == "WPawn":

        # checks when taking a piece, uses dict coordinate system
        if len(target_piece) > 2 and r_coord_dict[r * block_size] - r_coord_dict[fr * block_size] == 1:
            if abs(fc * block_size - c * block_size) == 50:
                return True

        # prevents the pawn from moving different columns
        if fc != c:
            return False

        # prevents from taking a piece when moving forward
        if len(target_piece) > 2 and fc == c:
            return False

        # allows double move if on correct row, uses dict coordinate system
        if r_coord_dict[fr * block_size] == 2 and r_coord_dict[r * block_size] - r_coord_dict[fr * block_size] <= 2 and len(pieces_dict[(fc * block_size, 250)]) < 2:
            return True

        if r_coord_dict[r * block_size] - r_coord_dict[fr * block_size] >= 2:
            return False

    # Move logic for black pawns - add en passant
    elif og_piece == "BPawn":
        if len(target_piece) > 2 and r_coord_dict[r * block_size] - r_coord_dict[fr * block_size] == -1:
            if abs(fc * block_size - c * block_size) == 50:
                return True

        # prevents the pawn from moving different columns
        if fc != c:
            return False

        # prevents from taking a piece when moving forward
        if len(target_piece) > 2 and fc == c:
            return False

        if r_coord_dict[fr * block_size] == 7 and r_coord_dict[r * block_size] - r_coord_dict[fr * block_size] >= -2 and len(pieces_dict[(fc * block_size, 100)]) < 2:
            return True

        if r_coord_dict[r * block_size] - r_coord_dict[fr * block_size] <= -2:
            return False

    elif og_piece == "WBishop" or og_piece == "BBishop":
        # Bishop moves diagonally, so the absolute difference between file and rank must be the same
        if abs(fc * block_size - c * block_size) != abs(fr * block_size - r * block_size):
            return False

        # Determine the direction of the movement
        file_direction = 1 if c > fc else -1
        rank_direction = 1 if r > fr else -1

        # Check all squares between the start and end positions to ensure there are no pieces in the way
        for step in range(1, abs(c - fc)):
            intermediate_file = fc + step * file_direction
            intermediate_rank = fr + step * rank_direction

            if len(pieces_dict[(intermediate_file * block_size, intermediate_rank * block_size)]) > 0:
                return False

        return True

    elif og_piece == "WKnight" or og_piece == "BKnight":

        # allows for 2 up, 1 over
        if abs(fr * block_size - r * block_size) == 100 and abs(fc * block_size - c * block_size) == 50:
            return True

        # allows for 2 over, 1 up
        if abs(fr * block_size - r * block_size) == 50 and abs(fc * block_size - c * block_size) == 100:
            return True

        return False

    elif og_piece == "WQueen" or og_piece == "BQueen":

        # diagonal
        if abs(fc * block_size - c * block_size) == abs(fr * block_size - r * block_size):

            file_direction = 1 if c > fc else -1
            rank_direction = 1 if r > fr else -1

            # Checks for pieces diagonally
            for step in range(1, abs(c - fc)):
                intermediate_file = fc + step * file_direction
                intermediate_rank = fr + step * rank_direction

                if len(pieces_dict[(intermediate_file * block_size, intermediate_rank * block_size)]) > 0:
                    return False

            return True

        # vertical
        if fc == c:

            if fr > r:
                for step in range(r+1, fr):
                    if len(pieces_dict[(c * block_size, step * block_size)]) > 0:
                        return False

            if fr < r:
                for step in range(fr+1, r):
                    if len(pieces_dict[(c * block_size, step * block_size)]) > 0:
                        return False

            return True

        # horizontal
        if fr == r:

            if c > fc:
                for step in range(fc+1, c):
                    if len(pieces_dict[(step * block_size, r * block_size)]) > 0:
                        return False

            if c < fc:
                for step in range(c+1, fc):
                    if len(pieces_dict[(step * block_size, r * block_size)]) > 0:
                        return False

            return True

        else:
            return False



    return True


def king_check(self, piece):
    pass


def move_notation(fc, fr, c, r):
    piece_name = pieces_dict[(fc * block_size, fr * block_size)]
    message = f"{piece_name} from {c_coord_dict[fc * block_size]}{r_coord_dict[fr * block_size]} to {c_coord_dict[c * block_size]}{r_coord_dict[r * block_size]}"
    return message


first_col = None
first_row = None
glow_col = None
glow_row = None

turn = 0
black_piece = None

initialize_board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # used to highlight and move pieces
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            col = event.pos[0] // 50
            row = event.pos[1] // 50

            # print(col, row)

            # Skips if a piece is not clicked on first move
            if pieces_dict[(col * block_size, row * block_size)] == '' and first_col is None:
                continue

            # This is to prevent an IndexError whenever finding black_piece
            if len(pieces_dict[(col * block_size, row * block_size)]) > 0:
                black_piece = pieces_dict[(col * block_size, row * block_size)][0]
                # Skips if first move is black on white's turn
                if black_piece == 'B' and first_row is None and turn % 2 == 0:
                    continue
                # Skips if first move is white on black's turn
                if black_piece == 'W' and first_row is None and turn % 2 == 1:
                    continue

            # Checks and then if approved, moves the pieces, and the turn sequence
            if first_col is not None:

                # prevents you from moving to the same spot
                if first_col == col and first_row == row:
                    continue

                if not king_check(1, black_piece):
                    print("Woah that's not valid")
                    continue
                
                if not legal_moves(first_col, first_row, col, row):
                    print("Woah that's not valid")
                    continue

                print(move_notation(first_col, first_row, col, row))
                update_pieces_dict(first_col, first_row, col, row)

                turn += 1
                if turn % 2 == 0:
                    print("Its white's turn")

                else:
                    print("Its black's turn")

                first_col = None
                first_row = None
                continue

            first_col = col
            first_row = row

            pygame.draw.rect(screen, yellow, (first_col * block_size, first_row * block_size, 50, 50), 5)
            glow_col = col
            glow_row = row

        # used to remove highlighted pieces
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

            # prevents game from crashing if right click is used first
            if glow_col is None:
                continue

            color = green if (glow_col + glow_row) % 2 == 0 else red

            # Turns highlighted area back to normal
            pygame.draw.rect(screen, color, (glow_col * block_size, glow_row * block_size, 50, 50), 5)
            first_col = None
            first_row = None

    draw_pieces()
    pygame.display.update()
