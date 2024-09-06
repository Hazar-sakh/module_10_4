from tabnanny import check
from time import sleep
from threading import Thread
from queue import Queue
from random import randint

guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman', 'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya',
    'Alexandra']


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for j in guests:
            for i in self.tables:
                if i.guest is None:
                    i.guest = j
                    print(f'{i.guest.name} сел(-а) за стол номер {i.number}')
                    j.start()
                    break
                elif i.guest is not None and i != self.tables[-1]:
                    continue
                else:
                    self.queue.put(j)
                    print(f'{j.name} в очереди')
                    break
            continue


    def discuss_guests(self):
        while not self.queue.empty():
            for i in self.tables:
                if i.guest.is_alive():
                    i.guest.join()
                    continue
                print (f'{i.guest.name} покушал(-а) и ушёл(ушла)\nСтол номер {i.number} свободен')
                i.guest = None
                if not self.queue.empty():
                    next_guest = self.queue.get()
                    i.guest = next_guest
                    next_guest.start()
                    print(f'{i.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {i.number}')




guests = [Guest(name) for name in guests_names]

tables = [Table(number) for number in range(1, 6)]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()