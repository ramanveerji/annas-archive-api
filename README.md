# Anna's Archive API

An unofficial API for the [Anna's Archive](https://annas-archive.org)
website made in python with coffee :)

Feel free to contribute here with code and relating problems or
just making a suggestion.


## Routes

### `/`: Get recommendations
  - Description: Get the recommendations from homepage of the website
  - Parameters: Don't need
  - Returns: A list of [Recommendations](api/extractors/home.py#L9)

### `/search`: Search for contents
  - Description: Search using filters and with a selectable sort
  - Parameters:
    - q: Query to search(required)
    - lang: Language code
    - ext: File extension
    - sort: Sort order to be used(see the valid values [here](api/extractors/search.py#L9))
  - Returns: A list of [Result](api/extractors/search.py#L44)


### `/download`: Get content information
  - Description: Get file information like the basic information, book description, and other file information
  - Parameters:
    - `path`: The URL path to the content(required)
  - Returns: [Download](api/extractors/download.py#L17)


# Building

You can build this project upside of your docker environment or in your host
system(here I will teach you to do it on Linux)

First clone the respository:
```bash
git clone https://github.com/dheison0/annas-archive-api
cd annas-archive-api
```

**For Docker:**
```bash
docker build -t annas-api .
docker run -d --name annas-api -e 1337:8080 annas-api:latest
```

**On host:**
```bash
sudo apt install python-poetry # Install poetry
poetry install
export PORT=8090
poetry run python run.py
```