import random
import copy
import time

class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit
        
        # Num: Raw number the computer uses to generate cards.
        # Value: Value of the card. Face cards are 10.
        # Name: Name of the card. Replaces 11, 12, 13, 1 with Jack, Queen, King, Ace.
        if self.num > 10:
            self.value = 10
        else:
            self.value = num
            
        if self.num == 1:
            self.name = "Ace"
        elif self.num < 11:
            self.name = num
        elif self.num == 11:
            self.name = "Jack"
        elif self.num == 12:
            self.name = "Queen"
        elif self.num == 13:
            self.name = "King"
    
    def __str__(self):
        return str(self.name) + " of " + str(self.suit)
            
class Player:
    def __init__(self):
        self.points = 0
        self.hand = []
        self.dealer = False

def makeDeck():
    deck = []
    suits = ["clubs", "diamonds", "hearts", "spades"]

    for i in range(1, 14):
        for j in suits:
            deck.append(Card(i, j))

    random.shuffle(deck)
    return deck
    
def printHand(hand, string):
    print (string)
    for i in range(len(hand)):
        print(i + 1, ": ", hand[i].__str__())
        
def printScore():
    print ("Player score: ", player1.points)
    print ("Computer score: ", player2.points)
    
def scoreHand(origHand, cut):
    hand = origHand
    hand.append(cut)
    
    pairs = 0
    fifteens = 0
    runPoints = 0
    flush = 0
    nob = 0
    
    # 15, pair
    for i in range(len(hand) - 1):
        for j in range(i + 1, len(hand)):
            if hand[i].value + hand[j].value == 15:
                fifteens += 1
            if hand[i].num == hand[j].num:
                pairs += 1
    # Now with 3 cards
    for i in range(len(hand) - 2):
        for j in range(i + 1, len(hand) - 1):
            for k in range(j + 1, len(hand)):
                if hand[i].value + hand[j].value + hand[k].value == 15:
                    fifteens += 1
    # 4 cards...
    for i in range(len(hand)):
        count = 0
        for card in hand:
            if card == hand[i]:
                continue
            else:
                count += card.value
        if count == 15:
            fifteens += 1
    # And 5 cards!
    if hand[0].value + hand[1].value + hand[2].value + hand[3].value + hand[4].value == 15:
        fifteens += 1
                
    # Runs
    values = []
    numRuns = 1
    runLength = 1
    for card in hand:
        values.append(card.num)
    values.sort()
    for i in range(len(values) - 1):
        # If the cards are consecutive, increment run length
        if values[i] + 1 == values[i+1]:
            runLength += 1
        # If it's a pair, double the number of runs.
        elif values[i] == values[i+1]:
            # But catch a 3-of-a-kind! The numRuns will already have been doubled (to 2) so it is incremented by 1.
            if values[i] == values[i-1]:
                numRuns += 1
            else:
                numRuns *= 2
        # And if the cards are not consecutive, reset if less than 3, othewise keep the score.
        else:
            if runLength >= 3:
                break
            else:
                runLength = 1
                
    if  runLength >= 3:
        runPoints = runLength * numRuns
    
    # Flush
    if hand[0].suit == hand[1].suit and hand[0].suit == hand[2].suit and hand[0].suit == hand[3].suit:
        if hand[0].suit == cut.suit:
            flush = 5
        else:
            flush = 4
    
    # And one for his nob
    for card in origHand:
        if card.num == 11 and card.suit == cut.suit:
            nob = 1
            break
            
    return fifteens * 2 + pairs * 2 + runPoints + flush + nob
    
def checkWin(player1, player2):
    if player1.points > 120:
        print ("You win!")
        printScore()
        exit()
    elif player2.points > 120:
        print ("You lose! What a noob.")
        printScore()
        exit()
        
def scoreGoCard(table, card):
    tablePoints = 0
    cardPoints = 0
    pair = 0
    flush = 0
    run = 0
    
    # 15, 31
    for goCard in table:
        tablePoints += goCard.value
    if tablePoints + card.value == 15:
        cardPoints += 2
    
    # Pair
    for goCard in reversed(table):
        if goCard.num == card.num:
            pair+= 1
        else:
            break
    # And score them properly.
    if pair == 1:
        cardPoints += 2
    elif pair == 2:
        cardPoints += 6
    elif pair == 3:
        cardPoints += 12
        
    # Flush
    for goCard in reversed(table):
        if goCard.suit == card.suit:
            flush+= 1
        else:
            break
    # And score
    if flush >= 4:
        cardPoints += flush
        
    # Run
    testTable = [card.num]
    # Walk backwards through the table and see what's the longest length of run we can create
    for card in reversed(table):
        testTable.append(card.num)
        # We test to see if the sorted test set of card values is equal to a generated set of sequential card values. This is the only way it can be a run.
        if sorted(testTable) == list(range(min(testTable), min(testTable) + len(testTable))) and len(testTable) >= 3:
            run = len(testTable)
    cardPoints += run
            
    return cardPoints
    
