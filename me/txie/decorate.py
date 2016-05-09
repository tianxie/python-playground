handlers = {}


def handler(type):
    def decorate(func):
        handlers[type] = func
        return func

    return decorate


@handler(type='a')
def a():
    pass


@handler(type='b')
def b():
    pass


print handlers
