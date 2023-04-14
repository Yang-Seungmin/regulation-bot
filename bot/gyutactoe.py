import datetime

from discord import User

from bot.source.gyutactoedb import GyutactoeResult


class GTTError(RuntimeError):
    pass


class TurnError(GTTError):
    def __init__(self, real_turn: User):
        self.real_turn = real_turn


class EndError(GTTError):
    pass


class PositionIsDuplicatedMeError(GTTError):
    pass


class PositionIsDuplicatedOtherError(GTTError):
    def __init__(self, user: User):
        self.user = user


class UserIsNotFullError(GTTError):
    pass


class UserIsFullError(GTTError):
    pass


class GyuTacToe:
    turn = 0
    gyutactoe: list[list[tuple[User, int] | None]] = [[None, None, None], [None, None, None], [None, None, None]]
    fight_with_regulation = False
    transparent = None

    def __init__(self):
        self.gyutactoe = [[None, None, None], [None, None, None], [None, None, None]]
        self.players: list[User] = []
        self.emojies = []
        self.record: list[tuple[int, int]] = []

    def enter(self, user: User, emoji):
        if self.is_all_user_entered():
            raise UserIsFullError
        self.players.append(user)
        self.emojies.append(emoji)
        return self.is_all_user_entered()

    def get_player_count(self):
        return len(self.players)

    def is_all_user_entered(self):
        return len(self.players) == 2

    def go(self, user: User, x: int, y: int):
        if not self.is_all_user_entered():
            raise UserIsNotFullError

        if not self.players[self.turn] == user:
            raise TurnError(self.players[self.turn])

        if self.gyutactoe[y - 1][x - 1] == user:
            raise PositionIsDuplicatedMeError

        if self.gyutactoe[y - 1][x - 1] is not None:
            raise PositionIsDuplicatedOtherError(self.gyutactoe[y - 1][x - 1][0])

        if not 1 <= x <= 3 or not 1 <= y <= 3:
            raise IndexError

        self.gyutactoe[y - 1][x - 1] = (user, self.turn)
        self.turn = (0 if self.turn == 1 else 1)
        self.record.append((x - 1, y - 1))
        winner = self.check()
        tile = self.get_gyutactoe_tile()
        is_end = self.is_end(winner)

        if is_end:
            GyutactoeResult.create(
                datetime=datetime.datetime.now(),
                player1=str(self.players[0].id),
                player2=str(self.players[1].id),
                winner='1' if winner is self.players[0] else '2' if winner is self.players[1] else 'N',
                record=''.join(map(lambda item: f'{item[0]}{item[1]}', self.record))
            )

        return tile, winner, is_end

    def check(self):
        winner = None
        gtt = self.gyutactoe

        for i, player in enumerate(self.players):
            if (gtt[0][0] == (player, i) and gtt[1][0] == (player, i) and gtt[2][0] == (player, i)) or \
                    (gtt[0][1] == (player, i) and gtt[1][1] == (player, i) and gtt[2][1] == (player, i)) or \
                    (gtt[0][2] == (player, i) and gtt[1][2] == (player, i) and gtt[2][2] == (player, i)) or \
                    (gtt[0][0] == (player, i) and gtt[0][1] == (player, i) and gtt[0][2] == (player, i)) or \
                    (gtt[1][0] == (player, i) and gtt[1][1] == (player, i) and gtt[1][2] == (player, i)) or \
                    (gtt[2][0] == (player, i) and gtt[2][1] == (player, i) and gtt[2][2] == (player, i)) or \
                    (gtt[0][0] == (player, i) and gtt[1][1] == (player, i) and gtt[2][2] == (player, i)) or \
                    (gtt[0][2] == (player, i) and gtt[1][1] == (player, i) and gtt[2][0] == (player, i)):
                winner = player

        return winner

    def get_gyutactoe_tile(self):
        result = ''
        for row in self.gyutactoe:
            for tile in row:
                if tile is not None:
                    result += '<:{name}:{id}>'.format(name=self.emojies[tile[1]].name, id=self.emojies[tile[1]].id)
                else:
                    result += '<:{name}:{id}>'.format(name=self.transparent.name, id=self.transparent.id)
            result += '\n'
        return result

    def is_end(self, winner=None):
        if winner is not None:
            return True

        for row in self.gyutactoe:
            for tile in row:
                if tile is None:
                    return False

        return True
