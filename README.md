# pypropeller
Rotating console propeller for running things in background.

## usage

### execute python function with an argument
```python
from pypropeller import Propeller

kwargs = {"func": my_sleep,
          "args": [3],
          "info": "Python function 'my_sleep' in the propeller"}
my_propeller = Propeller(**kwargs)
print(my_propeller.execute())

def my_sleep(sleeptime):
    for i in range(sleeptime):
        print('i = %d' % i)
        time.sleep(1)
```

```
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
```

### execute simple shell command
```python
from pypropeller import Propeller

kwargs = {"cmd": ["ls"],
          "info": "shell command 'ls' in the propeller"}
my_propeller = Propeller(**kwargs)
print(my_propeller.execute())
```

```
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
```

### execute shell command with an argument
```python
from pypropeller import Propeller

kwargs = {"cmd": ["sleep", "1"],
          "info": "shell command 'sleep 1' in the propeller"}
my_propeller = Propeller(**kwargs)
print(my_propeller.execute())
```

```
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
```
