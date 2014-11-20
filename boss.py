import base64
from datetime import datetime

class Boss:
    def __init__(self, parent, level, options=None):
        self.level = level
        self.parent = parent

        self.boss_list = {
            '1':["FBI Cybercrimes Unit",2],
            '2':["PLA Unit 61398",1],
            '3':["Cult of the Dead Cow",.5],
            '4':["Kevin Mitnick",.3],
            '5':["Hacker1",.2],
        }

        
        if isinstance(options, dict):
            health = options['health']
            active = options['active']
            distance_from_character = options['distance_from_character']
            new = options['new']
            
        else:
            health = 100
            active = 1
            distance_from_character = 100
            new = 1

        self.health = health
        self.active = active
        self.distance_from_character = distance_from_character
        self.current_timestamp = self.get_time()
        self.previous_attack = None
        self.attack_timeout = 0
        self.new = new
        self.messages = []
        self.set_messages()
        
    def set_messages(self):
        message_1 = 'The FBI Cybercrimes Unit has been recording your recent activity. They\'re hot on your tail!'
        
        message_2 = 'So it seems that you aren\'t the only quick witted black hat after all. PLA Unit 61938 ' + \
                    'out of Hong Kong have recently jumped in on your activities and are trying to thwart your hard-earned ' + \
                    'progress.'
        
        message_3 = 'Welcome n00b! It seems that you\'ve been doing pretty well for yourself, so far at least. I guess homebrewing ' + \
                    'a Wii is merit for an \'accomplished\' hacker nowadays. We\'re on the case now, hoping to share in your GLORY!'+ \
                    '\n LONG LIVE THE COW'
        
        message_4 = 'Kevin Mitnick here.'
        
        message_5 = 'Hacker 1'

        self.messages.append(message_1)
        self.messages.append(message_2)
        self.messages.append(message_3)
        self.messages.append(message_4)
        self.messages.append(message_5)
        
    def get_title(self):
        return self.boss_list[str(self.level)][0]

    def get_time(self):
        return datetime.now().time()
        
    def check_character_status(self, character):
        pass
    
    def serialize(self):
        boss_dict = {'health':self.health,
                     'level':self.level,
                     'active':self.active,
                     'distance':self.distance_from_character,
                     'new':self.new}
        
        encoded_dict = base64.b64encode(bytes(str(boss_dict), 'utf-8'))
        return str(encoded_dict.decode())

    def get_defeat_message(self):
        return "You've defeated " + self.get_title() + "!"
    
    def display_message(self):
        if self.new == 1:
            self.new = 0
            return self.messages[self.level-1]

    def steal_money(self, amount):
        self.parent.steal_character_money(amount)

        
    def damage(self, amount):
        self.health -= amount

    def push_back(self, distance):
        if self.distance_from_character < 100:
            self.distance_from_character += distance

        #Set distance upper limit
        if self.distance_from_character > 100:
            self.distance_from_character = 100
            

    def show_info(self):
        print("BOSS Info")
        print("Title: ", self.get_title())
        print("Level: ", self.level)
        print("Health: ", self.health)
        print("Active: ", self.active)
        print("Distance from character: ", self.distance_from_character)
        

def test(options=None):

    '''
    Basic unit testing
    '''
    
    if options:
        health = options[0]
        level = options[1]

    else:
        health = 100
        level = 3
    
    theboss = Boss(None, level, health)
    print("Boss object:", theboss)
    thebossenc = theboss.serialize()
    #thebossenc = 'eydhY3RpdmUnOiAxLCAnaGVhbHRoJzogMTAwLCAnbmV3JzogMCwgJ2Rpc3RhbmNlJzogMTAwLCAnbGV2ZWwnOiAxfQ=='
    
    print("Boss encoded string:", thebossenc)
    thebossdict = eval(base64.b64decode(bytes(thebossenc, 'utf-8')).decode())
    print("Boss object dictionary:", thebossdict)
    print("-------------------------------------")
    print("Boss Title:", theboss.get_title())
    print("Boss Level:", thebossdict['level'])
    print("Boss Health:", thebossdict['health'])
    print("Active:", thebossdict['active'])
    print("Distance from character:", thebossdict['distance'])
    
if __name__ == '__main__':
    test()
