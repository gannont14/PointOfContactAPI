# PointOfContactAPI

- [PointOfContactAPI][#PointOfContactAPI]
    - [Setup](#Setup)
    - [Documentation](#Documentation)
        - [Contact from Repository](#get-point-of-contact-from-repository-name)
        - [Contact from Product](#get-point-of-contact-from-product-name)
        - [Entire Team Contact](#get-entire-team-contact-information-from-product-name)




## Setup

Clone the code
```python
git clone git@github.com:gannont14/PointOfContactAPI.git
```

Install the requirements 


## Documentation

## Get Point of Contact from repository name
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
    search_query=enterprise-wide-empowering-circuit-repo
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


## Get point of contact from product name
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
    search_query=managed systematic intranet
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

## Get entire team contact information from product name

```rs
GET /api/products/all_contacts
Parameters:
    product_name=product_name
```

-   Returns a list of all contacts associated with a project, and their roles

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
  },
  \cdots
]
```

-  Example using a search query of "fundamental optimizing paradigm" 

```rs
GET /api/products/all_contacts
Parameters:
    product_name=fundamental optimizing paradigm
```

```json
[
    {
        "product name": "Fundamental optimizing paradigm",
        "first name": "Gregory",
        "last name": "Barton",
        "email": "gregory.barton@sc1701d.com",
        "chat username": "@gregorybarton",
        "location": "Berlin, DE",
        "role": "Scrum Master"
    },
    {
        "chat username": "@michaelbaker",
        "email": "michael.baker@sc1701d.com",
        "first name": "Michael",
        "last name": "Baker",
        "location": "Berlin, DE",
        "product name": "Fundamental optimizing paradigm",
        "role": "Product Owner"
    },
    \.\.\.
```
