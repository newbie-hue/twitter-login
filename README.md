Functions for automating Twitter processes


#### Example
```python
from login import login

session = login(username,password)

print(session.cookies.get_dict())
```

#### Use authenticated session 
```python
queryId:str = ...
operation:str = ...
variables:dict = ...
features:dict = ...

headers:dict = ...

url = f"https://api.twitter.com/graphql/{queryId}/{operation}?variables={variables}&features={features}"
r = session.get(url,heaeders=headers)

print(r.json())
```
