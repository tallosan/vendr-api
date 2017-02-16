# Kangaa API

```javascript
BASE_URL = api.kangaa.xyz/v1/
```
---

### Properties Endpoint:
```javascript
URL               METHODS               AUTH & PERMISSIONS

properties/       *GET, POST         	OAuth & must be owner. GET has none.
properties/<id>/  *GET, PUT, DELETE  	OAuth & must be owner. GET has none.
```

### Users Endpoint:
```javascript
URL               METHODS               AUTH & PERMISSIONS

users/            *GET, *POST         	None.
users/<id>/       *GET, PUT, DELETE  	Oauth & must be owner. GET has none.
```

### Search Endpoint:

```javascript
URL               METHODS               AUTH & PERMISSIONS

search/<?model>/  *GET               	None.
```

#### parameters:
	model [REQUIRED]
		possible values: ['property', 'user']
		description: The type of resource we are performing the
			     search on.
	kwargs: [OPTIONAL]
		description: The filters to apply on our search.

		e.g. sqr_ftg=3200

#### how to:



Standard Queries:

- To create a query, specify the model type, and then append your query to the
  URL.

Complex Queries:

- To create more complex queries, you can simply chain kwargs together with an &.

Querying Nested Values:

- To query a nested value, first specify its container name. We can then access
  the containers nested values via a double underscore. An example in this case
  is worth a thousand words.

- To query a location objects country, we do ...
```javascript
		search/?model=property&location__country=Canada
```

#### Examples:

Get all properties with an area of exactly 3200 square feet.
```javascript
search?model=property&sqr_ftg=3200
```
Get all properties with an area greater than 3200 square feet.
```javascript
search?model=property&sqr_ftg__gt=3200
```
Get all properties in the city of Toronto, that have more than 3 bedrooms.
```javascript
search?model=property&location__city=Toronto&n_bedrooms__gt=3
```
---
