from enum import Enum


class UserLevels(Enum):
    L1 = 1
    L2 = 2
    ADMIN = 100

    def __gt__(self, user_level2: "UserLevels"):
        return self.value > user_level2.value

    def __ge__(self, user_level2: "UserLevels"):
        return self.value >= user_level2.value

    def __lt__(self, user_level2: "UserLevels"):
        return self.value < user_level2.value

    def __le__(self, user_level2: "UserLevels"):
        return self.value <= user_level2.value
