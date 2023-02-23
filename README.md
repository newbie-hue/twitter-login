Component to automate Twitter login process. Returns authenticated session.


#### Example
```python
from login import Login

username = ...
password = ...

login = Login(username, password).run()

print(login.content)
print(login.session.cookies.get_dict())
    
```
