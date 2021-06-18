from time import strftime, gmtime, time

HELP = '''\
Print position of your first step in form of 2 integers separated by space. 
Pring "exit" to stop the game.'''


def readable_time_since(t):
    return strftime("%M m. %S sec.", gmtime(int(time() - t)))
