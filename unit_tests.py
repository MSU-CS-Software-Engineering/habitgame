import unittest
from types import *

from engine import *
#from work_space import ...
#from generic_list import ...
#from landing_page import ...
#from authenticate import ...
#from shop import ...
#from file_parser import ...

class characterTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.testCharacter = Character("Tom")

        self.habit_1 = Habit('Read More', 'Read more books', 50, 10, 'habit', 0)
        self.habit_2 = Habit('Veggies', 'Eat more veggies', 100, 15, 'habit', 1)
        self.habit_3 = Habit('Sleep more', 'Get more sleep', 20, 5, 'habit', 2)

        self.task_1 = Habit('Make dinner', 'and make it delicious', 10, 10, 'task', 0)

        self.daily_1 = Habit('Play guitar', 'hit strings in a pleasing combination', 15, 25, 'daily', 0)

        self.item_1 = Item('Laptop', 'laptop.jpg', 5, 1)
        self.item_2 = Item('CAT-5 Cable', 'cat5.jpg', 4, 15)
        self.item_3 = Item('SSD', 'ssd.jpg', 6, 20)

class engine_testCase(characterTestCase):
    """ Tests for 'engine.py' """

    def test_character_data_functions(self):
        #Habits
        self.assertEqual(self.testCharacter.add_habit(self.habit_1), 0, "Habit ID mismatch!")
        self.assertEqual(self.testCharacter.add_habit(self.habit_2), 1, "Habit ID mismatch!")
        self.assertEqual(self.testCharacter.add_habit(self.habit_3), 2, "Habit ID mismatch!")
        self.assertEqual(len(self.testCharacter.habits), 3, "Post-add habit count mismatch!")

        for index in range(len(self.testCharacter.habits)):
            self.assertIsInstance(self.testCharacter.get_habit(index), Habit, "{} is not of type Habit!".format(index))

        self.assertEqual(self.testCharacter.remove_habit(1), 1, "Failed to remove habit with ID of 1")
        self.assertEqual(self.testCharacter.remove_habit(100), -1, "Remove_habit did not throw invalid ID exception!")
        self.assertEqual(len(self.testCharacter.habits), 2, "Post-removal habit count mismatch!")
        
        #Items
        self.assertEqual(self.testCharacter.add_item(self.item_1), 0, "Habit ID mismatch!")
        self.assertEqual(self.testCharacter.add_item(self.item_2), 1, "Habit ID mismatch!")
        self.assertEqual(self.testCharacter.add_item(self.item_3), 2, "Habit ID mismatch!")
        self.assertEqual(len(self.testCharacter.items), 3, "Post-add item count mismatch!")

        for index in range(len(self.testCharacter.items)):
            self.assertIsInstance(self.testCharacter.get_item(index), Item, "{} is not of type Item!".format(index))

        self.assertEqual(self.testCharacter.remove_item(1), 1, "Failed to remove item with ID of 1")
        self.assertEqual(self.testCharacter.remove_item(100), -1, "Remove_item did not throw invalid ID exception!")
        self.assertEqual(len(self.testCharacter.items), 2, "Post-removal item count mismatch!")

        
    def test_complete_habit(self):
        self.testCharacter.add_habit(self.habit_1)
        self.testCharacter.add_habit(self.habit_2)
        self.testCharacter.add_habit(self.habit_3)
        self.app = GUI(self.root, self.testCharacter)
        base_cash = self.app.character.cash
        print("BASE CASH: ", base_cash)
        base_exp = self.app.character.exp
        
        for index in range(len(self.testCharacter.habits)):
            self.app.complete_habit(0) #Pop each habit from the list
        
        self.assertEqual(self.app.character.cash, 170, "Cash not adding correctly!")
        self.assertEqual(self.app.character.exp, 30, "Experience points not adding correctly!")
        self.assertEqual(len(self.app.character.habits), 0, "Habits are not emptying when completed!")

    def test_use_item(self):
        self.testCharacter.add_item(Item('Item_1', 'test1.jpg', 20, -1))
        self.testCharacter.add_item(Item('Item_2', 'test2.jpg', 200, 5))
        self.testCharacter.add_item(Item('Item_3', 'test3.jpg', 20, 1))
        self.app = GUI(self.root, self.testCharacter)

        self.assertEqual(len(self.app.character.items), 3, "-1 item erroneously popped from list!")
        self.app.use_item(1)
        self.assertEqual(self.app.character.items[1].uses, 4, "Item uses did not decrement!")
        self.app.use_item(2)
        self.assertEqual(len(self.app.character.items), 2, "Exhausted items not popped from list!")

    def test_buy_item(self):
        self.testCharacter.cash = 50
        self.app = GUI(self.root, self.testCharacter)

        testItem = Item('Item_1', 'test1.jpg', 20, 1)

        self.app.buy_item(testItem)
        self.assertEqual(self.app.character.cash, 30, 'Cash not decrementing appropriately!')
        self.app.buy_item(testItem)
        self.assertEqual(len(self.app.character.items), 2, 'Item list not receiving new items!')
        self.app.buy_item(testItem)
        self.assertNotEqual(len(self.app.character.items), 3, 'Item list not preventing unaffordable purchases!')
        self.assertEqual(self.app.character.cash, 10, 'Cash decrementing for failed buy attempts!')

    def tearDown(self):
        self.root.destroy()

#class work_space_testCase(unittest.TestCase)
    """ Tests for 'work_space.py' """

#class generic_list_testCase(unittest.TestCase)
    """ Tests for 'generic_list.py' """

#class landing_page_testCase(unittest.TestCase)
    """ Tests for 'landing_page.py' """

#class authenticate_testCase(unittest.TestCase)
    """ Tests for 'authenticate.py' """

#class shop_testCase(unittest.TestCase)
    """ Tests for 'shop.py' """

#class file_parser_testCase(unittest.TestCase)
    """ Tests for 'file_parser.py' """

if __name__ == '__main__':
    unittest.main()
