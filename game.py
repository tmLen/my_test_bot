import json
#Класс хранит состояние игры в города, есть методы для того чтобы делать ходы
class Game:
    def __init__(self):
        with open('cities.json', 'r', encoding='utf-8') as fin:
            self.cities = json.load(fin)
        self.used_cities = []
        self.prev_city = 'Москва'
        self.player_turn = True


    def use_city(self, city):
        self.used_cities.append(city)
        self.cities.remove(city)
        self.prev_city = city

    def try_city(self, city):
        city = city.lower()
        prev_city = self.prev_city
        if prev_city[-1] in ['ь','ы','ъ']:
            prev_city = prev_city[:-1]
        if city[0] != prev_city[-1]:
            return f'Город должен начинаться на букву {self.prev_city[-1]}'
        elif city in self.used_cities:
            return f'Такой город уже был'
        elif city not in self.cities:
            return f'Такого города я не знаю'
        
        else:
            self.use_city(city)
            self.player_turn = not self.player_turn
            return city

    def bot_turn(self):
        prev_city = self.prev_city
        if prev_city[-1] in ['ь','ы','ъ']:
            prev_city = prev_city[:-1]
        for city in self.cities:
            if city[0] == prev_city[-1]:
                return self.try_city(city).capitalize()
                break
        return 'Я сдаюсь!'