def aiPlayGoCard(hand, table):
    tablePoints = 0
    for card in table:
        tablePoints += card.value
    
    testHand = copy.copy(hand)
    while testHand:
        choice = random.randint(0, len(testHand) - 1)
        if testHand[choice].value + tablePoints > 31:
            testHand.pop(choice)
        else:
            return testHand[choice]
    return None

def round(player1, player2):
    # Shuffle and deal
    deck = makeDeck()
    player1.hand = []
    player2.hand = []
    
    if (player1.dealer):
        print ("\nYou are the dealer!")
    else:
        print ("\nThe computer is the dealer!")
    
    for i in range(6):
        player1.hand.append(deck.pop())
        player2.hand.append(deck.pop())
    
    # Display player cards and prompt for crib
    printHand(player1.hand, "\nYour hand: ")
    
    while True:
        selection = input("Please select two cards for the crib: ")
        
        # Ensure the input is correct
        try:
            card1 = int(selection[0:1])
        except ValueError:
            print ("Please ensure input is of form [num][num] where 'num' is a number between 1 and 6 to select 2 different cards to send to the crib.")
            continue
        try:
            card2 = int(selection[1:2])
        except ValueError:
            print ("Please ensure input is of form [num][num] where 'num' is a number between 1 and 6 to select 2 different cards to send to the crib.")
            continue
        
        if card1 >= 1 and card1 <= 6 and card2 >= 1 and card2 <= 6:
            break
        print ("Please ensure input is of form [num][num] where 'num' is a number between 1 and 6 to select 2 different cards to send to the crib.")
    
    # Transfer cards to the crib
    crib = Player()
    crib.hand.append(player1.hand.pop(max(card1, card2) - 1))
    crib.hand.append(player1.hand.pop(min(card1, card2) - 1))
    
    time.sleep(0.5)
    
    # And the computer does the same.
    card1 = random.randint(0, 6)
    card2 = random.randint(0, 6)
    crib.hand.append(player2.hand.pop(max(card1, card2) - 1))
    crib.hand.append(player2.hand.pop(min(card1, card2) - 1))
        
    # Cut
    cut = deck.pop()
    print ("\nCut card: " + cut.__str__())
    
    if cut.value == 11:
        for player in [player1, player2]:
            if player.dealer:
                print("Dealer awarded 2 for his heels!")
                checkWin(player1, player2)
                printScore()
    
    time.sleep(0.5)
    
    # Go
    playerGoHand = copy.copy(player1.hand)
    aiGoHand = copy.copy(player2.hand)
    table = []
    tableCount = 0
    if player1.dealer:
        print ("\nPlayer is the dealer. Computer goes first.")
        cardChoice = aiPlayGoCard(aiGoHand, table)
        time.sleep(0.5)
        print ("\nComputer plays: ", cardChoice.__str__())
        table.append(aiGoHand.pop(aiGoHand.index(cardChoice)))
        tableCount += cardChoice.value
    else:
        print ("\nComputer is the dealer. Player goes first.")
        
    aiGo = False
    lastCard = None
        
    while playerGoHand or aiGoHand:
        playerGo = True
        score = 0
        printHand(playerGoHand, "")
        while True:
            # Test if player has a valid card to play
            for card in playerGoHand:
                if card.value + tableCount <= 31:
                    playerGo = False
            if playerGo:
                print ("No playable cards. Player says Go!")
                time.sleep(0.5)
                card1 = None
                if aiGo:
                    print ("Player scores 1 point.")
                    player1.points += 1
                    checkWin(player1, player2)
                    print ("Player's score: ", player1.points)
                    table = []
                    tableCount = 0
                    aiGo = False
                    playerGo = False
                break
            
            # Prompt player for input and make sure it's correct
            selection = input("Select a card to play: ")
            try:
                card1 = int(selection[0:1])
            except ValueError:
                print ("Please ensure card selection is a number corresponding to the card choice.")
                continue
            if card1 >= 1 and card1 <= len(playerGoHand):
                if (playerGoHand[card1 - 1].value + tableCount > 31):
                    print ("Over 31! Not a legal choice.")
                    continue
                break
            print ("Please ensure card selection is a number corresponding to the card choice.")
        
        # If card chosen, play it.
        if card1 is not None:
            lastCard = player1
            score = scoreGoCard(table, playerGoHand[card1 - 1])
            print ("\nYou played: ", playerGoHand[card1 - 1].__str__())
            table.append(playerGoHand.pop(card1 - 1))
            tableCount += table[len(table) - 1].value
            if tableCount == 31:
                print ("31 for two!")
                player1.points += 2
                checkWin(player1, player2)
                print ("Your score: ", player1.points)
                table = []
                tableCount = 0
            else:
                print ("Count: ", tableCount)
            if score > 0:
                print ("Score for that card: ", score)
                player1.points += score
                checkWin(player1, player2)
                print ("Your score: ", player1.points)
            
        score = 0
        
        # AI turn
        card2 = aiPlayGoCard(aiGoHand, table)
        # Choice is None if there's no legal card to play
        if card2 is None:
            time.sleep(0.5)
            print ("Computer says Go!")
            # If player has already said Go, score a point and reset
            if playerGo:
                print ("Computer scores 1 point.")
                player2.points += 1
                checkWin(player1, player2)
                print ("Computer's score: ", player2.points)
                table = []
                tableCount = 0
                aiGo = False
            else:
                aiGo = True
        # Else play the card
        else:
            time.sleep(0.5)
            lastCard = player2
            print ("\nComputer plays: ", card2.__str__())
            score = scoreGoCard(table, card2)
            table.append(aiGoHand.pop(aiGoHand.index(card2)))
            tableCount += table[len(table) - 1].value
            if tableCount == 31:
                print ("31 for two!")
                player2.points += 2
                checkWin(player1, player2)
                print ("Computer's score: ", player2.points)
                table = []
                tableCount = 0
            else:
                print ("Count: ", tableCount)
            if score > 0:
                print ("Score for that card: ", score)
                player2.points += score
                checkWin(player1, player2)
                print ("Computer's score: ", player2.points)
    
    time.sleep(0.5)
    
    if lastCard == player1:
        print ("\nPlayer scores 1 point for last card.")
        player1.points += 1
        checkWin(player1, player2)
        print ("Player's score: ", player1.points)
    else:
        print ("\nComputer scores 1 point for last card.")
        player2.points += 1
        checkWin(player1, player2)
        print ("Computer's score: ", player2.points)
        
    time.sleep(0.5)
    
    print ("\nCounting off!")
    
    # Count Off
    player1score = scoreHand(player1.hand, cut)
    player2score = scoreHand(player2.hand, cut)
    cribScore = scoreHand(crib.hand, cut)
    
    # Opponent goes first.
    if player1.dealer:
        print ("\nYou are the dealer! Computer counts off first.")
        printHand (player2.hand, "\nComputer hand: ")
        print ("Score: ", player2score)
        player2.points += player2score
        checkWin(player1, player2)
        print ("Computer's score: ", player2.points)
        
        time.sleep(1)
        
        printHand (player1.hand, "\nPlayer hand: ")
        print ("Score: ", player1score)
        player1.points += player1score
        checkWin(player1, player2)
        print ("Your score: ", player1.points)
        
    else:
        print ("\nThe computer is the dealer! You count off first.")
        printHand (player1.hand, "\nPlayer hand: ")
        print ("Score: ", player1score)
        player1.points += player1score
        checkWin(player1, player2)
        print ("Your score: ", player1.points)
        
        time.sleep(1)
        
        printHand (player2.hand, "\nComputer hand: ")
        print ("Score: ", player2score)
        player2.points += player2score
        checkWin(player1, player2)
        print ("Computer's score: ", player2.points)

    time.sleep(1)
    
    printHand (crib.hand, "\nCrib: ")
    print ("Score: ", cribScore)
    
    # Allocate crib points correctly
    if player1.dealer:
        print ("You were the dealer! You get the crib points.")
        player1.points += cribScore
        player1.dealer = False
        player2.dealer = True
    else:
        print ("\nThe computer was the dealer! It gets the crib points.")
        player2.points += cribScore
        player1.dealer = True
        player2.dealer = False
    checkWin(player1, player2)
    printScore()
    
    time.sleep(2)
    
# Main game sequence
if __name__ == '__main__':
    player1 = Player()
    player2 = Player()
    random.seed()

    if random.randint(1, 2) == 1:
        player1.dealer = True
    else:
        player2.dealer = True

    while True:
        # Play round
        round(player1, player2)