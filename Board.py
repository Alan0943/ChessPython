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


def legal_moves():
    pass


first_col = None
first_row = None
glow_col = None
glow_row = None

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

            print(col, row)

            # Skips if a piece is not clicked on first move
            if pieces_dict[(col * block_size, row * block_size)] == '' and first_col is None:
                continue

            if first_col is not None:
                update_pieces_dict(first_col, first_row, col, row)
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
