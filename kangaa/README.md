# Kangaa API

```javascript
BASE_URL = api.kangaa.xyz/v1/
```

### OAuth Keys:

#### client_id:

CVUK9hAGWf1AxoVJfjlUGgAThezkYrZ83dkGc6kg

#### client_secret:
3jtPlGH58i6X5tPlwwjzJNG5OOZ0LCSzyTcJHMCHd0pxSwtUG8wN318lelywFfqsDR8hodvxezLhBu4YEKGpEH2rGS2kHSRNKsSMrOTMlSr0xwa3vCRieX4UxoIAFlia

---

## Authentication:

The API is protected via OAuth. The OAuth endpoint is:

```javascript
http://api.kangaa.xyz/o/token/
```

In order to access protected resources, a user needs an access token.
The following example shows how the user with *email* 'superdev@kangaa.xyz', and *password* 'reallystrongpassword' is able
  to obtain an access token from the OAuth endpoint.


```javascript
curl -X POST -d "grant_type=password&username=superdev@kangaa.xyz&password=reallystrongpassword" -u"client_id:client_secret" http://api.kangaa.xyz/o/token/'
```

Upon issuing the above request, we'll get back a response that looks like ...

```json
{
    "access_token": "<your_access_token>",
    "token_type": "Bearer",
    "expires_in": 36000,
    "refresh_token": "<your_refresh_token>",
    "scope": "read write groups"
}
```

We can now use the access token to query any of superdev0's protected resources by setting the Authorization header.
```javascript
http http://api.kangaa.xyz/v1/transactions/8e4ae98c-f40a-4cfc-9e7b-6a6773149170/ 'Authorization:Bearer access_token'
```
---

## Endpoints:


### Properties Endpoint [POST, GET, PUT, DELETE]:

**POST**:

Create a new property object of type 'ptype'.

```javascript
POST	http://api.kangaa.xyz/v1/properties/<ptype>/	(Authentication Required)
```

#### Request Parameters:

| Parameter     | Description           | Values                      |
| ------------- |-----------------------| --------------------------- |
| ptype         | The type of property. | < condo, house, multiplex > |



**GET, UPDATE, DELETE**:

Get, Update, or Delete the property object with the given ID.

```javascript
GET	http://api.kangaa.xyz/v1/properties/<id>/
UPDATE	http://api.kangaa.xyz/v1/properties/<id>/    (Authentication Required)
DELETE	http://api.kangaa.xyz/v1/properties/<id>/    (Authentication Required)
```

#### Request Parameters:

| Parameter     | Description           | Values                  |
| ------------- |-----------------------| ----------------------- |
| id            | The property id.      | A valid property id	  |

---
### Users Endpoint [POST, GET, PUT, DELETE]:

**POST**

Create a new user.

```javascript
POST	http://api.kangaa.xyz/v1/users/
```


**GET, UPDATE, DELETE**:

Get, Update, or Delete the property object with the given ID.

```javascript
GET	http://api.kangaa.xyz/v1/users/<id>/
UPDATE	http://api.kangaa.xyz/v1/users/<id>/    (Authentication Required)
DELETE	http://api.kangaa.xyz/v1/users/<id>/    (Authentication Required)
```

#### Request Parameters:

| Parameter     | Description           | Values                  |
| ------------- |-----------------------| ----------------------- |
| id            | The user id.          | A valid user id	  |

---
### Search Endpoint [GET]:

**GET**:

Search on either properties or users.

```javascript
GET	http://api.kangaa.xyz/v1/search?<stype>&<query=query value>
```

#### Request Parameters:

| Parameter            | Description           | Values                  |
| -------------------- |-----------------------| ----------------------- |
| stype                | The type of search.   | < property, user >	 |
| query (*optional*)   | The search queries.   | Any valid search query. |


#### How To:

Standard Queries:

- To create a query, specify the search type, and then append your query to the
  URL.

Complex Queries:

- To create more complex queries, you can simply chain kwargs together with an &.

Querying Nested Values:

- To query a nested value, first specify its container name. We can then access
  the containers nested values via a double underscore. An example in this case
  is worth a thousand words.

- To query a location objects country, we do ...
```javascript
		search?stype=property&location__country=Canada
```

