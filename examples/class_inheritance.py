class Animal:

    def show(self):
        print('Animal')

    def pee(self):
        print('Pee')


class Dog(Animal):
    def show(self):
        # super().show()
        print('Dog')



animal = Dog()
animal.show()
animal.pee()
