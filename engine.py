"""
  Habit game core

  Dependencies: landing_page.py
"""

class Character:
    """
      Class for Habit character profile

      Variables:
        name: Name of character       (string)
        cash: Total currency          (int)
        exp: Total experience points  (int)
        level: Current level          (int)
        habits: Current habits        (list of Habit objects)
        items: Owned (soft|hard)ware  (list of Item objects)
    """
    def __init__(self, name):
        self.name = name
        self.cash = 0
        self.exp = 0
        self.level = 1
        self.habits = []
        self.items = []


class Habit:
    """
      Class for Individual Habits

      Variables:
        name: Name of habit         (string)
        value: Cash reward/penalty  (int)
        exp: Experience point value (int)
    """
    def __init__(self, name, value, exp):
        self.name = name
        self.value = value
        self.exp = exp

class Item:
    """
      Class for purchasable software/hardware

      Variables:
        name: Name of item                                (string)
        image: Name of accompanying image                 (string)
        value: Currency value of item                     (int)
        uses: Uses before item expires [-1 for infinite]  (int)
    """
    def __init__(self, name, image, value, uses):
        self.name = name
        self.image = image
        self.value = value
        self.uses = uses

def main():
    """
      Stub for main function
    """

if __name__ = "__main__":
    main();
