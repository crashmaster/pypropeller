#!/usr/bin/env python3
# encoding: utf-8

import time

from pypropeller import Propeller


def main():
    kwargs = {"func": my_sleep,
              "args": [3],
              "info": "Demo propeller with Python function and arguments"}
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())

    kwargs = {"cmd": ["ls"],
              "info": "Demo propeller with shell ls"}
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())

    kwargs = {"cmd": ["sleep", "1"],
              "info": "Demo propeller with shell sleep and arguments"}
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())


def my_sleep(sleeptime):
    for i in range(sleeptime):
        print('i = %d' % i)
        time.sleep(1)


if __name__ == '__main__':
    main()
