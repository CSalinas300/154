#!/usr/bin/env python
# coding: utf-8

# In[63]:


import random

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
        
    def show(self):
        print("{} of {}".format(self.value, self.suit))
    
#card = Card("Card", 6)
#card.show()
    
class Deck: 
    def __init__(self):
        self.cards = []
        self.build()
        
    def build(self):
        for i in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for k in range(1,14):
                self.cards.append(Card(i, k))
                
    def show(self):
        for m in self.cards:
            m.show()
            
    def shuffle(self):
        for n in range(len(self.cards) -1, 0, -1):
            r = random.randint(0, n)
            self.cards[n], self.cards[r] = self.cards[r], self.cards[n]
            
    def drawCard(self):
        return self.cards.pop()

class Player: 
    def __init__(self, name):
        self.name = name
        self.hand = []
        
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self
    
    def showHand(self):
        for card in self.hand:
            card.show()
         
deck = Deck()
deck.shuffle()

bob = Player("Bob")
bob.draw(deck)
bob.draw(deck)
bob.draw(deck)
bob.showHand()


# In[ ]:




