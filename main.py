import pygame
import random

# Переменные цветов для отрисовки экрана, кораблей и сетки
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Переменные для масштабации основного экрана
block_size = 50
left_margin = 100
upper_margin = 80
size = (left_margin + 30 * block_size , upper_margin + 15 * block_size)

# Иницилизируем pygame
pygame.init()

# Задаем поверхность для отрисовки полей
screen = pygame.display.set_mode(size)

# Задаем название для окна
pygame.display.set_caption('Морской бой')

# Задаем размер и вид шрифта
font_size = int(block_size / 1.5)
font = pygame.font.SysFont('Arial', font_size)


# Класс для кораблей
class ShipsOnGrid():
    def __init__(self):
        self.available_blocks = set((a, b)
                                    for a in range(1, 11) for b in range(1, 11))
        self.ships_set = set()
        self.ships = self.populate_grid()

    def create_start_block(self, available_blocks):
        x_or_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, x_or_y, str_rev

    # Отвечает
    def create_ship(self, numbers_of_blocks, available_blocks):
        ship_coordinates = []
        x, y, x_or_y, str_rev = self.create_start_block(available_blocks)
        for _ in range(numbers_of_blocks):
            ship_coordinates.append((x, y))
            if not x_or_y:
                str_rev, x = self.add_block_to_ship(x, str_rev, x_or_y, ship_coordinates)
            else:
                str_rev, y = self.add_block_to_ship(x, str_rev, x_or_y, ship_coordinates)

        if self.ship_is_valid(ship_coordinates):
            return ship_coordinates
        return self.create_ship(numbers_of_blocks, available_blocks)

    def add_block_to_ship(self, coor, str_rev, x_or_y, ship_coordinates):
        if (coor <= 1 and str_rev == -1) or (coor >= 10 and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coordinates[0][x_or_y] + str_rev
        else:
            return str_rev, ship_coordinates[-1][x_or_y] + str_rev

    def ship_is_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def add_new_ship_to_set(self, new_ship):
        for elem in new_ship:
            self.ships_set.add(elem)

    def update_available_blocks_for_create_ships(self, new_ship):
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if 0 < (elem[0] + k) < 11 and 0 < (elem[1] + m) < 11:
                        self.available_blocks.discard((elem[0] + k, elem[1] + m))

    def populate_grid(self):
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5 - number_of_blocks):
                new_ship = self.create_ship(number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.add_new_ship_to_set(new_ship)
                self.update_available_blocks_for_create_ships(new_ship)
        return ships_coordinates_list


computer = ShipsOnGrid()
human = ShipsOnGrid()


# Рисуем коробли
def draw_ships(ship_coordinates_list):
    for elem in ship_coordinates_list:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # Рисуем вертикальные корабли
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width = block_size
            ship_height = block_size * len(ship)
        # Рисуем горизонтальные и одноклеточные корабли
        else:
            ship_width = block_size * len(ship)
            ship_height = block_size
        x = block_size * (x_start - 1) + left_margin
        y = block_size * (y_start - 1) + upper_margin
        if ship_coordinates_list == human.ships:
            x += 15 * block_size
        pygame.draw.rect(screen, BLACK, ((x, y,), (ship_width, ship_height)), width=block_size // 10)


# Рисуем поле
def draw_grid():
    letters = ['A', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
    for i in range(11):
        # Горизонтальные линии 1 поле
        pygame.draw.line(screen, BLACK, (left_margin, upper_margin + i * block_size),
                         (left_margin + 10 * block_size, upper_margin + i * block_size), 1)
        # Горизонтальные линии 2 поле
        pygame.draw.line(screen, BLACK, (left_margin + 15 * block_size, upper_margin + i * block_size),
                         (left_margin + 25 * block_size, upper_margin + i * block_size), 1)
        # Вертикальные  линии 1 поле
        pygame.draw.line(screen, BLACK, (left_margin + i * block_size, upper_margin),
                         (left_margin + i * block_size, upper_margin + 10 * block_size), 1)
        # Вертикальные  линии 2 поле
        pygame.draw.line(screen, BLACK, (left_margin + i * block_size + 15 * block_size, upper_margin),
                         (left_margin + i * block_size + 15 * block_size, upper_margin + 10 * block_size), 1)
        if i < 10:
            numbers_vr = font.render(str(i + 1), True, BLACK)
            letters_hr = font.render(letters[i], True, BLACK)

            numbers_vr_width = numbers_vr.get_width()
            numbers_vr_height = numbers_vr.get_height()
            letters_hr_width = letters_hr.get_width()

            # Отображение номеров яччеек 1 поля
            screen.blit(numbers_vr, (left_margin - (block_size // 2 + numbers_vr_width // 2),
                                     upper_margin + i * block_size + (block_size // 2 - numbers_vr_height // 2)))
            # Отображение букв яччеек 1 поля
            screen.blit(letters_hr, (left_margin + i * block_size + (block_size // 2 - letters_hr_width // 2),
                                     upper_margin + 10 * block_size + block_size // 4))
            # Отображение номеров яччеек 2 поля
            screen.blit(numbers_vr, (left_margin - (block_size // 2 + numbers_vr_width // 2) + 15 * block_size,
                                     upper_margin + i * block_size + (block_size // 2 - numbers_vr_height // 2)))
            # Отображение букв яччеек 2 поля
            screen.blit(letters_hr,
                        (left_margin + i * block_size + 15 * block_size + (block_size // 2 - letters_hr_width // 2),
                         upper_margin + block_size // 4 + 10 * block_size))


# Основная функция работы игры
def main():
    game_over = False
    # Заливка экрана
    screen.fill(WHITE)
    draw_grid()
    draw_ships(computer.ships)
    draw_ships(human.ships)
    pygame.display.update()

    while not game_over:
        # выход из игры по закрытию приложения
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True


main()

pygame.QUIT

