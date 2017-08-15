```javascript
BASE_URL = api.vendr.xyz/v1/
```

### OAuth Keys:

#### client_id:

foOWPCONHldZXPnkZ1wVUEBemyVZp3dcARY4p7Lb

#### client_secret:
dGoXvLV0vU3EikGHUcBrRXhxLJyyLxW4jlReSmJC2UQbo8EYta5W1MWZsLfgVgHh5k5zkhuSprIIVL6TZ8x4qPplqieeO9C4gQqN8VMXvnFx64PlmLdZ7tpbRdapychk

---

## Authentication:

The API is protected via OAuth. The OAuth endpoint is:

```javascript
http://api.vendr.xyz/o/token/
```

In order to access protected resources, a user needs an access token.
The following example shows how the user with *email* 'superdev@vendr.xyz', and *password* 'reallystrongpassword' is able
  to obtain an access token from the OAuth endpoint.


```javascript
curl -X POST -d "grant_type=password&username=superdev@vendr.xyz&password=reallystrongpassword" -u"client_id:client_secret" http://api.zappme.xyz/o/token/'
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
http http://api.vendr.xyz/v1/transactions/8e4ae98c-f40a-4cfc-9e7b-6a6773149170/ 'Authorization:Bearer access_token'
```
---

## Endpoints:


### Properties Endpoint [POST, GET, PUT, DELETE]:

**POST**:

Create a new property object of type 'ptype'.

```javascript
BODY

Content-Type: application/json
{
    "location": {
        "address": "60 Brian Harrison", 
        "city": "Toronto", 
        "country": "Canada", 
        "latitude": "43.773313", 
        "longitude": "-79.258729", 
        "postal_code": "M1P0B2", 
        "province": "Ontario"
    }, 
    "n_bathrooms": 1, 
    "n_bedrooms": 2, 
    "price": 250000.0, 
    "sqr_ftg": 3000.0,
    "unit_num": 1105,
    "tax_records": [
         {
             "assessment": 200000, "assessment_year": 2015
         }
     ],
     "history": {
         "last_sold_price": 20000,
         "last_sold_date": "2011-08-14",
         "year_built": 2010
     },
     "features": [
         { "feature": "Oven" },
         { "feature": "Pool" }
     ]
}
Multipart/form-data
{ images ... }

POST	http://api.vendr.xyz/v1/properties/<?ptype>	(Authentication Required)
```

#### Request Parameters:

| Parameter     | Description           | Values                      |
| ------------- |-----------------------| --------------------------- |
| ptype         | The type of property. | <condo, house, townhouse,   |
|		|			|  manufactured, vacant_land> |



**GET, UPDATE, DELETE**:

Get, Update, or Delete the property object with the given ID.

```javascript
GET	http://api.vendr.xyz/v1/properties/<id>/
UPDATE	http://api.vendr.xyz/v1/properties/<id>/    (Authentication Required)
DELETE	http://api.vendr.xyz/v1/properties/<id>/    (Authentication Required)
```

#### Request Parameters:

| Parameter     | Description           | Values                  |
| ------------- |-----------------------| ----------------------- |
| id            | The property id.      | A valid property id	  |


***Sample Response***:

```javascript
{
    "created_time": "2017-06-19T17:36:33.155889Z", 
    "features":
         { "feature": "Oven" },
         { "feature": "Pool" }
    },
    "history": {
         "last_sold_price": 20000,
         "last_sold_date": "2011-08-14",
         "year_built": 2010
    },
    "id": 1, 
    "images": [
        {
            "image": "https://s3.ca-central-1.amazonaws.com/media.zapp/listings/images/07482c04-7a0e-44a4-8f63-e488ec95a404", 
            "timestamp": "2017-06-19"
        },
        {
            "image": "https://s3.ca-central-1.amazonaws.com/media.zapp/listings/images/1d67cd2f-08d8-4250-b267-80c17771e6a6", 
            "timestamp": "2017-06-19"
        }
    ], 
    "is_featured": false, 
    "location": {
        "address": "18 Little Italy", 
        "city": "Torino", 
        "country": "Canada", 
        "latitude": "43.773313", 
        "longitude": "-79.258729", 
        "postal_code": "M230B3", 
        "province": "Ontario"
    }, 
    "n_bathrooms": 1, 
    "n_bedrooms": 2, 
    "price": 250000.0, 
    "sqr_ftg": 300.0,
    "unit_num": 1105,
    "offers": 0, 
    "owner": 1, 
    "price": 250000.0, 
    "sqr_ftg": 4200.0, 
    "tax_records": [
        {
            "assessment": 4250000.0, 
            "assessment_year": 2016
        }
    ], 
    "views": 30
}
```

