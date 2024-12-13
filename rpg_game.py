import tkinter as tk
from tkinter import simpledialog, messagebox
import logging

# Настройка логирования с указанием кодировки
logging.basicConfig(
    filename='game_log.txt',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Кодировка
)


class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Аркадная текстовая RPG-игра")
        self.player = Player()
        self.current_scene = None

        self.text_area = tk.Text(master, height=15, width=50)
        self.text_area.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()
        self.entry.bind("<Return>", self.process_input)

        self.start_game()

    def start_game(self):
        self.player = Player()  # Создаем нового игрока
        self.player.name = self.get_player_name()
        logging.info(f"Игрок {self.player.name} начал игру.")  # Логируем имя игрока
        self.current_scene = Scene1(self)  # Создаем новую сцену
        self.update_text_area()

    def get_player_name(self):
        name = simpledialog.askstring("Имя игрока", "Введите ваше имя:")
        if name:
            logging.info(f"Игрок ввел имя: {name}")  # Логируем введенное имя
            return name
        else:
            logging.info("Игрок не ввел имя, используется значение по умолчанию.")
            return "Игрок"

    def update_text_area(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.current_scene.description)
        logging.info(f"Текущая сцена: {self.current_scene.description}")

    def process_input(self, event):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)
        logging.info(f"Игрок ввел: {user_input}")
        next_scene = self.current_scene.next_scene(user_input)
        if next_scene is not None:
            self.current_scene = next_scene
            self.update_text_area()


class Player:
    def __init__(self):
        self.name = ""
        self.score = 0


class Scene:
    def __init__(self, game, description):
        self.game = game
        self.description = description

    def next_scene(self, user_input):
        raise NotImplementedError("Метод next_scene должен быть переопределен в подклассе.")


class Scene1(Scene):
    def __init__(self, game):
        super().__init__(game, "Вы находитесь в темном лесу.\n1. Исследовать лес.\n2. Вернуться в деревню.")

    def next_scene(self, user_input):
        if user_input == "1":
            logging.info("Игрок выбрал: Исследовать лес.")
            return Scene2(self.game)
        elif user_input == "2":
            logging.info("Игрок выбрал: Вернуться в деревню.")
            return Scene3(self.game)
        else:
            messagebox.showerror("Ошибка", "Неверный выбор. Попробуйте снова.")
            logging.error("Ошибка: Неверный выбор в Scene1.")
            return self


class Scene2(Scene):
    def __init__(self, game):
        super().__init__(game,
                         "Вы решили исследовать лес.\nВнезапно вы встречаете диких животных!\n1. Сразиться с ними.\n2. Убежать.")

    def next_scene(self, user_input):
        if user_input == "1":
            self.game.player.score += 2
            logging.info(f"Игрок сразился с дикими животными. Очки: {self.game.player.score}")
            return SceneEnd(self.game, "Вы сражаетесь с дикими животными и побеждаете!")
        elif user_input == "2":
            self.game.player.score += 1
            logging.info(f"Игрок убегает от диких животных. Очки: {self.game.player.score}")
            return SceneEnd(self.game, "Вы убегаете и спасаетесь.")
        else:
            messagebox.showerror("Ошибка", "Неверный выбор. Попробуйте снова.")
            logging.error("Ошибка: Неверный выбор в Scene2.")
            return self

class Scene3(Scene):
    def __init__(self, game):
        super().__init__(game, "Вы вернулись в деревню.\nЗдесь вы можете отдохнуть и восстановить силы.\n1. Отдохнуть.\n2. Исследовать окрестности.")

    def next_scene(self, user_input):
        if user_input == "1":
            self.game.player.score += 1
            logging.info(f"Игрок отдохнул. Очки: {self.game.player.score}")
            return SceneEnd(self.game, "Вы отдохнули и восстановили силы.")
        elif user_input == "2":
            logging.info("Игрок решил исследовать окрестности.")
            return Scene2(self.game)
        else:
            messagebox.showerror("Ошибка", "Неверный выбор. Попробуйте снова.")
            logging.error("Ошибка: Неверный выбор в Scene3.")
            return self

class SceneEnd(Scene):
    def __init__(self, game, ending_text):
        super().__init__(game, ending_text + f"\nВаши очки: {game.player.score}\n\nХотите сыграть еще раз? (да/нет)")

    def next_scene(self, user_input):
        if user_input.lower() == "да":
            logging.info("Игрок решил сыграть еще раз.")
            self.game.start_game()  # Перезапускаем игру
            return None  # Возвращаем None, чтобы не пытаться обновить текстовую область
        elif user_input.lower() == "нет":
            logging.info("Игрок завершил игру.")
            self.game.master.quit()
        else:
            messagebox.showerror("Ошибка", "Неверный выбор. Попробуйте снова.")
            logging.error("Ошибка: Неверный выбор в SceneEnd.")
            return self

# Основной код для запуска игры
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()