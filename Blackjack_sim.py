import random

ranking = ('A', '2', '3', '4','5', '6', '7', '8', '9', '10', 'J', 'K')

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

class Card(Player):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
        
    def show(self):
        print("{} of {}".format(self.value, self.suit))
    
class Deck(Player): 
    def __init__(self):
        self.cards = []
        self.build()
        
    def build(self):
        for i in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for k in ranking:
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

    def calc_val(self):
        total = 0
        for card in self.cards:
	        if card == "J" or card == "Q" or card == "K":
	            total+= 10
	        elif card == "A":
	            if total >= 11: total+= 1
	            else: total+= 11
	       # else:
	       #     total += card
        return total

def policy_2():
    hand = deal()
    return policy_2_recursive(hand), draw_card()

def policy_2_recursive(hand):

    if sum(hand) == 21:
        return hand

    if sum(hand) >= 17:

        is_soft = isSoft(hand)
        index = isSoft(hand)

        if is_soft != True:
            return hand

    card = drawCard()

    if card != 0:
        hand = harden_until (card, hand)
        win = harden_until (card, hand)

    if win != True:
        hand.clear()
        return hand
    else:
        return policy_2_recursive(hand)

         
deck = Deck()
deck.shuffle()

player = Player("Player")
casino = Player("Casino")

casino.draw(deck)
casino.draw(deck)
print("Casinos hand is: ")
casino.showHand()

player.draw(deck)
player.draw(deck)
print("Player's hand is: ")
player.showHand()
print("Player's total is: ")
#deck.calc_val(deck)