### Open House & RSVP Endpoint [POST, GET, PUT, DELETE]:

Open Houses & RSVP's exist as sub-models on Property objects.
Sellers can create (POST) OpenHouses on their listings, view (GET), update (PUT), and cancel (DELETE)
them. Buyers can RSVP (POST) to an Open House, view (GET) all Open Houses for a Property, and cancel
their RSVP (DELETE).

**POST**

Sellers -- Create a new Open House.

```javascript
BODY
{
	"start": "2017-08-06T18:38:39.069638Z",
	"end": "2017-08-06T20:38:39.069638Z"
}

POST	http://api.vendr.xyz/v1/properties/<property_id>/openhouses/    (Authentication Required)
```

Buyers -- RSVP to an Open House.

```javascript
BODY
{

}

POST	http://api.vendr.xyz/v1/properties/<property_id>/openhouses/<openhouse_id>/rsvp/    (Authentication Required)
```

---
### Users Endpoint [POST, GET, PUT, DELETE]:

**POST**

Create a new user.

```javascript
BODY
{
	"email":"superdev@vendr.xyz",
	"password": "reallystrongpassword",
	"profile":
		{
			"first_name":"super",
			"last_name": "dev",
			"location": "Toronto",
			"bio": "I write code."
		}
	}
}

POST	http://api.vendr.xyz/v1/users/
```


**GET, UPDATE, DELETE**:

Get, Update, or Delete the user object with the given ID.

*Updating Image Fields*:

We're using multipart/form-data encoding for images, and unfortunately nested updates are
not supported. This is problematic here, as a user's profile pic is stored on their nested
Profile model. The following workaround solves this problem:

To update a file / image field, you ONLY pass the field's name in the multipart/form-data request.
I.e. ignore the fact that the field is nested!

For example, updating a user's profile pic is done like so:

```javascript
prof_pic=@my_image.jpg
```

Resolving the actual model to update (in this case, the Profile model) is all taken care of in the API.

```javascript
GET	http://api.vendr.xyz/v1/users/<id>/
UPDATE	http://api.vendr.xyz/v1/users/<id>/    (Authentication Required)
DELETE	http://api.vendr.xyz/v1/users/<id>/    (Authentication Required)
```

#### Request Parameters:

| Parameter     | Description           | Values                  |
| ------------- |-----------------------| ----------------------- |
| id            | The user id.          | A valid user id	  |


***Sample Response***:

```javascript
[
    {
        "email": "tallosan@vendr.xyz", 
        "id": 1, 
        "join_date": "2017-06-19T17:10:41.713149Z", 
        "notifications": [], 
        "password": "bcrypt_sha256$$2b$12$rdd/V7y4vIB/Ilj6nfm07um8DjW5mgSjwiADung7/DK0qYJXFVA7y", 
        "profile": {
            "bio": "", 
            "first_name": "", 
            "last_name": "", 
            "location": "", 
            "prof_pic": "http://api.vendr.xyz/media/profiles/default.svg"
        }, 
        "properties": [
		3
	], 
        "transactions": {
            "incoming": [
	    	"8367365d-5730-4096-9d92-efd7e778eae9"
	], 
            "outgoing": [
	]
        }
    }
]
```

### Notifications Endpoint [GET/LIST, PUT]:

Notification objects exist as sub-models on User objects.
These objects are created in response to events on other models in the system, but NEVER directly
by a user.

The only change a user can make is to the **is_viewed** field, which indictates whether
or not a user has seen the notification.

```javascript
RESPONSE
{
	'transaction': 'e2f48a7a-af03-4254-86e0-0e0686294798',
	'description': u'stone has sent you a new offer on your property 3000 Victoria Park Ave.',
	'offer': '4427a4df-153e-4159-8e6f-ba48e7356f66',
	'timestamp': u'2017-08-09T13:40:49.401360Z', 
	'is_viewed': False,
	'recipient': 2,
	'id': 'cfbe6be2-0952-4edf-a775-83e84aafe764'
}

GET	http://api.vendr.xyz/v1/users/<user_id>/    (Authentication Required)
```

### Chat & Message Endpoint:

Chat & Message objects exist as sub-models on User objects.
To send a message, a User first creates (POST) a Chat with the intended recipient/s. Then, assuming
this is successful, they can both start sending (POST) messages to the Chat object created.

