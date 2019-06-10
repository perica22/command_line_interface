import sys
from .classmodule import MyClass
from .funcmodule import my_function


def main():
    print('in main')

    for arg in sys.argv[1:]:
        print('passed argument :: {}'.format(arg))
    my_function('hello world')
    my_object = MyClass('Thomas')
    my_object.say_name()


if __name__ == '__main__':
    main()
