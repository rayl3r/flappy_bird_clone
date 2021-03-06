# Flappy Bird

The popular game Flappy Bird played by a Neural Network with evolution.

## Dependencies

- All python dependencies are managed with [poetry](https://python-poetry.org/), this should be installed first.
- It is recommended to use [git](https://git-scm.com/). Especially if you want to development.

## Run the game

- Clone the Repository

    ```Shell
    git clone https://github.com/rayl3r/flappy_bird_clone.git
    ```

- Move into the project folder

    ```Shell
    cd flappy_bird_clone
    ```

- Install the python dependencies

    ```Shell
    poetry install
    ```

- Run the code

    ```Shell
    poetry run python ./flappy_bird/main.py
    ```

- To update the dependencies run

    ```Shell
    poetry update
    ```

- Start the game with the up arrow key &uarr; or the spacebar. To speed up use the right arrow &rarr;.
- Load the example best bird with L and save your own best bird with S and override the sample best bird.

## Documentation

You can find the documentation of the code [here](https://rayl3r.github.io/flappy_bird_clone/).

But that documentation might not be up-to-date so it is advised to build you own documentation running the command:

    poetry run pdoc --math flappy_bird

Or run the "documentation" [task using VS Code](https://code.visualstudio.com/Docs/editor/tasks).
