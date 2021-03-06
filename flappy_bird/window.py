import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
__docformat__ = "google"

import pyglet
from bird_population import bird_population
from blocks import blocks
from button import button
import constants
from displayed_texts import menu


class app(pyglet.window.Window):

    def __init__(self) -> None:
        """
        Create the flappy bird window with blocks and bird.

        Args:
            self (undefined):

        Returns:
            None

        """
        super(app, self).__init__()

        self.y_max = self.get_size()[0]
        self.x_max = self.get_size()[1]

        self.set_variables()

        # Draw the background
        self.background_image = pyglet.image.load("./assets/background.png")
        self.background = pyglet.sprite.Sprite(
            self.background_image, x=0, y=-20)
        self.background.scale_y = self.y_max / self.background.height

        # Initialize the Menu
        self.menu = menu(self.x_max/2, self.y_max / 2)
        self.menu_blur_image = pyglet.image.load("./assets/menu_blur.png")
        self.menu_blur = pyglet.sprite.Sprite(
            self.menu_blur_image, x=0, y=-20)

        # Create the Scoretext / Scoreboard
        self.max_score = 0
        self.score_text = pyglet.text.Label('Score : 0',
                                            font_name='Times New Roman',
                                            font_size=25, color=(0, 0, 0, 255),
                                            x=self.x_max * 40/41, y=self.y_max * 2/3)
        self.gen_text = pyglet.text.Label('Gen. : 1',
                                          font_name='Times New Roman',
                                          font_size=25, color=(0, 0, 0, 255),
                                          x=self.x_max * 40/41 + 11, y=self.y_max * 2/3 - 35)
        self.highscore_text = pyglet.text.Label('Highscore : 0',
                                                font_name='Times New Roman',
                                                font_size=25, color=(0, 0, 0, 255),
                                                x=self.x_max * 40/41 - 63, y=self.y_max * 2/3 - 70)
        self.alive_bird_count_text = pyglet.text.Label('Alive Birds : ' + str(constants.BIRD_COUNT),
                                                       font_name='Times New Roman',
                                                       font_size=15, color=(0, 0, 0, 255),
                                                       x=10, y=10)

        # Start a Menu Sequence of the game
        self.birds = bird_population(1, self.x_max, self.y_max)
        # TODO: If the loaded bird is deleted this might cause Problems
        self.birds.load_best_bird()
        pyglet.clock.schedule_interval(self.update_app, constants.GAME_SPEED)

    def start_game(self):
        """
        Function to start a new game.

        Args:
            self (undefined):

        """
        self.started = True
        self.birds = bird_population(
            constants.BIRD_COUNT, self.x_max, self.y_max)
        self.bird_generation = 1
        self.highscore = 0
        self.generations_without_beating_the_highscore = 0

    def set_variables(self):
        """
        Set all the variables:
        - Crate all blocks
        - (Currently not) Create a / all birds
        - Set the starting point of the blocks
        - (WIP) Create a restart buttom, if the game ends
        - A variable if the game has already started

        Args:
            self (undefined):

        """

        self.blocks = blocks(self.y_max, self.x_max)

        self.started = False
        self.block_speed = constants.BLOCK_SPEED
        self.onpause = False

        # self.restart_button = button(self.get_size()[1] / 2 ,self.get_size()[0] / 2, 600, 600)

    def update_app(self, timer):
        """
        Update the app and all the objects in that app:
        - The blocks
        - The bird

        Args:
            self (undefined):
            timer (undefined): The timer of the app.

        """
        self.bird_decisions(timer)

        # Speed up the Blocks / Pipes game over time
        self.block_speed += timer * constants.BLOCK_SPEEDUP

        self.clear()

        self.blocks.update(self.block_speed)

        # [x_bot_left, y_bot_left, x_bot_right, y_bot_right, x_top_right, y_top_right, x_top_left, y_top_left, block_number]
        block_coordinates = self.blocks.nearest_block_coordinates(
            constants.BIRD_X)

        stop_game = self.birds.update(block_coordinates)

        # Check the score
        check = self.birds.check_best_bird()

        # If all birds are dead the game is get restarted and if no bird passed a single pipe a new population of birds is created
        if stop_game and not self.started:  # If the Menu sequence bird died.
            self.restart
        elif stop_game:
            # If the score is 0, create a new population
            if check is None:
                print("No one made it :(")
                self.birds.recreate_population()
            elif self.generations_without_beating_the_highscore > constants.MAX_GENERATIONS_WITHOUT_HIGHSCORE:
                print("For " + str(self.generations_without_beating_the_highscore) +
                      " generatrions no bird broke the highscore. So a new population is created.")
                self.birds.recreate_population()
                self.generations_without_beating_the_highscore = 0
            else:
                best_birds = check[1]
                score = check[0]
                print("The score of the best bird was: " +
                      str(score))
                print("The best bird was number: " + str(best_birds))
                # Update the hight score
                if score > self.highscore:
                    self.highscore = score
                else:
                    self.generations_without_beating_the_highscore += 1
                print("Birds are learning...")
                # If more than one bird made it as far as he got split the next generation up and let them learn from the different birds.
                self.birds.learn(best_birds)
            self.bird_generation += 1

            # Restart the game
            self.restart()

        if check is not None:
            self.max_score = check[0]
        if self.started:
            self.score_text.text = "Score : " + str(self.max_score)
            self.gen_text.text = "Gen. : " + str(self.bird_generation)
            self.highscore_text.text = "Highscore : " + str(self.highscore)
            self.alive_bird_count_text.text = 'Alive Birds : ' + \
                str(self.birds.get_alive_count())

    def bird_decisions(self, timer):
        """
        A explicit function to let the birds decide an and don't do that in every step of the update.

        Args:
            self (undefined):
            timer (undefined):

        """

        # [x_bot_left, y_bot_left, x_bot_right, y_top_right, x_top_right, y_top_right, x_top_left, y_top_left, block_number]
        block_coordinates = self.blocks.nearest_block_coordinates(
            constants.BIRD_X)
        # self.blocks.change_color(block_coordinates[8])

        self.birds.birds_brain_decides(block_coordinates)

    def on_draw(self):
        """
        Draw all the objects in the app:
        - The blocks
        - The bird / birds

        Args:
            self (undefined):

        """
        self.clear()

        self.background.draw()

        self.blocks.draw()

        self.birds.draw()

        # Draw all of the text
        if not self.started:
            self.menu_blur.draw()
            self.menu.draw()
        else:
            self.score_text.draw()
            self.gen_text.draw()
            self.highscore_text.draw()
            self.alive_bird_count_text.draw()

    def pause(self):
        """
        Pause the game and:
        - (WIP) Draw the restart buttom to restart the game.

        Args:
            self (undefined):

        """
        # self.restart_button.draw()

        pyglet.clock.unschedule(self.update_app)
        self.started = False
        # pyglet.clock.unschedule(self.bird_decisions)

    def unpause(self):
        """
        Onpause the game

        Args:
            self (undefined):

        """
        pyglet.clock.schedule_interval(self.update_app, constants.GAME_SPEED)
        self.started = True

    def restart(self):
        """
        Restart the whole game.

        Args:
            self (undefined):

        """
        # First pause the game. FIXME: If the game is already stopped, this could lead to errors in the future.
        self.pause()

        self.set_variables()

        self.blocks = blocks(self.y_max, self.x_max)

        self.started = True
        self.max_score = 0

        self.birds.revive_population()

        print("Restarting with a new generation. \n")
        pyglet.clock.schedule_interval(self.update_app, constants.GAME_SPEED)
        # pyglet.clock.schedule_interval(self.bird_decisions, constants.NN_DECISION_SPEED)

    def on_key_press(self, symbol, modifiers):
        """
        The function to check keyboard inputs and react to them.

        Args:
            self (undefined):
            symbol (undefined):
            modifiers (undefined):

        """
        if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.SPACE:
            if not self.started:
                self.start_game()
                self.restart()
                #pyglet.clock.schedule_interval(self.bird_decisions, constants.NN_DECISION_SPEED)
            # self.birds[1].move_up()
        if symbol == pyglet.window.key.RIGHT:
            if self.started:
                print("Lets go faster!")
                pyglet.clock.schedule_interval(
                    self.update_app, constants.GAME_SPEED)

        if symbol == pyglet.window.key.S:
            self.birds.save_best_bird()

        if symbol == pyglet.window.key.L:
            self.birds.load_best_bird()

        if symbol == pyglet.window.key.ESCAPE:
            self.close()

        if symbol == pyglet.window.key.P:
            if self.started:
                self.pause()
                self.onpause = True
            elif not self.started and self.onpause:
                self.unpause()
                self.onpause = False
