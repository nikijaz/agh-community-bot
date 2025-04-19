# AGH Community Bot

Telegram bot designed for the AGH University of Science and Technology community. Features captcha verification to
prevent spam and anecdote sending to keep the community engaged.

## Installation

0. Ensure [Docker](https://docs.docker.com/engine/install/) and
   [Docker Compose](https://docs.docker.com/compose/install/) are installed.
1. Clone and navigate to the repository:

    ```shell
    git clone https://github.com/nikijaz/agh-community-bot.git
    cd agh-community-bot/
    ```

2. Create `.env` file with your configuration. You can use `.env.template` as a template.
3. Create `anecdotes.txt` file with anecdotes, each on a new line.
4. Run detached Docker container in production mode:

    ```shell
    docker compose --profile prod up -d
    ```

## Development

0. Ensure [Docker](https://docs.docker.com/engine/install/), [Docker Compose](https://docs.docker.com/compose/install/)
   and [uv](https://docs.astral.sh/uv/getting-started/installation/) are installed.
1. Clone and navigate to the repository:

    ```shell
    git clone https://github.com/nikijaz/agh-community-bot.git
    cd agh-community-bot/
    ```

2. Create `.env` file with your configuration. You can use `.env.template` as a template.
3. Create `anecdotes.txt` file with anecdotes, each on a new line.

4. Install dependencies:

    ```shell
    uv sync
    ```

5. Make changes to the code.
6. Run detached Docker container in development mode (this will start only the PostgreSQL service):

    ```shell
    docker compose --profile dev up -d
    ```

7. Verify your changes by running the bot:

    ```shell
    uv run main.py
    ```

8. Check for any typing, linting or formatting issues:

    ```shell
    mypy .
    ruff check .
    ruff format --check .
    ```

## Technologies Used

**Python** powers the bot's logic, with **uv** as the package manager. The bot uses the **Telethon** library for
Telegram API communication. **PostgreSQL** serves as the database, with **SQLAlchemy** for ORM. **Docker** is used for
containerization.
