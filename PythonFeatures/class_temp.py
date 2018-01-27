class Player:
    @property
    def name(self):
        return self.__name

    def __init__(self, name=''):
        self.__name = name
        self.__score = 0
        pass

    def append_score(self, score):
        self.__score += score


class Human(Player):
    def append_score(self, score):
        Player.append_score(self, score)
        self._Player__score += score


def test_main(p):
    print(p.name)
    p.append_score(300)
    print(p._Player__score)


p = Human("peter")

test_main(p)
