# TODO: сделать общий интерфейс для бара
class ProgressBar:

    __PROGRESS_CHAR = '▓'
    __EMPTY_CHAR = '░'
    __MAX_VALUE = 100

    def __init__(self, current_progress: int, description: str):
        self.current_progress = current_progress
        print(description, end=" ")

    def print_progress(self, time: float, max_time: float):
        delta_for_progress = int(100 * time / max_time) - self.current_progress
        if delta_for_progress > 0:
            self.current_progress += delta_for_progress
            self.__print(self.current_progress)

    def __print(self, value):
        line = self.__PROGRESS_CHAR * value + self.__EMPTY_CHAR * (self.__MAX_VALUE - value)
        print('\r' + line, end='')
