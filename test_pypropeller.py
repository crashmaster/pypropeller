#!/usr/bin/env python3
# encoding: utf-8

import time

from pypropeller import Propeller


def main():
    kwargs = {"func": my_sleep,
              "args": [3],
              "info": "Execute Python function 'my_sleep' in the propeller"}
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())

    kwargs = {"cmd": ["ls"],
              "info": "Execute shell command 'ls' in the propeller"}
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())

    kwargs = {"cmd": ["sleep", "1"],
              "info": "Execute shell command 'sleep 1' in the propeller"}
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())


def my_sleep(sleeptime):
    for i in range(sleeptime):
        print('i = %d' % i)
        time.sleep(1)


if __name__ == '__main__':
    main()
