# coding: utf-8
import types


# Stragety design pattern
class StragetyExample:
    def __init__(self, func=None):
        self.name = 'Strategy Example 0'
        if func is not None:
            self.execute = types.MethodType(func, self)  # Python 3+
            # self.execute = types.MethodType(func, obj, obj.__class__)  # Python 2

    def execute(self):
        print(self.name)


def execute_replacement1(self):
    print(self.name + ' from execute 1')


def execute_replacement2(self):
    print(self.name + ' from execute 2')


if __name__ == '__main__':
    strat0 = StragetyExample()

    strat1 = StragetyExample(execute_replacement1)
    strat1.name = 'Strategy Example 1'

    strat2 = StragetyExample(execute_replacement2)
    strat2.name = 'Strategy Example 2'

    strat0.execute()  # 调用默认的execute
    strat1.execute()  # 调用注入的函数
    strat2.execute()  # 调用注入的函数
