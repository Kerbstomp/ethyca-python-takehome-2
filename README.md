# Noughts & Crosses

Noughts and Crosses (British English), Tic-tac-toe (American English) is a game for two players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their marks in a diagonal, horizontal, or vertical row is the winner

Project Details can be found [here](https://github.com/ethyca/python-takehome-2)

This project was built using the [FastAPI](https://fastapi.tiangolo.com/) python web framework

## Quick Start

### Minimum requirements

* [Python](https://www.python.org/downloads/) (3.10+)

### Build

> [!TIP]
> It is recommend to set up a Python virtual environment such as `venv` to install the dependencies into

Run the following command to get started:

```sh
pip install -r requirements.txt
```

### Run

Run the following command to start the application:

```sh
uvicorn app.main:app
```

The application will now be running on `http://127.0.0.1:8000`

To view the REST API documentation navigate to: 
 - `http://127.0.0.1:8000/docs` (for swagger)
 - `http://127.0.0.1:8000/redoc` (for redoc)

## Delivery

Time taken to complete: 3.5 hours

### Assumptions & Tradeoffs

 - Data on games is not persisted between application runs
 - No authentication required to hit API
 - No pagination in list endpoints
 - Player symbols are not selectable, user player is always denoted to symbol 'X'
 - ~~No~~ Very little unit tests 🙃

### Extra features

 - List all games endpoint supports the `order` query param that allows for sorting the results by the created at date/time, asceding (default) or descending
 - Endpoint added to allow for forfeiting an existing game
 - Built out and published a [Postman](https://www.postman.com/) collection for testing the API
 - Added some simple GitHub actions for CI tools

### Feedback

I quite enjoyed this project! I am a big propenent of these kinds of technical assesments over doing live coding just solving random leet code type problems. This type of assesment is much more applicable to the work I normally do (and would be doing in this role), and is much more fun to work on 😄
