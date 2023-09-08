# Anna's Archive API

An unofficial API for the [Anna's Archive](https://annas-archive.org)
website made in python with coffee :)

Feel free to contribute here with code and relating problems or
just making a suggestion.

## Routes

**`/recents`: Get recent downloads**

- Description: Get recent downloaded books from others users.
- Parameters: Don't need.
- Returns: A list of [RecentDownload](api/models/response.py#L12)

**`/search`: Search for contents**

- Description: Search using filters
- Parameters:
  - `q`: Query to search(required)
  - `lang`: [Language code](api/models/args.py#L36)
  - `ext`: [File extension](api/models/args.py#L12)
  - `sort`: [Sort order to be used](api/models/args.py#L4)
- Returns: A list of [SearchResult](api/models/response.py#L24)

**`/download`: Get content information**

- Description: Get file information like the basic information, book description, and other file information
- Parameters:
  - `path`: The URL path to the content(required)
- Returns: [Download](api/models/response.py#L35)

## Building

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
sudo apt install python3-poetry # Install poetry
poetry install
export PORT=8090
poetry run python run.py
```
