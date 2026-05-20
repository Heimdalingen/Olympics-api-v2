# Rate limiter (per-user or in-total??)
A node holding track of how many requests we have received lately, and delay the response based on this.

It should have the following endpoints:

`POST /<user-id>` - Add a new request
```JSON
{
    "username": <string>
}
```

`GET /<user-id>` - Retrieve number of requests the last 10 seconds.
```JSON
{
    "delay": <float>
}
```

When the last 10 seconds have 10 or more requests, it should return a number of seconds of delay before returning the results. E.g.,

```python
delay: float = ...  # API call
time.sleep(delay)  # Sleep for `delay` seconds
return whatever
```

The Rate limiter should calculate the amount of seconds based on the following function.

$$ f(r) = \frac{r}{10} $$

where $r$ is the number of request the last 10 seconds. So when passing 10 requests the last 10 seconds, add a tenth of a second per these requests.

To keep track of the number of requests the last 10 seconds (or $n$ seconds), you need to store info about the last requests. It can be a list with times.
- New POST: Add current time as float.
- New GET: Remove 10+ seconds old times and count how many. If 10+, return r/10, otherwise return 0.
