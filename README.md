# Urban Mobility Analytics

## Techincal notes

### `pathlib` vs `os`
Throughout this project, we are using the module `pathlib` to define our paths to our directories. It is better than using `os` module since it handles path varibales as objects and it is easier to use it accross different OS and to read.
```
ROOT_DIR = Path(__file__).resolve().parents[2]
ANOTHER_DIR = ROOT_DIR/"dir1"/"dir2"

# instead of
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANOTHER_DIR = os.path.join(ROOT_DIR, "dir1")
```

Useful commands:
- `Path()` returns the path of the current working directory.
- `Path().iterdir()` iterdir is a methode that returns a list of all the subfiles and directories from the path object. Can be used in for loops.
- `Path().suffix` and `Path().stem` are 2 useful attributes. Suffix refers to the extension and stem refers to the name.
- `Path().exists()` does what it says.
- `Path().glob("*.json")` or `Path().rglob("*test*)` checks for specific patterns of files under the current directory. The first example checks for JSON files in the current directory and the second examples checks for files containing the word text in the directory **and its sub directories**. Check documentation for optional arguments.
- `Path().mkdir(parents=True, exist_ok=True)` or `Path().touch()` creates a directory for the first example. The argument `parents` is set to True means our path can contain a chain of non existing sub directories.

## Datasets

### NYC Trip Records
This is the taxi trips data that we are going to use for this project. We can find the documentation [here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). This data contains instances of every trip made by cabs with columns like pick up location and time, fees and distance. For the purpose of this project, we are going to download some `parquet` files for a handful of months from 2024.

### NYC Taxi Zones


### APIs
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

## Databases
This project intentionally follows a SQL-first transformation approach. All data transformations are written in SQL while Python is only used for ingesting raw data (CSVs, APIs) and managing database connection and executing scripts. The database used is **PostgreSQL** and the access layer is going to be through the module `sqlalchemy`. We couldve sticked to `psycopg2` but `sqlachemy` provides portability if the back end changes and better integration with `pandas`.

**Note:** `psycopg2` needs to be installed though since `sqlalchemy` is going to need it to interact with our database.