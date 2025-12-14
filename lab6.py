import os
import logging
import functools

class FileNotFound(Exception):
    """
    Exception raised when the specified file path does not exist.
    """
    pass

class FileCorrupted(Exception):
    """
    Exception raised when an input/output operation on the file fails
    (e.g., reading, writing, or permissions issues).
    """
    pass


def get_logger(mode):
    logger = logging.getLogger("file_logger")

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    if mode == "console":
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler("file_operations.log", encoding="utf-8")

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def logged(exception_types, mode=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_mode = mode if mode else LOG_MODE
            logger = get_logger(current_mode)

            try:
                result = func(*args, **kwargs)
                logger.info(f"Операція {func.__name__} виконана успішно.")
                return result
            except exception_types as e:
                logger.error(f"Помилка у {func.__name__}: {e}")
                raise
        return wrapper
    return decorator


class TextFileManager:
    """
    A class to manage basic text file operations such as reading, 
    writing, and appending content.
    
    Attributes:
        path (str): The absolute path to the text file.
    """

    @logged((FileNotFound, ValueError))
    def __init__(self, path):
        self.path = os.path.abspath(path)

        if not os.path.exists(self.path):
            raise FileNotFound("Файл не знайдено.")

        if not self.path.endswith(".txt"):
            raise ValueError("Потрібен текстовий файл з розширенням .txt")

    @logged(FileCorrupted)
    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            raise FileCorrupted("Неможливо прочитати файл")

    @logged(FileCorrupted)
    def write(self, text):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            raise FileCorrupted("Неможливо записати у файл")

    @logged(FileCorrupted)
    def append(self, text):
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            raise FileCorrupted("Неможливо дописати у файл")


if __name__ == "__main__":

    LOG_MODE = input("Виберіть режим логування (console/file): ").strip().lower()
    if LOG_MODE not in ("console", "file"):
        LOG_MODE = "console"

    file_path = input("\nВведіть шлях до текстового файлу: ")

    try:
        fh = TextFileManager(file_path)
    except Exception as e:
        print("Помилка:", e)
        exit()

    while True:
        print("\n========== МЕНЮ ==========")
        print("1 — Прочитати файл")
        print("2 — Перезаписати файл")
        print("3 — Дописати до файлу")
        print("4 — Вийти")
        print("==========================")

        choice = input("Ваш вибір: ")

        if choice == "1":
            try:
                content = fh.read()
                print("\n=== ВМІСТ ФАЙЛУ ===")
                print(content if content else "(Файл порожній)")
            except Exception as e:
                print("Помилка:", e)

        elif choice == "2":
            new_text = input("Введіть новий текст: ")
            try:
                fh.write(new_text + "\n")
                print("Файл перезаписано.")
            except Exception as e:
                print("Помилка:", e)

        elif choice == "3":
            add_text = input("Введіть текст для дописування: ")
            try:
                fh.append(add_text + "\n")
                print("Текст дописано.")
            except Exception as e:
                print("Помилка:", e)

        elif choice == "4":
            break

        else:
            print("Неправильний вибір, число має бути від 1 до 4")