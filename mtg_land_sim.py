#!/usr/bin/env python3
import random
import copy
import argparse

parser = argparse.ArgumentParser(description='MTG Land Simulator')
parser.add_argument('--lands', dest='lands', type=int, help='Number of lands',
                    default=23)
parser.add_argument('--dorks', dest='dorks', type=int, help='Number of dorks',
                    default=8)
RUNS = 50000

args = parser.parse_args()
lands = args.lands
dorks = args.dorks

def draw(n, deck, hand):
    for x in range(0,n):
        draw_key=random.randint(0,len(deck)-1)
        hand.append(deck.pop(draw_key))


def simulate(lands, dorks):
    #------------------construct a deck ---------------------#
    spells = 60-dorks-lands

    deck_list =[]
    deck_list.append(lands*['land'])
    deck_list.append(dorks*['dork'])
    deck_list.append(spells*['spell'])
    flatten = lambda deck_list: [item for sublist in deck_list for item in sublist]
    deck_list = flatten(deck_list)

    successes = 0

    for i in range(0, RUNS):
        deck = copy.deepcopy(deck_list)
        hand =[]

        #------------------initial draws and mulligans ---------------------#
        draw(7, deck, hand)
        hand_size = 7
        while hand_size >4: 

            #mulligan conditions:
            #with 7: To keep, need at least 2 spells, and at least 2 mana sources.
            #with 6: Same as 7
            #with 5: To keep, need at least 1 land, at least 1 spell.

            if hand_size == 7:
                mull_criteria = (hand.count('land')<=1 and hand.count('land')+hand.count('dork')<=2) or hand.count('spell') <1
            elif hand_size == 6:
                mull_criteria = (hand.count('land') <=1 or hand.count('land')>=6) and hand.count('spell') < 2
            elif hand_size == 5:
                mull_criteria = hand.count('land')== 0 and hand.count('spell') < 1

            if mull_criteria:
                hand_size-=1
                deck = copy.deepcopy(deck_list)
                hand =[]
                draw(hand_size,deck,hand)
            else:
                break
        if hand_size<5:    #If you did mull three times, e.g to 4, concede
            continue

        #---------------checking consistency of mana-------------------#
        draw(2, deck, hand) #T3 on the play
        success_condition = hand.count('land')+hand[:len(hand)-1].count('dork')>=3
        #4 mana sources by T3 including dorks. A dork doesn't count as a source if you drew it on T3 i.e your 2nd draw

        if success_condition:
            successes += 1

    return (successes/RUNS)


result = simulate(lands=lands, dorks=dorks)

print(result)

