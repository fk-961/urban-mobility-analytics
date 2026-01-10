# Urban Mobility Analytics

## APIs
An API is an interface usually between an application (web) us. It is used to query data using HTTP requests without having to download or import raw data and without worrying about how the processing works from the server side or storing the whole data locally. One disadvantage of an API is that it depends on the server and therefore it can change a lot if the API providers modify data or calls. In this case, our code may not work and we have to check the documentation again.

Calling an API is done by a `get` request and returns a `response` (JSON, XML, CSV) with a code. A code between 200 and 300 means usually that we got a response while 400-500 answers means something is wrong (server is down, access denied). Authentification for an API usually happens with keys, tokens, *whitelisting* (access to a specific pool of IPs) or OAuth. While querying an API for a huge dataset for example, it is common practice to use **pagination** (getting the data in batches while specifying limit and offset parameters as we did here).

For this project, we are using the **NYC 311 Service Requests** Socrata API. Socrata lets us use parameters for GET requests such as WHERE and LIMIT. We can also check the [API's documentation](https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9) to know more. For simplicity, we are going to use the public version of the API and get some 2024 data since the data is huge. Our code should look something like this:
```
r = requests.get(api_url + endpoint, params = params)
r.raise_for_status()

data = r.json()
```
This is the baseline of API interaction using the `requests` module from Python. It is crucial to add the WHERE parameters to get 2024 data.

**Note:** When I first tried to create the script, I did not know about the WHERE parameter therefore I started querying the data, fetching it (`r.json()`) and checking the dates. This beats the purpose of batch checking since I am fetching every batch of data to check for dates and it implies the data is stored in chronological order. 