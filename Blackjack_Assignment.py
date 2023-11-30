# Blackjack Assignment

import requests
import os

# Using a deack of cards API
def new_deck():
    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
    deck_data = response.json()
    return deck_data["deck_id"]

# Making sure we're drawing the correct amount of cards
def draw_cards(deck_id, num_cards):
    draw_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={num_cards}"
    response = requests.get(draw_url)
    return response.json()["cards"]

# Calculating the total value of a hand
def calculate_hand_value(hand):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'JACK': 10, 'QUEEN': 10, 'KING': 10, 'ACE': 11}
    total_value = sum(values.get(card['value'], 0) for card in hand)
    
    # Changing the value of an Ace from 11 to 1 if player's total hand value exceeds 21
    for card in hand:
        if card['value'] == 'ACE' and total_value > 21:
            total_value -= 10  
    
    return total_value

# Displaying the player's and dealer's hands
def display_hand(player_hand, dealer_hand, show_all=False):
    print("\nYour hand:")
    for card in player_hand:
        print(f"{card['value']} of {card['suit']}")
    print(f"Total value: {calculate_hand_value(player_hand)}")

    print("\nDealer's hand:")
    if show_all:
        for card in dealer_hand:
            print(f"{card['value']} of {card['suit']}")
        print(f"Total value: {calculate_hand_value(dealer_hand)}")
    else:
        print(f"{dealer_hand[0]['value']} of {dealer_hand[0]['suit']}")
        print("One card hidden")

# Playing the game
def blackjack_game():
    # Get a new deck 
    deck_id = new_deck()

    # Draw initial hands for the player and dealer
    player_hand = draw_cards(deck_id, 2)
    dealer_hand = draw_cards(deck_id, 2)

    while True:
        # Display both hands
        display_hand(player_hand, dealer_hand)

        # Check for blackjack (21) in the initial hands
        if calculate_hand_value(player_hand) == 21:
            print("Congratulations! You have a blackjack. You win!")
            break

        # Ask the player to hit or stand
        action = input("Do you want to hit or stand? ").lower()

        # Draw a new card if the player chooses to hit
        if action == "hit":
            player_hand.extend(draw_cards(deck_id, 1))
            
            # Check for bust (total value > 21)
            if calculate_hand_value(player_hand) > 21:
                display_hand(player_hand, dealer_hand, show_all=True)
                print("Bust! You lose.")
                break
        elif action == "stand":
            # Dealer's turn
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.extend(draw_cards(deck_id, 1))
            
            
            display_hand(player_hand, dealer_hand, show_all=True)

            # Determine the winner
            if calculate_hand_value(dealer_hand) > 21 or calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand):
                print("Congratulations! You win!")
            elif calculate_hand_value(player_hand) < calculate_hand_value(dealer_hand):
                print("Oh no, you lose.")
            else:
                print("It's a tie!")

            break
        else:
            print("Wrong input. Please enter 'hit' or 'stand'.")

if __name__ == "__main__":
    blackjack_game()

