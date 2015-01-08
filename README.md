# pypropeller
Rotating console propeller for running things in background.

## usage

### execute simple shell command
```python
from pypropeller import Propeller

kwargs = {"cmd": ["ls"],
          "info": "shell command 'ls' in the propeller"}
my_propeller = Propeller(**kwargs)
print(my_propeller.execute())
```

### execute shell command with an argument
```python
from pypropeller import Propeller

kwargs = {"cmd": ["sleep", "1"],
          "info": "shell command 'sleep 1' in the propeller"}
my_propeller = Propeller(**kwargs)
print(my_propeller.execute())
```

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