The chat flow is like this:

User 0 likes a house being sold by users 1 & 3. He wants to schedule an open house with them, but
unfortunately none are taking place during his spare time. Thus, he wants to message them to set
something up.
0 creates a Chat object with participants = 1, 3.

Now, all 3 users have access to the created Chat.

They can now send messages by posting to it, which will subsequently be readable by all participants.

Any member can delete the Chat, thereby ending the conversation.


0 creates the chat. N.B. -- The chat MUST be CREATED on the user's own
endpoint (in this case /users/0/chat/). After this, all users will have access to the chat on their OWN respective endpoints.

***Chat [POST, GET, DELETE]***
```javascript
BODY
{
	"participants": [1, 3]
}

POST	http://api.vendr.xyz/v1/users/<user_id>/chat/    (Authentication Required)
```

The Chat will look like this ...

```javascript
RESPONSE
{
    "participants": [
    	0,
        1,
        3
    ], 
    "pk": "4398f64f-6aaa-47cc-9c65-b3c1daefb4d6"
}

GET	http://api.vendr.xyz/v1/users/<user_id>/chat/<chat_id>/    (Authentication Required)
```

Again, it is accessible to each participant ONLY on their respective endpoints, and all further actions (message
creations, chat deletions, etc.) must be done there.

In this case, 0 operates on .../users/0/chat/, 1 on .../users/1/chat/, and 3 on .../users/3/chat/

***Message [POST, GET]***
```javascript
BODY
{
	"content": "Hey, I love the house! Any chance I could come by to check it out tomorrow?"
}

POST	http://api.vendr.xyz/v1/users/<user_id>/chat/<chat_id>/messages/    (Authentication Required)
```

A user can POST a message to a chat. These messages are now accessible to all of the chat's participants.

```javascript
RESPONSE
{
    {
	"content": "Hey, I love the house! Any chance I could come by to check it out tomorrow?",
	"pk": "19f2036f-5f6b-45a8-a582-83efda6848e8", 
        "sender": 0, 
        "timestamp": "2017-08-08T20:01:38.517666Z"
    }, 
    {
        "content": "Of course, I'll just double check with my wife.",
        "pk": "48b94ad9-b8ef-4442-9403-997c7fed115c", 
        "sender": 3, 
        "timestamp": "2017-08-08T21:47:06.996285Z"
    },
    {
        "content": "Fine with me!",
        "pk": "48b94ad9-b8ef-4442-9403-997c7fed115c", 
        "sender": 1, 
        "timestamp": "2017-08-08T21:47:06.996285Z"
    }
}

GET	http://api.vendr.xyz/v1/users/<user_id>/chat/<chat_id>/messages/    (Authentication Required)
```

### Live Endpoints -- Notifications, Messages [GET]:

The Vendr API also allows for live updates. These updates exist on the following subdomain:

```javascript
BASE_URL = notify.vendr.xyz/
```

To access them, you will need to establish a websocket connection using Socket.IO.

