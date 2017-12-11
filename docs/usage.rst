Usage
=====

Examples
--------

Execute python function with an argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pypropeller import Propeller

    def my_sleep(sleeptime):
        for i in range(sleeptime):
            print('i = {}'.format(i))
            time.sleep(1.0)

    kwargs = {
        "func": my_sleep,
        "args": [3],
        "info": "Execute Python function 'my_sleep' in the propeller"
    }
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())

Result
++++++

.. code-block:: none

    [+] Python function 'my_sleep' in the propeller
    Executed Item:    my_sleep(3)
    Execution Time:   3.015s
    Return Value:     True
    Exception caught: False
    Standard output:
    i = 0
    i = 1
    i = 2
    Standard Error:
    None
    Exception:
    None

Execute simple shell command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pypropeller import Propeller

    kwargs = {
        "cmd": ["ls"],
        "info": "Execute shell command 'ls' in the propeller"
    }
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())

Result
++++++

.. code-block:: none

    [+] shell command 'ls' in the propeller
    Executed Item:    ls
    Execution Time:   0.002s
    Return Value:     True
    Exception caught: False
    Standard output:
    console.py
    LICENSE
    __pycache__
    pypropeller.py
    README.md
    test_pypropeller.py
    Standard Error:
    None
    Exception:
    None

Execute shell command with an argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pypropeller import Propeller

    kwargs = {
        "cmd": ["sleep", "1"],
        "info": "Execute shell command 'sleep 1' in the propeller"
    }
    my_propeller = Propeller(**kwargs)
    print(my_propeller.execute())

Result
++++++

.. code-block:: none

    [+] shell command 'sleep 1' in the propeller
    Executed Item:    sleep 1
    Execution Time:   1.004s
    Return Value:     True
    Exception caught: False
    Standard output:
    None
    Standard Error:
    None
    Exception:
    None
