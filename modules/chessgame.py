import chess.pgn
import re

class Turn:

    def __init__(self, turn):
        self.turn = turn
        self.turn_number, self.white_move, self.black_move = self.parse(turn)

    def parse(self,turn):
        turn_parts = turn.split(" ")
        turn_number = int(re.search(r'\d+', turn_parts[0]).group())
        white_move = turn_parts[1]
        black_move = turn_parts[2] if len(turn_parts) > 2 else None

        return turn_number, white_move, black_move
    
    def move_to_text(self, move):

        # Define the maps
        extension_map = {
            "+": "check",
            "#": "checkmate",
            "=N": "promotes to knight",
            "=B": "promotes to bishop",
            "=R": "promotes to rook",
            "=Q": "promotes to queen"
        }

        piece_to_string_map = {
            "": "Pawn",
            "a": "Pawn",
            "b": "Pawn",
            "c": "Pawn",
            "d": "Pawn",
            "e": "Pawn",
            "f": "Pawn",
            "g": "Pawn",
            "h": "Pawn",
            "N": "Knight",
            "B": "Bishop",
            "R": "Rook",
            "Q": "Queen",
            "K": "King"
        }

        print(move)
            
        piece = re.search(r'\A[NBRQK]|\A[a-h]', move)
        extension = re.search(r'[+#]|=[NBRQ]', move)

        move_text = ""
        
        if move == "O-O-O":
            move_text += "Queen side castle"
            if extension:
                move_text += " " + extension.group()
        elif move == "O-O":
            move_text += "King side castle"
            if extension:
                move_text += " " + extension.group()
        else:
            action = "takes" if "x" in move else "to"
            piece_name = piece_to_string_map[piece.group() if piece else ""]
            target_square = re.search(r'[a-h][1-8]', move)
            move_text += f"{piece_name} {action} {target_square.group() if target_square else ''}"
            if extension:
                move_text += f", {extension_map[extension.group() if extension else '']}"
        print(move_text)
        return move_text
    
    

    def to_text(self):

        return f"{self.turn_number} - {self.move_to_text(self.white_move)} – {self.move_to_text(self.black_move) if self.black_move else '' } "

class Game:

    def __init__(self, pgn):
        self.pgn_file = pgn
        self.game = chess.pgn.read_game(pgn)
        self.game_moves = self.game.mainline_moves()
        self.moves_string = str(self.game_moves)
        self.result = self.game.headers["Result"]
        
        pattern = r'(?=\s\d+[.]\s)'
        self._turns = [Turn(turn.strip()) for turn in re.split(pattern, self.moves_string)]
        self.length = len(self._turns)

    @property
    def turns(self):
        return self._turns
    
    def turn(self, turn_number):
        return self._turns[turn_number-1]
    
    def result_to_text(self, result):

        result_map_checkmate = {
            "0-1": "Black wins",
            "1-0": "White wins",
        }

        result_map = {
            "0-1": "White resigns",
            "1-0": "Black resigns",
            "1/2-1/2": "Draw"
        }

        result_text = result_map_checkmate[self.result] if '#' in self.turn else result_map[self.result]

        return result_text
    
    

    

    

if __name__ == "__main__":
    with open("modules/chess/PGN/Maffnuff_vs_aMagnu_2025.03.06.pgn", "r") as pgn:
        game = Game(pgn)
    print("\n".join([turn.to_text() for turn in game.turns]))
    print(game.game.mainline())
    print(game.game.mainline_moves())
    print(game.game.headers)
    print(game.game.board())