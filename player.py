import deck

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def show_hand(self):
        print("Hand:")
        i = 1
        for card in self.hand:
            print(str(i) + ". ", end="")
            card.peek()
            i += 1

    def draw_card(self, deck):
        self.hand.append(deck.draw_card())

    def num_cards(self):
        return len(self.hand)

    def remove_cards(self, cards):
        for card in cards:
            self.hand.remove(card)

    def low_card(self):
        low_card = deck.Card("Hearts", 2)
        for card in self.hand:
            low_card = deck.compare_cards(low_card, card)
        return low_card

    async def valid_single(self, player_card, card_stack, prev_move):
        if card_stack == []:
            return True
        if prev_move == 1:
            if await deck.compare_cards(player_card, card_stack[0]) == card_stack[0]:
                return True
        return False

    async def play_single(self, card, card_stack, prev_move):
        player_card = self.hand[card]
        if await self.valid_single(player_card, card_stack, prev_move):
            self.remove_cards([player_card])
            return [player_card]
        return False

    async def valid_double_triple(self, player_cards, card_stack):
        card_value_set = set()
        for card in player_cards:
            card_value_set.add(card.value)
        if len(card_value_set) == 1:
            if card_stack == []:
                return True
            elif len(player_cards) == len(card_stack):
                player_high_card = await deck.high_card(player_cards)
                card_stack_high_card = await deck.high_card(card_stack)
                high_card = await deck.compare_cards(player_high_card, card_stack_high_card)
                if high_card == card_stack_high_card:
                    return True
        return False

    async def play_double_triple(self, cards, card_stack):
        player_cards = [self.hand[card] for card in cards]
        if await self.valid_double_triple(player_cards, card_stack):
            self.remove_cards(player_cards)
            return player_cards
        return False

    async def valid_run(self, player_cards, card_stack, prev_move):
        card_values = [card.value for card in player_cards]
        if len(card_values) < 3:
            return False
        if 2 in card_values:
            return False
        if 1 in card_values:
            one_index = card_values.index(1)
            card_values[one_index] = 14
        if sorted(card_values) == list(range(min(card_values), max(card_values)+1)):
            if card_stack == []:
                return True
            elif prev_move == 4 and len(player_cards) == len(card_stack):
                player_high_card = await deck.high_card(player_cards)
                card_stack_high_card = await deck.high_card(card_stack)
                low_card = await deck.compare_cards(player_high_card, card_stack_high_card)
                if low_card == card_stack_high_card:
                    return True
        return False

    async def play_run(self, cards, card_stack, prev_move):
        player_cards = [self.hand[card] for card in cards]
        if await self.valid_run(player_cards, card_stack, prev_move):
            self.remove_cards(player_cards)
            return player_cards
        return False