An example client can be found [here](https://github.com/tallosan/vendr-api/blob/master/vendr/notify/test_client.js)

Currently our API supports live updates for notifications and messages.

These endpoints are documented below. Note, a user will need to suppy their OAuth token (just like with any other resource) in order to connect. This is demonstrated in the test client linked above.


```javascript
Resource:	URL:				Channel:

Notifications	http://notify.vendr.xyz/	users.<user_pk>.notifications    (Authentication Required)
Messages	http://notify.vendr.xyz/	users.<user_pk>.inbox    	 (Authentication Required)
```

---
### Search Endpoint [GET]:

**GET**:

Search on either properties or users.

```javascript
GET	http://api.vendr.xyz/v1/search?<stype>&<query=query value>
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
- To query all Condos and Townhouses, we do ...
```javascript
		search?stype=property&ptypes=[Condo,Townhouse]
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
GET	http://api.vendr.xyz/v1/autocomplete?<type>&<term=term value>
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

A Transaction model is simply a container for organizing sub-objects involved in the transaction; Offers, and Contracts.
Transactions also look after any clerical or meta data.

### On Stages:

A transaction can be in one of 3 stages, represented in the transaction model as an integer 'stage':

0 -- Offer stage.

1 -- Contract stage.

2 -- Closing stage.


Each stage limits the resources and actions that can be performed on a transaction. For example, when in the Offer stage,
a user can ONLY interact with the offer resources.

Each stage has a set of 2 'accepted' resources. When these are equal, they represent an agreement between both parties.
For example, when in the offer stage, note that a transaction has 2 accepted offer resources named:

buyer_accepted_offer & seller_accepted_offer.

Users should be setting their corresponding accepted resource once they are happy with the state of the transaction.
To move to the next stage, the user should attempt to increment the stage variable. This will only succeed if the 2 accepted
resources are not null, and are equal (i.e. point to the same offer).


**POST**

Create a new transaction.

```javascript
BODY:

POST	http://api.vendr.xyz/v1/transactions/    (Authentication Required)
```

**GET, UPDATE, DELETE**:

Get, Update, or Delete the transaction object with the given ID.

```javascript
GET	http://api.vendr.xyz/v1/transactions/<id>/    (Authentication Required)
UPDATE	http://api.vendr.xyz/v1/transactions/<id>/    (Authentication Required)
DELETE	http://api.vendr.xyz/v1/transactions/<id>/    (Authentication Required)
```

#### Request Parameters:

| Parameter     | Description                  | Values                   |
| ------------- |------------------------------| ------------------------ |
| id            | The transaction id.          | A valid transaction id	  |

---


***Sample Response***:

```javascript
{
    "buyer": 1, 
    "buyer_accepted_contract": null, 
    "buyer_accepted_offer": "384ddec8-d904-4e11-bfda-7b3030b1c372", 
    "contracts": [], 
    "id": "23fdebcf-82f4-4150-92c7-9724ec02669e", 
    "kproperty": 3, 
    "offers": {
        "buyer_offers": [
            {
                "comment": "Please consider this offer!", 
                "deposit": 20000.0, 
                "id": "384ddec8-d904-4e11-bfda-7b3030b1c372", 
                "offer": 350000.0, 
                "owner": 1, 
                "timestamp": "2017-06-19T19:40:08.570101Z"
            }
        ], 
        "seller_offers": [
        ]
    }, 
    "seller": 1, 
    "seller_accepted_contract": null, 
    "seller_accepted_offer": null, 
    "stage": 0, 
    "start_date": "2017-06-19T19:40:08.490699Z"
}
```
### Transactions / Offers [POST, GET, DELETE]:

**POST**

Create a new offer.

```javascript
BODY: 

{	
	"offer": 300000,
	"deposit": 20000,
	"comment": "Hello Mr. Owner, I hope you will consider my offer."
}

POST	http://api.vendr.xyz/v1/transactions/<transaction_id>/offers/    (Authentication Required)
```

#### Request Parameters:

| Parameter      | Description                  | Values                                |
| -------------- |------------------------------| ------------------------------------- |
| transaction_id | The transaction id.          | The transaction the offer belongs to. |


**GET, DELETE**:

Get or Delete the offer object with the given ID. N.B. -- It makes no sense for us to handle updates.

```javascript
GET	http://api.vendr.xyz/v1/transactions/<transaction_id>/offers/<offer_id>    (Authentication Required)
DELETE	http://api.vendr.xyz/v1/transactions/<transaction_id>/offers/<offer_id>    (Authentication Required)
```

#### Request Parameters:

| Parameter      | Description                  | Values                                |
| -------------- |------------------------------| ------------------------------------- |
| transaction_id | The transaction id.          | The id of the offer's transaction.    |
| offer_id       | The offer id.                | The id of the offer.                  |


***Sample Response***:

```javascript
{
    "buyer_offers": [
        {
            "comment": "Hello Mr. Owner, I hope you will consider my offer.", 
            "deposit": 20000.0, 
            "id": "1b4872d9-66a4-4c1c-a5a2-3a9a67d68c1b", 
            "offer": 300000.0, 
            "owner": 1, 
            "timestamp": "2017-06-19T19:49:20.018898Z"
        }, 
        {
            "comment": "Fair enough, I accept!", 
            "deposit": 20000.0, 
            "id": "384ddec8-d904-4e11-bfda-7b3030b1c372", 
            "offer": 350000.0, 
            "owner": 1, 
            "timestamp": "2017-06-19T19:40:08.570101Z"
        }
    ], 
    "seller_offers": [
        {
            "comment": "I feel my property is worth $5000 more.", 
            "deposit": 20000.0, 
            "id": "1b4872d9-66a4-4c1c-a5a2-3a9a67d68c1b", 
            "offer": 350000.0, 
            "owner": 1, 
            "timestamp": "2017-06-19T19:49:20.018898Z"
        }, 
    ]
}
```
---

### Transactions / Contracts[POST, GET, PUT, DELETE]:

N.B. -- A user can only have ONE contract for any given transaction.

**POST**

Create a new contract.

```javascript

POST	http://api.vendr.xyz/v1/transactions/<transaction_id>/contracts/?ctype/    (Authentication Required)
```

#### Request Parameters:

| Parameter      | Description                  | Values                                |
| -------------- |------------------------------| ------------------------------------- |
| transaction_id | The transaction id.          | The id of the contract's transaction. |
| ctype          | The type of property.        | < condo, house, townhouse,            |
|		 |			        |  manufactured, vacant_land >          |

**GET, UPDATE, DELETE**:

Get, Update, or Delete the contract object with the given ID.

```javascript
GET	http://api.vendr.xyz/v1/transactions/<transaction_id>/contracts/<contract_id>    (Authentication Required)
UPDATE	http://api.vendr.xyz/v1/transactions/<transaction_id>/contracts/<contract_id>    (Authentication Required)
DELETE	http://api.vendr.xyz/v1/transactions/<transaction_id>/contracts/<contract_id>    (Authentication Required)
```

#### Request Parameters:

| Parameter      | Description                  | Values                                |
| -------------- |------------------------------| ------------------------------------- |
| transaction_id | The transaction id.          | The id of the contract's transaction. |
| contract_id    | The contract id.             | The id of the contract.               |


***Sample Response***:

```javascript
{
    "clauses": "http://api.vendr.xyz/v1/transactions/23fdebcf-82f4-4150-92c7-9724ec02669e/contracts/85336987-4e53-40cd-a02d-253658167c57/clauses/", 
    "id": "85336987-4e53-40cd-a02d-253658167c57", 
    "owner": 1, 
    "timestamp": "2017-06-19T19:43:21.081036Z"
}
```
---

### Transactions / Contracts / Clauses [GET, PUT]:

There are two types of clauses: static, and dynamic.
There difference is that static clauses cannot be removed or edited, whereas dynamic clauses can.

***Clause Anatomy***:

Each dynamic clause has two views, a generator view, and a preview view.
Each static clause only has the preview view.
There are only two fields that you can edit on a dynamic clause:
```javascript
is_active and value.
```

To remove a dynamic clause, set its 'is_active' field to False.
To update a dynamic clause's value, set its 'value' field.

**GET, UPDATE**:

Get, Update, or Delete the contract object with the given ID.

```javascript
GET	http://api.vendr.xyz/v1/transactions/<transaction_id>/contracts/<contract_id>/clause/<clause_id>    (Authentication Required)
UPDATE	http://api.vendr.xyz/v1/transactions/<transaction_id>/contracts/<contract_id>/clause/<clause_id>    (Authentication Required)
DELETE	http://api.vendr.xyz/v1/transactions/<transaction_id>/contracts/<contract_id>/clause/<clause_id>    (Authentication Required)
```

#### Request Parameters:

| Parameter      | Description                  | Values                                |
| -------------- |------------------------------| ------------------------------------- |
| transaction_id | The transaction id.          | The id of the contract's transaction. |
| contract_id    | The contract id.             | The id of the contract.               |
| clause_id      | The clause id.               | The id of the clause.                 |


***Sample Response***:

N.B. -- We are only showing one clause of each type to keep things short.

```javascript
{
    "dynamic_clauses": [
        {
            "generator": {
                "category": "U", 
                "prompt": "Ensure Chattels & Fixtures are in good working order", 
                "ui_type": "TOGGLE", 
                "value": true
            }, 
            "id": "9f777fa0-f4bc-4d46-9365-fc86cefb385b", 
            "is_active": true, 
            "preview": "The Seller represents and warrants that the chattels and fixtures as included in this Agreement will be in good working order and free from liens and encumbrances on completion. The parties in this Agreement of Purchase and Sale agree that this representation and warranty shall survive and not merge on completion of this transaction, but apply only to those circumstances existing at the date of completion stated herein.", 
            "title": "Chattels and Fixtures"
        }
    ], 
    "static_clauses": [
        {
            "id": "b0a4dd10-4d6c-4a19-9f4d-bb70e43d0868", 
            "is_active": true, 
            "preview": "Notwithstanding the completion date set out in the Agreement, the parties in this Agreement may, by mutual agreement in writing, advance or extend the completion date of this transaction. ", 
            "title": "Completion Date Adjustments"
        }
    ]
}
```
---

