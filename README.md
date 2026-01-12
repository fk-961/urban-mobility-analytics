# Urban Mobility Analytics

## APIs
An API is an interface usually between an application (web) and us. It is used to query data using HTTP requests without having to download or import raw data and without worrying about how the processing works from the server side or storing the whole data locally. One disadvantage of an API is that it depends on the server and therefore it can change a lot if the API providers modify data or calls. In this case, our code may not work and we have to check the documentation again.

Calling an API is done by a `get` request and returns a `response` (JSON, XML, CSV) with a code. A code between 200 and 300 means usually that we got a response while 400-500 answers means something is wrong (server is down, access denied). Authentification for an API usually happens with keys, tokens, *whitelisting* (access to a specific pool of IPs) or OAuth. While querying an API for a huge dataset for example, it is common practice to use **pagination** (getting the data in batches while specifying limit and offset parameters as we did here).

### NYC 311 Service Requests
For this project, we are using the **NYC 311 Service Requests** Socrata API. Socrata lets us use parameters for GET requests such as WHERE and LIMIT. We can also check the [API's documentation](https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9) to know more. For simplicity, we are going to use the public version of the API and get some 2024 data since the data is huge. Our code should look something like this:
```
r = requests.get(api_url + endpoint, params = params)
r.raise_for_status()

data = r.json()
```
This is the baseline of API interaction using the `requests` module from Python. It is crucial to add the WHERE parameters to get 2024 data.

**Note:** When I first tried to create the script, I did not know about the WHERE parameter therefore I started querying the data, fetching it (`r.json()`) and checking the dates. This beats the purpose of batch checking since I am fetching every batch of data to check for dates and it implies the data is stored in chronological order.

### ACS Census API
This API gives us information about all the areas in the US like income, population and unemployement rate. We selected a small, interpretable set of variables commonly used in socioeconomic analysis:

| Variable Code	| Description |
| --- | --- |
| B19013_001E	| Median household income |
| B01003_001E	| Total population |
| B25077_001E	| Median home value |
| B23025_005E	| Number of unemployed persons |

## `config.py` and `.env`
While writing our scripts, we will most likely be using data folders paths and/or API keys and URLs. A good practice is to have a `config.py` where we define the paths to useful directories using the `pathlib` module. This way our code will run smoothly on any machine without having to rename the path variables.
```
ROOT_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = ROOT_DIR/"raw"
...
```
Considering that `config.py` is saved in `src/` directory, our project root therefore is the parent of our path at index 1 ( `__file__` being the current directory). Therefore, when we import our path variables in our scripts, we can create a new directory for example using `ROOT_DIR/"output_dir"` for example and then using the `mkdir(parents=True, exists_ok=True)` method.

The `.env` file is a safe space where we can add sensitive data like API keys that we do not wanna push into our remote repository. We need to use the `load_dotenv` function from the module `dotenv` at the beginning of the script so we can load the variables. Then we can access the variables by using `os.getenv("VAR_NAME")` for example.