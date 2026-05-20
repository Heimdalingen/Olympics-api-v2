# Token shop
We won't actually touch _real_ money APIs, so we will make our own version.


## System flow
When "buying" tokens, you will buy it from this service.

`POST /buy`

Input
```JSON
{
    "username": <string>,  // Which user the tokens are bought for
    "money": <int>  // How many manies should be bought
}
```

The results should be a return message with a secret code. Return
```JSON
{
    "secret": <string>
}
```

The user will then take this code to the main API, and the main API will check with the show API how many money you paid, and then figure out how many tokens to add.

Main API input
```JSON
{
    "code": <string>
}
```

Main API request to token shop
```JSON
{
    "code": <string>
}
```

Token shop response
```JSON
{
    "tokens": <int>
}
```

The main API will add $x$ amount of tokens to your account, depending on what the current token price is now. Admins should be able to update this price. Users should be able to see it by running a GET on `<main-API>/v/tokens`.


## Reuse of codes
Importantly, the system should ensure the money won't be counted twice. Some suggestions on how to stop this from happening is
- Token shop also returns number of times this code has been used, or _if_ it has been used. Or even just delete after use/GET-request.
- The main API can keep track of previous codes, and ensure it does not reuse codes.
