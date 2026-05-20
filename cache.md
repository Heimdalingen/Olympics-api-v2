# Cache
The cache should temporarily store info about the request and query.
This is only necessary for the GET requests returning text (not images).

If a user requests, say, all the medals of Usain Bolt, it may look something like this:

`GET /v1.2/athlete/123`

and it will return some data, for example in a JSON format. What we want to do is store the request and return data together (along with time of request), such that next time we get an GET request to the same endpoint, we can return the stored data, instead of re-querying the database. This saves time!

## Data deprecation
When data is older than 1 minute, we delete it.

When a request comes in, we should _first_ delete deprecated cache data, and then return from the cache.
This is not as efficient as keeping it up to date in the background, but much simpler.
<!-- Make a separete container keep it up to date? -->
