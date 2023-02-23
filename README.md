Component to automate Twitter login process. Returns Login object containing authenticated session.


#### Example
```python
from login import Login

username = ...
password = ...

login = Login(username, password).run()
```

#### Use authenticated session 
```python
queryId: str = ...
operation: str = ...
variables: dict = ...
features: dict = ...

r = login.session.get(f"https://api.twitter.com/graphql/{queryId}/{operation}?variables={variables}&features={features}")

print(r.json())
```
