# hw8_mongoDB

#  docker run --name redis-cache -d -p 6379:6379 redis

# Quote Search Application

## Overview

This Python application allows you to search for quotes by author or tags. It uses MongoDB for storing and retrieving quotes and authors, and Redis for caching search results. The application provides a command-line interface for interacting with the data.

## Features

- Search quotes by author name.
- Search quotes by tags.
- Results are cached using Redis to improve performance.

## Requirements

- Python 3.11+
- MongoDB
- Redis

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up MongoDB and Redis:**

   Ensure that MongoDB and Redis are running. You may need to configure your connection settings in the `connect` module if they are not running locally or if credentials are required.

## Usage

1. **Run the application:**

    ```bash
    python search_quotes.py
    ```

2. **Enter a search query:**

    The application accepts queries in the format:

    ```
    key:value
    ```

    - To search by author: `name:author_name`
    - To search by tags: `tags:tag1,tag2,...`
    - To search by one tag: `tag:tag1`
    - To search by first letters of author name or tags `name:au`, `tags:ta,ta,...`, `tag:ta`

    Example queries:
    - `name:Steve Martin`, `name:st`
    - `tags:inspiration,life`, `tags:li,hu`
    - `tag:life`, `tag:li`

3. **Exit the application:**

    Type `exit` to terminate the program.

## Code Explanation

- **`search_by_author(name: str)`**: Searches for quotes by a given author's name using a regular expression pattern.
- **`search_by_tags(tags: str)`**: Searches for quotes containing any of the specified tags using regular expression patterns.
- **`search(search_query: str)`**: Parses the search query and delegates the search operation to the appropriate function based on the key (`name` or `tags`). Caching is applied to improve performance.
- **`if __name__ == '__main__':`**: Runs the application in a loop, accepting user input and displaying search results. Handles exceptions and provides a way to exit the program gracefully.

## Troubleshooting

- **Authentication Errors**: Ensure that MongoDB and Redis are correctly configured and running.
- **Value Errors**: Check that the search query is in the correct format.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

