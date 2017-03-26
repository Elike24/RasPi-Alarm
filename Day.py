from enum import Enum


class Day(Enum):  # replace Enum with Flag once using Python 3.6
    Mo = 1
    Tu = 2
    We = 4
    Th = 8
    Fr = 16
    Sa = 32
    Su = 64

    def __and__(self, other):
        assert isinstance(other, Day)
        return self.value & other.value

    def __or__(self, other):
        assert isinstance(other, Day)
        return self.value | other.value

    def to_int(self):
        return {
            Day.Mo: 0,
            Day.Tu: 1,
            Day.We: 2,
            Day.Th: 3,
            Day.Fr: 4,
            Day.Sa: 5,
            Day.Su: 6
        }.get(self, 0)

    @staticmethod
    def get_from_int(weekday: int):
        return {
            0: Day.Mo,
            1: Day.Tu,
            2: Day.We,
            3: Day.Th,
            4: Day.Fr,
            5: Day.Sa,
            6: Day.Su
        }.get(weekday, Day.Mo)

    @staticmethod
    def everyday():
        return Day.Mo | Day.Tu | Day.We | Day.Th | Day.Fr | Day.Sa | Day.Su