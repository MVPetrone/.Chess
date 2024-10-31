from tkinter import *
from PIL import Image, ImageTk
import time
import random

from PIL.Image import Dither

root = Tk()
root.geometry("{}x{}".format(600,660))


class Main:
    def __init__(self):
        self.images = {}
        self.load_images()
        self.boards = []
        self.boards.append(Board(main=self))
        for x in range(len(self.boards)):
            self.boards[x].create_tiles()
        root.bind("<ButtonPress-1>", self.pressing_mouse)
        root.bind("<ButtonRelease-1>", self.releasing_mouse)

    def main(self):
        start_main = time.time()
        while True:
            if time.time() - start_main > 0.01:
                # desired execution
                self.update()
            # undesired execution

    def pressing_mouse(self, event):
        self.mouse_down = True

    def releasing_mouse(self, event):
        self.mouse_down = False

    def load_images(self):
        self.images["empty"] = ImageTk.PhotoImage(Image.open("./resources/images/empty.png").resize((60, 60), Dither.NONE).convert("RGBA"))

        self.images["w_pawn"] = ImageTk.PhotoImage(Image.open("./resources/images/w_pawn.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["w_knight"] = ImageTk.PhotoImage(Image.open("./resources/images/w_knight.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["w_bishop"] = ImageTk.PhotoImage(Image.open("./resources/images/w_bishop.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["w_rook"] = ImageTk.PhotoImage(Image.open("./resources/images/w_rook.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["w_queen"] = ImageTk.PhotoImage(Image.open("./resources/images/w_queen.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["w_king"] = ImageTk.PhotoImage(Image.open("./resources/images/w_king.png").resize((50, 50), Dither.NONE).convert("RGBA"))

        self.images["b_pawn"] = ImageTk.PhotoImage(Image.open("./resources/images/b_pawn.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["b_knight"] = ImageTk.PhotoImage(Image.open("./resources/images/b_knight.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["b_bishop"] = ImageTk.PhotoImage(Image.open("./resources/images/b_bishop.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["b_rook"] = ImageTk.PhotoImage(Image.open("./resources/images/b_rook.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["b_queen"] = ImageTk.PhotoImage(Image.open("./resources/images/b_queen.png").resize((50, 50), Dither.NONE).convert("RGBA"))
        self.images["b_king"] = ImageTk.PhotoImage(Image.open("./resources/images/b_king.png").resize((50, 50), Dither.NONE).convert("RGBA"))

        self.images["selected"] = ImageTk.PhotoImage(Image.open("./resources/images/selected.png").resize((64, 64), Dither.NONE).convert("RGBA"))
        self.images["option"] = ImageTk.PhotoImage(Image.open("./resources/images/option.png").resize((30, 30), Dither.NONE).convert("RGBA"))

    def restart_all_boards(self):
        for x in range(len(self.boards)):
            self.boards[x].restart()

    def update_all_boards(self):
        for x in range(len(self.boards)):
            self.boards[x].update()
            self.boards[x].update_all_tiles()

    def update(self):
        self.update_all_boards()
        root.update()


class Board:
    alphabet = "abcdefgh"

    def __init__(self, main):
        self.main = main
        self.tiles_array = []
        self.tiles_selected = []
        self.tiles_optioned = []

        # Frame
        self.frame = Frame(root, bd=4, bg="grey")
        self.frame.place(x=5, y=5)
        # Board as a frame
        self.board_frame = Frame(self.frame, bd=4, bg="grey30")
        self.board_frame.pack()
        # Board as a canvas
        self.board_canvas = Canvas(self.board_frame)
        self.board_canvas.pack()
        # Save Button
        self.save_button = Button(self.frame, command=lambda: self.save_to_file(), text="SAVE")
        self.save_button.pack()
        # Restart Button
        self.restart_button = Button(self.frame, command=lambda: self.restart(), text="RESTART")
        self.restart_button.pack()
        # Clear Button
        self.clear_button = Button(self.frame, command=lambda: self.clear(), text="CLEAR")
        self.clear_button.pack()
        # Update Button
        self.update_button = Button(self.frame, command=lambda: self.update_all_tiles(), text="UPDATE")
        self.update_button.pack()

    def create_tiles(self):
        counter = 0
        alt = True
        for y, alphabet in zip(range(8), Board.alphabet):
            alt = False if alt else True
            for x, numbers in zip(range(8), range(1, 9)):
                alt = True if not alt else False
                c = "coral2" if alt else "ivory"
                self.tiles_array.append(Tile(_id=counter, colour=c, board=self, pos=(x, y), state="00"))
                self.tiles_array[counter].spawn(row=y, column=x)
                counter += 1

    def clear(self):
        self.load_from_file(custom=False, name="empty")

    def swap_tile_pieces(self, tile1, tile2):
        temp = tile1.state
        tile1.set_state(tile2.state)
        tile2.set_state(temp)

    def restart(self):
        self.load_from_file(custom=False, name="default")

    def load_from_file(self, custom=False, name=None):
        if custom:
            filename = f"./resources/saves/custom/{name}.txt"
        else:
            filename = f"./resources/saves/{name}.txt"
        file = open(filename, "r")
        layout = file.read()
        layout = layout.split("\n")
        e = []
        for x in range(len(layout)):
            e.append(layout[x].split(" "))
        a = []
        for x in range(8):
            for y in range(8):
                a.append(e[x][y])
        file.close()
        self.set_all_tiles(a)

    def save_to_file(self):
        # open count file
        c_file = open("./resources/saves/count.txt", "r")
        count = int(c_file.read().strip("\n").strip(""))
        c_file.close()

        # format layout
        layout = []
        c = 0
        for y in range(8):
            row = []
            for x in range(8):
                row.append(self.tiles_array[c].state)
                c += 1
            layout.append(row)
        for x in range(len(layout)):
            layout[x] = " ".join(layout[x])
        layout = "\n".join(layout)

        file = open(f"./resources/saves/custom/{count+1}.txt", "w")
        file.write(layout)
        file.close()

        c_file = open("./resources/saves/count.txt", "w")
        c_file.write(str(count+1))
        c_file.close()

    def select_all_tiles(self):
        pass

    def deselect_all_tiles(self):
        for tile in self.tiles_selected:
            tile.deselect()

    def set_all_tiles(self, states):
        for i in range(len(self.tiles_array)):
            self.tiles_array[i].set_state(states[i])
        self.update_all_tiles()

    def remove_all_optioned_tiles(self):
        while len(self.tiles_optioned) > 0:
            self.tiles_optioned[0].remove_option()

    def update_all_tiles(self):
        for tile in self.tiles_array:
            tile.update()

    def update(self):
        pass


class Tile:
    states_dict = {"00": "empty",
                   "01": "w_pawn", "02": "w_knight", "03": "w_bishop", "04": "w_rook", "05": "w_queen", "06": "w_king",
                   "11": "b_pawn", "12": "b_knight", "13": "b_bishop", "14": "b_rook", "15": "b_queen", "16": "b_king"}

    def __init__(self, _id, colour, board, pos, state="00"):
        self.board = board
        self.id = _id
        self.colour = colour
        self.state = state
        self.pos = pos
        self.selected = False
        self.option = False
        self.image = self.board.main.images[Tile.states_dict[self.state]]

        self.frame = Frame(self.board.board_canvas, bd=2, bg="black", width=64, height=64)
        self.frame.place(x=0, y=0)
        self.canvas = Canvas(self.frame, highlightthickness=0, bg=self.colour, bd=0)
        self.canvas.place(x=0, y=0)
        self.canvas_piece_img = self.canvas.create_image(6, 6, anchor="nw", image=self.image)
        #self.canvas_text = self.canvas.create_text(0, 0, anchor="nw", text=self.pos)
        self.canvas_selected_img = self.canvas.create_image(-1, -1, anchor="nw")
        self.canvas_option_img = self.canvas.create_image(16, 16, anchor="nw")
        self.canvas.bind("<Button-1>", self.clicked)

    def print_selected(self):
        print(self.selected)

    def set_state(self, state):
        self.state = state

    def spawn(self, row, column):
        self.frame.grid(row=row, column=column)

    def clicked(self, event):
        if not self.option:
            if self.state != "00":
                if not self.selected:
                    self.board.deselect_all_tiles()
                    self.select()
                else:
                    self.deselect()
            else:
                self.board.deselect_all_tiles()
        else:
            self.board.swap_tile_pieces(self.board.tiles_selected[0], self)
            self.board.deselect_all_tiles()

    def select(self):
        self.selected = True
        self.board.tiles_selected.append(self)
        self.canvas.itemconfig(self.canvas_selected_img, image=self.board.main.images["selected"])
        self.find_options()
        self.update()

    def deselect(self):
        self.selected = False
        self.board.tiles_selected.remove(self)
        self.canvas.itemconfig(self.canvas_selected_img, image=self.board.main.images["empty"])
        self.board.remove_all_optioned_tiles()
        self.update()

    def find_options(self):
        if self.state == "01":  # white pawn
            poses = [(self.pos[0], self.pos[1]-1), (self.pos[0], self.pos[1]-2)]
        elif self.state == "11":  # black pawn
            poses = [(self.pos[0], self.pos[1]+1), (self.pos[0], self.pos[1]+2)]

        elif self.state == "02" or self.state == "12":  # knight
            poses = [(self.pos[0]-1, self.pos[1]-2), (self.pos[0]+1, self.pos[1]-2),
                     (self.pos[0]+2, self.pos[1]-1), (self.pos[0]+2, self.pos[1]+1),
                     (self.pos[0]+1, self.pos[1]+2), (self.pos[0]-1, self.pos[1]+2),
                     (self.pos[0]-2, self.pos[1]+1), (self.pos[0]-2, self.pos[1]-1)]

        elif self.state == "03" or self.state == "13":  # bishop
            poses = []
            for x in range(-8, 8):
                pos = (self.pos[0]+x, self.pos[1]+x)
                poses.append(pos)
            for x in range(-8, 8):
                pos = (self.pos[0]-x, self.pos[1]+x)
                poses.append(pos)

        elif self.state == "04" or self.state == "14":  # rook
            poses = []
            for x in range(-8, 8):
                poses.append((self.pos[0]+x, self.pos[1]))
            for x in range(-8, 8):
                poses.append((self.pos[0], self.pos[1]+x))

        elif self.state == "05" or self.state == "15":  # queen
            poses = []
            for x in range(-8, 8):
                poses.append((self.pos[0] + x, self.pos[1]))
            for x in range(-8, 8):
                poses.append((self.pos[0], self.pos[1] + x))
            for x in range(-8, 8):
                poses.append((self.pos[0]+x, self.pos[1]+x))
            for x in range(-8, 8):
                poses.append((self.pos[0]-x, self.pos[1]+x))
        elif self.state == "06" or self.state == "16":  # king
            poses = []
            for x in range(-1, 2):
                for y in range(-1, 2):
                    poses.append((self.pos[0] + x, self.pos[1] + y))
        else:
            raise ValueError("Unknown state")

        #locate unnecessary posses
        not_empty = []
        for tile in self.board.tiles_array:
            if tile.state != "00":
                not_empty.append(tile.pos)


        #remove any unnecessary posses
        for i in range(3):
            for pos in poses:
                if pos == self.pos or pos in not_empty:
                    poses.remove(pos)

        #format poses into option tiles
        options = []
        for pos in poses:
            for tile in self.board.tiles_array:
                if tile.pos == pos:
                    options.append(tile)
                    break
        for option in options:
            option.add_option()

    def add_option(self):
        self.option = True
        self.board.tiles_optioned.append(self)
        self.canvas.itemconfig(self.canvas_option_img, image=self.board.main.images["option"])
        self.update()

    def remove_option(self):
        self.option = False
        self.board.tiles_optioned.remove(self)
        self.canvas.itemconfig(self.canvas_option_img, image=self.board.main.images["empty"])
        self.update()

    def update(self):
        self.canvas.itemconfig(self.canvas_piece_img, image=self.board.main.images[Tile.states_dict[self.state]])


class Piece:
    type_dict = {1: "pawn", 2: "knight", 3: "bishop", 4: "rook", 5: "queen", 6: "king"}

    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.config = self.get_config()

    def get_config(self):
        config = []
        for y in range(8):
            for x in range(8):
                config.append()
        return config

def get_key_from_value(dict, value):
    return list(dict.keys())[list(dict.values()).index(value)]


if __name__ == '__main__':
    main = Main()
    main.main()
    main.restart_all_boards()

