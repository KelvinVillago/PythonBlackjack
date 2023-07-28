import random

#global variables that will be used all game
suits = {'Hearts', 'Diamonds', 'Clubs', 'Spades'}
ranks = {'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'Ace'}
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"<Card {self.suit} | {self.rank}>"
    
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        return f"There are {len(self.deck)} cards left in the deck\n"

    def __repr__(self):
        return f"<Deck | {len(self.deck)} cards>"

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        card = self.deck.pop()
        return card

class Person:
    def __init__(self, name = 'player'):
        self.name = name
        self.cards = []
        self.value = 0
        self.aces = 0

    def addCard(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def aceAdjust(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
    def __str__(self):
        output = f"\n{self.name.title()}: "
        for card in self.cards:
            output += str(card) + ', '
        output += "Value: " + str(self.value)
        output += '\n'
        return output

class Dealer(Person):
    def __init__(self, deck, name='dealer'):
        super().__init__(name)
        self.deck = deck

    def displayFirst(self):
        output = f"\n{self.name.title()}: "
        output += "<hidden>, "
        output += str(self.cards[1])
        output += '\n'
        return output
    
    def dealerPlay(self):
        while self.value <= 17:
            self.addCard(self.deck.deal())

class Player(Person):
    pass

def play(deck, hand):
    #function to handle playing the game
    while True:
        global playing #used to access global var
        decision = input("Do you want to hit or stand (hit/stand): ").lower().strip(' ')
        if decision == 'hit':
            hand.addCard(deck.deal())
        elif decision == 'stand':
            print("Player has chosen to stand. Dealer's turn. \n")
            playing = False #needed to break out of loop. Without it standing option results in infinite loop
        else:
            print('Invalid input. Please try again: ')
            continue
        break

def main():
    global playing #used to access global var

    #Enter amount to start in table
    startAmt = input("How much would you like to play with: ")
    while not startAmt.isnumeric():
            startAmt = input("Invalid amount")
    startAmt = int(startAmt)

    while True:
        deck = Deck() #create Deck instance
        deck.shuffle()

        #Handle betting and if there is no more money left
        betAmt = input("How much would you like to bet: ")
        while not betAmt.isnumeric():
            betAmt = input("Invalid bet amount")
        betAmt = int(betAmt)
        if startAmt <= 0:
            print("Sorry, you do not have enough money to play again. \n")
            break
        
        #Create users
        player = Player('Henry')
        player.addCard(deck.deal())
        player.addCard(deck.deal())

        dealer = Dealer(deck)
        dealer.addCard(deck.deal())
        dealer.addCard(deck.deal())

        #display the card of both players
        print(dealer.displayFirst())
        print(player)

        while playing: #Runs true while player does not pick stand option
            #Doubling down if I understood it correctly
            double = input("Would you like to double down (y/n)? ")
            if double == 'y':
                betAmt *= 2
                print(f"The bet amount is now ${betAmt}")

            play(deck, player) #play the game
            
            #Print hands of both players
            print(dealer.displayFirst())
            print(player)

            #Check player to end game instantly
            if player.value == 21:
                print(f'{player.name.title()} Wins.')
                startAmt += 2*betAmt
                break
            elif(player.value > 21):
                print(f'{player.name.title()} Bust. {dealer.name.title()} wins')
                startAmt -= betAmt
                break

        if player.value < 21: #Other win conditions where dealer has to play the game
            dealer.dealerPlay()
            print(dealer)
            print(player)

            if dealer.value > 21:
                print(f'{dealer.name.title()} Bust. {player.name.title()} wins')
                startAmt += 2*betAmt
            elif player.value > dealer.value:
                print(f'{player.name.title()} Wins.')
                startAmt += 2*betAmt
            elif dealer.value == 21:
                print(f'{dealer.name.title()} Wins.')
                startAmt -= betAmt
            elif player.value < dealer.value:
                print(f'{dealer.name.title()} Wins.')
                startAmt -= betAmt
            elif player.value == dealer.value:
                print(f'Tie. {dealer.name.title()} Wins.')
                startAmt -= betAmt

        #Print finishing text
        print(f"Your balance: ${startAmt}\n")
        toDo = input("\nWould you like to continue playing (y/n): ").lower()
        if toDo == 'y':
            playing = True
            continue
        else:
            print("Thank you for playing")
            break


main()