Querying Multiple Values On the Same Field:

- To query multiple values on the same field, pass in an array of these values.
- To query all Condos and Multiplexes, we do ...
```javascript
		search?stype=property&ptypes=[Condo,Multiplex]
```

#### Examples:

```javascript
// Get all properties with an area of exactly 3200 square feet.
search?stype=property&sqr_ftg=3200

// Get all properties with an area greater than 3200 square feet.
search?stype=property&sqr_ftg__gt=3200

//Get all properties in the city of Toronto, that have more than 3 bedrooms.
search?stype=property&location__city=Toronto&n_bedrooms__gt=3

// Get all Condo and House properties in Toronto.
search?stype=property&ptypes=[House, Condo]
```

---
### Autocomplete Endpoint [GET]:

**GET**:

Get autocomplete results on the given resource.

```javascript
GET	http://api.kangaa.xyz/v1/autocomplete?<type>&<term=term value>
```

#### Request Parameters:

| Parameter           | Description              | Values                 |
| ------------------- |--------------------------| ---------------------- |
| type                | The autocomplete type.   | < location, username > |
| term (*optional*)   | The current search term. | Any valid search term. |

#### Examples:

```javascript
// Get all properties starting with 'Tor'.
?type=location&term=Tor
```
---
### Transactions Endpoint [POST, GET, PUT, DELETE]:

This is probably the most complex endpoint. All actions on this resource require authentication, which
only users belonging to the transaction (buyer & seller) have.

In addition to generic authentication on the whole model, we also must handle field level permissions.

A Transaction object is simply a tool for organizing sub-objects involved in the transaction.
These are Offers, and Contracts.

We also look after the transaction stage (offer stage, contract stage, closing stage), along with any
additional metadata pertaining to the transaction.

**POST**

Create a new transaction.

```javascript
POST	http://api.kangaa.xyz/v1/transactions/    (Authentication Required)
```


**GET, UPDATE, DELETE**:

Get, Update, or Delete the transaction object with the given ID.

```javascript
GET	http://api.kangaa.xyz/v1/transactions/<id>/    (Authentication Required)
UPDATE	http://api.kangaa.xyz/v1/transactions/<id>/    (Authentication Required)
DELETE	http://api.kangaa.xyz/v1/transactions/<id>/    (Authentication Required)
```

#### Request Parameters:

| Parameter     | Description                  | Values                   |
| ------------- |------------------------------| ------------------------ |
| id            | The transaction id.          | A valid transaction id	  |

---

What a Transaction looks like in JSON:

```json
{
    "buyer": 35, 
    "id": "8e4ae98c-f40a-4cfc-9e7b-6a6773149170", 
    "kproperty": 52, 
    "offers": [
        {
            "buyer_offers": [
                {
                    "comment": "Please consider this new offer!", 
                    "deposit": 2000.0, 
                    "id": "98ff9a4f-820d-4864-92e9-f40671ed879f", 
                    "is_accepted": false, 
                    "offer": 350000.0, 
                    "owner": "tallosan@kangaa.xyz", 
                    "timestamp": "2017-04-22T19:55:18.106262Z"
                }, 
                {
                    "comment": "My initial offer!", 
                    "deposit": 2000.0, 
                    "id": "8f439a29-c6e4-4cd3-bb3d-30a2878216fc", 
                    "is_accepted": false, 
                    "offer": 350000.0, 
                    "owner": "tallosan@kangaa.xyz", 
                    "timestamp": "2017-04-22T19:54:55.674213Z"
                }, 
            ]
        }, 
        {
            "seller_offers": [
                {
                    "comment": "Please consider this counter offer!", 
                    "deposit": 2000.0, 
                    "id": "8f439a29-c6e4-4cd3-bb3d-30a2878216fc", 
                    "is_accepted": false, 
                    "offer": 350000.0, 
                    "owner": "tallosan@kangaa.xyz", 
                    "timestamp": "2017-04-22T19:54:55.674213Z"
                }, 
            ]
        }
    ], 
    "seller": 35, 
    "stage": 0, 
    "start_date": "2017-04-18T20:30:19.096212Z"
}
```

