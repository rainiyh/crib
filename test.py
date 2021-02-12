import unittest

import crib

class Tester(unittest.TestCase):
    # Test if deck has 52 cards
    def test_deck_len(self):
        self.assertEqual(len(crib.makeDeck()), 52)
        
    # Test if each suit in the deck has 13 cards
    def test_num_cards_in_suit(self):
        deck = crib.makeDeck()
        spades = 0
        clubs = 0
        hearts = 0
        diamonds = 0
        for card in deck:
            if card.suit == "spades":
                spades += 1
            elif card.suit == "clubs":
                clubs += 1
            elif card.suit == "hearts":
                hearts += 1
            elif card.suit == "diamonds":
                diamonds += 1
                
        self.assertEqual(spades, 13)
        self.assertEqual(clubs, 13)
        self.assertEqual(hearts, 13)
        self.assertEqual(diamonds, 13)
        
    # Test scoring some sample hands
    def test_score_hand(self):
        hand = []
        hand.append(crib.Card(5, "clubs"))
        hand.append(crib.Card(5, "diamonds"))
        hand.append(crib.Card(5, "hearts"))
        hand.append(crib.Card(11, "spades"))
        self.assertEqual(crib.scoreHand(hand, crib.Card(5, "spades")), 29)
        
        hand = []
        hand.append(crib.Card(7, "spades"))
        hand.append(crib.Card(4, "diamonds"))
        hand.append(crib.Card(4, "hearts"))
        hand.append(crib.Card(4, "clubs"))
        self.assertEqual(crib.scoreHand(hand, crib.Card(4, "spades")), 24)
        
        hand = []
        hand.append(crib.Card(11, "spades"))
        hand.append(crib.Card(7, "spades"))
        hand.append(crib.Card(4, "spades"))
        hand.append(crib.Card(13, "spades"))
        self.assertEqual(crib.scoreHand(hand, crib.Card(6, "spades")), 6)
    
    # Test AI's go play - playing such that the table count is over 31 is illegal
    def test_go_card(self):
        table = []
        table.append(crib.Card(10, "spades"))
        table.append(crib.Card(10, "hearts"))
        table.append(crib.Card(5, "diamonds"))
        for i in range(10):
            aiHand = []
            deck = crib.makeDeck()
            for j in range(4):
                aiHand.append(deck.pop())
            
            total = 25
            self.assertTrue(crib.aiPlayGoCard(aiHand, table).value + total <= 31)
    
if __name__ == '__main__':
    unittest.main()