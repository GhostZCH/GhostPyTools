
class Dish:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Cook:
    def __init__(self, name, dish_name):
        self.name = name
        self.dish_name = dish_name

    def get_name(self):
        return self.name

    def get_dish(self):
        return Dish(self.dish_name)


class Kitchen:
    dish_name = [u'xxx', u'yyy']

    def __init__(self):
        self.cook = {}
        self.init_cook()

    def init_cook(self):
        for i in Kitchen.dish_name:
            cook = Cook('cook'+str(i), i)
            self.cook[i] = cook

    def get_cook(self, dish_name):
        return self.cook[dish_name]


class Server:
    def __init__(self):
        pass

    def sent(self, dish):
        print('send %s food to customer' % dish.get_name())

class FrontDesk:
    def __init__(self, manager):
        self.manager = manager

    def order(self, dish):
        self.manager.order(dish)

class Manager:
    def __init__(self, restaurant):
        self.restaurant = restaurant

    def order(self, dish_name):
        dish = self.restaurant.kitchen.get_cook(dish_name).get_dish()
        self.restaurant.server.sent(dish)

# Ӎڝ
class Restaurant:
    def __init__(self):
        self.manager = Manager(self)
        self.kitchen = Kitchen()
        self.server = Server()
        self.front = FrontDesk(self.manager)


if __name__ == '__main__':
    front_desk = Restaurant().front
    front_desk.order(u'xxx')