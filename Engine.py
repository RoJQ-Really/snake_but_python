import copy
import random
import time
import os
import keyboard


class DevActions:
    def __init__(self):
        pass

    @staticmethod
    def add_to_log(message: str, encoding: str = "utf-8"):
        """
        Записывает данные в лог файл. Построчно (экранирование работает [\n, \r, \b])
        :param message:  сообщение записываемое в лог
        :param encoding: кодировака
        :return:
        """
        with open(file = Settings.LOG_FILE, mode="a+", encoding=encoding) as log_file:
            log_file.write(message + "\n")


class Settings:
    EXTENSION_FOR_FILES = ".rqfile"
    LOG_FILE = "log" + EXTENSION_FOR_FILES


class Snake:
    def __init__(self):
        self.direction_x = 1
        self.direction_y = 0
        self.__head = [9, 4]
        self.snake_skin = "@"
        self.speed_x = 1*self.direction_x
        self.speed_y = 1*self.direction_y
        self.__size = 5
        self.__snake_cords = self.__create_snake()
        keyboard.hook_key(key="w", callback=self.up)
        keyboard.hook_key(key="s", callback=self.down)
        keyboard.hook_key(key="a", callback=self.left)
        keyboard.hook_key(key="d", callback=self.right)

    def __redefine_speed(self):
        self.speed_y = 1*self.direction_y
        self.speed_x = 1*self.direction_x

    def up(self, *args):
        if self.direction_y != 1:
            self.direction_x = 0
            self.direction_y = -1
            self.__redefine_speed()

    def down(self, *args):
        if self.direction_y != -1:
            self.direction_x = 0
            self.direction_y = 1
            self.__redefine_speed()

    def right(self, *args):
        if self.direction_x != -1:
            self.direction_y = 0
            self.direction_x = 1
            self.__redefine_speed()

    def left(self, *args):
        if self.direction_x != 1:
            self.direction_y = 0
            self.direction_x = -1
            self.__redefine_speed()

    def __create_snake(self):
        snake_cords = []
        for i in range(self.get_size()):
            snake_cords.append([self.__head[0] - i, self.y_head()])
        return snake_cords

    def update(self):
        pixel = [self.x_head() + self.speed_x, self.y_head() + self.speed_y]
        self.__snake_cords.insert(0, pixel)
        self.__snake_cords.pop(len(self.__snake_cords) - 1)
        self.__head = pixel

    def add_size(self):
        if self.__snake_cords[-1][0] == self.__snake_cords[-2][0]:
            self.__snake_cords.append([self.__snake_cords[-1][0], self.__snake_cords[-1][1] + self.speed_y])
        else:
            self.__snake_cords.append([self.__snake_cords[-1][0] + self.speed_x, self.__snake_cords[-1][1]])
        self.__size += 1

    def x_head(self) -> int:
        return self.__head[0]

    def y_head(self) -> int:
        return self.__head[1]

    def get_head_cords(self) -> list[int, int]:
        return self.__head

    def get_size(self) -> int:

        return self.__size

    def get_snake(self) -> list:
        return self.__snake_cords


class Game:
    def __init__(self):
        self._rand = random.Random()
        self._dev = DevActions()
        self.color = "0"
        self.apple_skin = "%"
        self.width = 32
        self.height = 10
        self.count = -1
        self.frame_update = None
        self.snake = Snake()
        self.apple = self.snake.get_head_cords()
        self._origin_width_line = []
        self.iter_per_second = 10
        self.__iter_order = 0
        self.sleep_time = 1/self.iter_per_second
        self._map = []
        self.game = True
        self.pre_init()

    def pre_init(self):
        now_time = time.gmtime()
        time_str = f"////{now_time.tm_mday}-{now_time.tm_mon}, {now_time.tm_hour+5}:{now_time.tm_min}////"
        self._dev.add_to_log(time_str)

    def create_point(self):
        apple = [-1, -1]
        apple[0] = self._rand.randint(0, self.width-1)
        apple[1] = self._rand.randint(0, self.height-1)
        return apple

    def init_map(self):
        self._map = []
        for j in range(self.width):
            self._origin_width_line.append(self.color)
        for i in range(self.height):
            self._map.append(self._origin_width_line)

    def update_map(self):
        if not((0 <= self.snake.x_head() <= self.width - 1) and (0 <= self.snake.y_head() <= self.height - 1)) or self.snake.get_head_cords() in self.snake.get_snake()[1:-1]:
            self.death()
        map_cycle = copy.deepcopy(self._map)

        if self.snake.get_head_cords() == self.apple:
            self.count += 1
            self.apple = self.create_point()
            self.snake.add_size()
        y_layer = copy.deepcopy(map_cycle[self.apple[1]])
        y_layer[self.apple[0]] = self.apple_skin
        map_cycle[self.apple[1]] = y_layer
        print(f"{self.snake.get_head_cords()}, Счёт = {self.count}, size = {self.snake.get_size()}")

        for i in self.snake.get_snake():
            i: list
            y = i[1]
            x = i[0]
            y_layer = copy.deepcopy(map_cycle[y])
            y_layer[x] = self.snake.snake_skin
            map_cycle[y] = y_layer
        self.snake.update()
        return map_cycle

    def death(self):
        self.game = False
        os.system("cls")
        print("Вы проиграли")
        self._dev.add_to_log("////Конец игры////")
        time.sleep(0.5)
        exit()

    def __service_processing(self):  # Служебна обработка цикла
        self.__iter_order += 1
        if self.__iter_order == self.iter_per_second + 1:
            self.__iter_order = 1
        mess_1 = f"Итерация#{self.__iter_order} \n"
        mess_2 = f"snake_info:\n" \
                 f"size = {self.snake.get_size()}, \n" \
                 f"head_coord = ({self.snake.get_head_cords()})"
        self._dev.add_to_log(f"{mess_1} {mess_2}")

    def main_loop(self, game_loop=True):
        self.game = game_loop
        while self.game:
            u_map = self.update_map()
            for i in u_map:
                print("".join(i))
            # service_dev
            self.__service_processing()
            # -e
            time.sleep(self.sleep_time)
            os.system("cls")


if __name__ == '__main__':
    game = Game()
    game.init_map()
    game.main_loop()
