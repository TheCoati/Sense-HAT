from sense_hat import SenseHat
import threading
import time
import random

MAX_WIDTH = 8
MAX_HEIGHT = 8

snake_coords = [
    [3, 5],
    [3, 6],
    [3, 7],
]
food_coords = [0, 0]
last_input = 'up'

sense = SenseHat()


def generate_food():
    global food_coords

    def regenerate():
        return [
            random.randint(0, MAX_WIDTH - 1),
            random.randint(0, MAX_HEIGHT - 1)
        ]

    coords = regenerate()

    while coords in snake_coords:
        coords = regenerate()

    food_coords = coords


def main_loop():
    sense.clear()
    generate_food()

    while True:
        x = snake_coords[0][0]
        y = snake_coords[0][1]

        if last_input == 'up':
            y -= 1

        if last_input == 'down':
            y += 1

        if last_input == 'right':
            x += 1

        if last_input == 'left':
            x -= 1

        if y > MAX_HEIGHT - 1:
            y = 0

        if y < 0:
            y = MAX_HEIGHT - 1

        if x > MAX_WIDTH - 1:
            x = 0

        if x < 0:
            x = MAX_WIDTH - 1

        print(snake_coords)
        print([x, y])

        if [x, y] in snake_coords:
            print('Game Over!')
            return

        snake_coords.insert(0, [x, y])

        if snake_coords[0] == food_coords:
            generate_food()
        else:
            snake_coords.pop()

        sense.clear()

        # Update snake position
        for coords in snake_coords:
            sense.set_pixel(coords[0], coords[1], (0, 0, 255))

        sense.set_pixel(food_coords[0], food_coords[1], (0, 255, 0))

        time.sleep(1)


def input_loop():
    global last_input

    while True:
        for event in sense.stick.get_events():
            if event.action == 'pressed':
                last_input = event.direction


main_thread = threading.Thread(target=main_loop).start()
input_thread = threading.Thread(target=input_loop).start()

for thread in threading.enumerate():
    # Skip joining the main thread
    if thread == threading.current_thread():
        continue
    thread.join()
