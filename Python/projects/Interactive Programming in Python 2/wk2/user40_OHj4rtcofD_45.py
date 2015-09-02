# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# contants 
PLAYER = "player"
DEALER = "dealer"

# initialize some useful global variables
in_play = True
outcome = ""
score = 0
player = []
dealer = []
deck = []
winner = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object containing a hand with no cards
        # _cards_list is a list of Card objects
        self._cards_list = []
        
    def __str__(self):
        # return a string representation of a hand
        
        string = "Cards in Hand are : "
        for card in self._cards_list:
            string += card.__str__() + " "
        
        string += "\nHave a total Resulting Value of " + str(self.get_value())
        
        return string    
            

    def add_card(self, card):
        # add a card object to a hand
        
        self._cards_list.append(card)
        
        

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        
        any_aces = False
        sum = 0 
        for a_card in self._cards_list:
            sum += VALUES[a_card.get_rank()]
            if a_card.get_rank() == 'A':
                any_aces = True
                
            
            
        if not any_aces:
            # has no aces 
            return sum
        else:
            # has atleast one ace 
            if sum + 10 <= 21:
                # counted any one of teh aces as 11
                return sum + 10 
            else:
                return sum
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for idx in range(len(self._cards_list)):
            self._cards_list[idx].draw(canvas, (pos[0] + idx*72 ,pos[1]))
               
# define deck class 
class Deck:
    def __init__(self):
        self._cards_deck = []
        # fill the deck with cards of all deck and all ranks 
        for a_suite in SUITS:
            for a_rank in RANKS:
                self._cards_deck.append(Card(a_suite, a_rank))
                
        # Shuffle the created set of cards                
        self.shuffle()

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self._cards_deck)

    def deal_card(self):
        # deal a card object from the deck
        return self._cards_deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        string = "The Deck has teh following cards : "
        for a_card in self._cards_deck:
            string += a_card.__str__() + " "  # this is not a very good programming practive but still 
        
        return string

    
def draw_card_back(canvas, pos):
    # draws a card facedown
    card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
    canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_SIZE)                                     

# define event handlers for buttons

def deal():
    # creates a new deal 
    global outcome, in_play, deck, dealer, player, outcome, winner
    
    outcome = ""
    winner = None
    
    deck = Deck()
    deck.shuffle()
    
    dealer = Hand()
    player = Hand()

    dealer.add_card(deck.deal_card()) 
    player.add_card(deck.deal_card())
    
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())

    in_play = True

    
    
def hit():
    
    global player, dealer, deck, in_play, outcome, score, winner
    
    # if the hand is in play, hit the player
    if in_play == True:
        player.add_card(deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        score -= 1
        outcome = "Busted !!! "
        winner = PLAYER
        in_play = False
    
    print outcome
        
        
def stand():
    global player, dealer, deck, in_play, outcome, score, winner
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())
                
                if dealer.get_value() > 21:
                    outcome = "Busted !!! "
                    winner = DEALER
                    score += 1
                    in_play = False
        
        if dealer.get_value() <= 21:
            # dealer is not busted 
            if dealer.get_value() < player.get_value():
                outcome = "Player Won !!!"
                winner = PLAYER
                score += 1
                in_play = False
                
            elif dealer.get_value() == player.get_value():
                outcome = "It's a Tie !! Dealer Gets the Point "
                winner = DEALER
                score -= 1
                in_play = False
                
            else : 
                outcome = "Dealer Won !!"
                score -= 1
                winner = DEALER
                in_play = False
                
        print outcome
        
    else: # game is not comtinuing just a reminder            
        print outcome   

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player, dealer, outcome, score, winner
    canvas.draw_text("BlackJack", (50, 50), 30, "Aqua")
    canvas.draw_text("Score : "+str(score), (300, 50), 24, "Black")
    canvas.draw_text("Player : ",(50, 100), 24, "Black")
    canvas.draw_text("Dealer : ",(50, 354), 24, "Black")
    
    
    if winner == PLAYER:
        canvas.draw_text(outcome, (200, 100), 26, "White")
        canvas.draw_text("New Deal ? ", (400, 100), 26, "Blue")
    elif winner == DEALER:
        canvas.draw_text(outcome, (200, 354), 26, "White")
        canvas.draw_text("New Deal ? ", (400, 100), 26, "Blue")
    
    player.draw(canvas, (50, 150))
    
    dealer.draw(canvas, (50, 404))
    
    if in_play == True:
        draw_card_back(canvas, (50, 404))
        canvas.draw_text("Hit Or Stand ? ", (200, 100), 30, "Red")
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

# test 
Card1 = Card('C', 'A')
Card2 = Card('C', 'K')
Card3 = Card('C', '2')

Hand1 = Hand()

Hand1.add_card(Card1)
Hand1.add_card(Card2)
Hand1.add_card(Card3)
print Hand1.get_value()

# remember to review the gradic rubric