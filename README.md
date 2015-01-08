# pypropeller
Rotating console propeller for running things in background.

## usage
```python
from pypropeller import Propeller

kwargs = {"cmd": ["ls"],
          "info": "Demo propeller with shell ls"}
my_propeller = Propeller(**kwargs)
print(my_propeller.execute())
```
