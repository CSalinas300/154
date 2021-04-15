#!/usr/bin/env python
# coding: utf-8

# In[14]:


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

#bob = Player("Bob")
#bob.draw(deck)
#bob.draw(deck)
#bob.draw(deck)
#bob.showHand()

def isSoft(hand):
        index = -1
        for i in range(len(hand)-1, 0, 1):
            if hand[i]==11:
                index = i
        is_Soft = True if index != -1 else False
        return is_soft, index

def harden_until(new_card, hand):

    if new_card + sum(hand) > 21:

        is_soft, index = check_softness(hand)

        if is_soft:
            return harden_until(new_card, harden(hand, index))

        elif new_card == 11:
            return harden_until(1, hand)

        else:
            hand.clear()
            return hand, False

    else:
        hand.append(new_card)
        return hand, True


# In[ ]:





# In[ ]:





# In[ ]:




