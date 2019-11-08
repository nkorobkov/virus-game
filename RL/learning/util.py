from time import strftime, gmtime, time


def readable_time_since(t):
    return strftime("%M m. %S sec.", gmtime(int(time() - t)))
