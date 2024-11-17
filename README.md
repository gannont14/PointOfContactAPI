# PointOfContactAPI

- [PointOfContactAPI][#PointOfContactAPI]
    - [Setup][#Setup]




## Setup

Clone the code
```python
git clone git@github.com:gannont14/PointOfContactAPI.git
```

Install the requirements 


## Documentation

-   Get point of contact from a repository name for the scrum master
```rs
GET /api/repos
Parameters:
    search_query=repo_name
```

```json
[
  {
    "repo name": "string",
    "repo url": "string",
    "product name": "string",
    "first name": "string",
    "last name": "string",
    "email": "string",
    "chat username": "string",
    "location": "string",
    "role": "string"
  }
]
```

-  Example using a search query of "Enterprise-wide-empowering-circuit-repo" 

```rs
GET /api/repos
Parameters:
    search_query=Enterprise-wide-empowering-circuit-repo
```

```json
[
  {
    "repo name": "Enterprise-wide-empowering-circuit-repo",
    "repo url": "https://github.com/sc1701d/enterprise-wide-empowering-circuit-repo",
    "product name": "Enterprise-wide empowering circuit",
    "first name": "Erika",
    "last name": "McKnight",
    "email": "erica.mcknight@sc1701d.com",
    "chat username": "@erikamcknight",
    "location": "Chicago, IL",
    "role": "Scrum Master"
  }
]
```


-   Get point of contact from a product name for the scrum master
```rs
GET /api/products
Parameters:
    search_query=repo_name
```

```json
[
  {
    "product name": "string",
    "first name": "string",
    "last name": "string",
    "email": "string",
    "chat username": "string",
    "location": "string",
    "role": "string"
  }
]
```

-  Example using a search query of "Managed systematic Intranet" 

```rs
GET /api/products
Parameters:
    search_query=Managed systematic Intranet
```

```json
[
    {
        "product name": "Managed systematic intranet",
        "first name": "Chad",
        "last name": "Hunt",
        "email": "chad.hunt@sc1701d.com",
        "chat username": "@chadhunt",
        "location": "Bloomington, IN",
        "role": "Scrum Master"
    }
]
```



