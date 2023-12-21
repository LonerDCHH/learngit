
from enum import IntEnum, unique
from typing import Tuple, List
import copy




@unique
class Color(IntEnum):
    RED = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3
    CYAN = 4
    ORANGE = 5
    PURPLE = 6
    WHITE = 7
    BLACK = 8
    VIOLET = 9
    

@unique
class Effect(IntEnum):
    CHANGE_COLOR = 0
    BAN = 1
    PLUS_TWO = 2


@unique
class ActionType(IntEnum):
    DRAW = 0
    DROP = 1
    PASS = 2



class Card:
   
    def __init__(self, color: Color) -> None:
        self._color = color
        pass

    def get_color(self) -> Color:
        # YOUR CODE HERE
        return self._color
        pass



class NumericCard(Card):
    def __init__(self, color: Color, number: int) -> None:
        super().__init__(color)
        # YOUR CODE HERE
        self.number=number
        pass

    def __repr__(self) -> str:
        # YOUR CODE HERE
        return f"Numeric card {Color(self._color).name} {self.number}"
        pass

    # We provide some hints for you to implement this method.
    def __lt__(self, other: Card) -> bool:
        if not isinstance(other, NumericCard) and not isinstance(other, SpecialCard):
            raise Exception("Invalid Card Type")
        
        if self.get_color() < other.get_color():
            # YOUR CODE HERE
            return True
        elif self.get_color() > other.get_color():
            # YOUR CODE HERE
            return False
        else:
            if isinstance(other, NumericCard):
                # YOUR CODE HERE
                if self.number<other.number:
                    return True
                else:
                    return False

            else:
                # YOUR CODE HERE
                return True

    # You should implement this method (almost) completely by yourself.
    def __eq__(self, other: Card) -> bool:
        if not isinstance(other, NumericCard) and not isinstance(other, SpecialCard):
            raise Exception("Invalid Card Type")
        # YOUR CODE HERE
        if not isinstance(other, NumericCard):
            return False
        if self.number==other.number and self.get_color() == other.get_color():
            return True
        else:
            return False


    def get_number(self) -> int:
        # YOUR CODE HERE
        return self.number
        pass


class SpecialCard(Card):
    def __init__(self, color: Color, effect: Effect) -> None:
        super().__init__(color)
        # YOUR CODE HERE
        self.effect=effect
        pass

    def __repr__(self) -> str:
        # YOUR CODE HERE
        return f"{Effect(self.effect).name} card {Color(self._color).name}"
        pass

    def __lt__(self, other: Card) -> bool:
        if not isinstance(other, NumericCard) and not isinstance(other, SpecialCard):
            raise Exception("Invalid Card Type")   
        # YOUR CODE HERE
        if self.get_color() < other.get_color():
            # YOUR CODE HERE
            return True
        elif self.get_color() > other.get_color():
            # YOUR CODE HERE
            return False
        else:
            if isinstance(other, SpecialCard):
                # YOUR CODE HERE
                if self.get_effect()<other.get_effect():
                    return True
                else:
                    return False

            else:
                # YOUR CODE HERE
                return False


    def __eq__(self, other: Card) -> bool:
        if not isinstance(other, NumericCard) and not isinstance(other, SpecialCard):
            raise Exception("Invalid Card Type")
        # YOUR CODE HEREdef __eq__(self, other: Card) -> bool:
        if not isinstance(other, SpecialCard):
            return False
        if self.get_effect()==other.get_effect() and self.get_color() == other.get_color():
            return True
        else:
            return False

    
    def get_effect(self) -> Effect:
        # YOUR CODE HERE
        return self.effect
        pass



class CardSet:
    _cards: List[Card]

    def __init__(self, cards: List[Card]) -> None:
        # You should guarantee that we CANNOT modify your self._cards from outside.
        # YOUR CODE HERE
        self._cards=copy.deepcopy(cards)
        pass

    def __repr__(self) -> str:
        # YOUR CODE HERE
        return str(self._cards)
        pass    

    def is_empty(self) -> bool:
        # YOUR CODE HERE
        if len(self._cards)==0:
            return True
        else:
            return False
        pass

    def get_cards(self) -> List[Card]:
        return copy.deepcopy(self._cards)


class Hand(CardSet):
    def add_card(self, card: Card) -> None:
        # YOUR CODE HERE
        self._cards.append(card)
        pass
    
    def remove_card(self, card: Card) -> None:
        # YOUR CODE HERE
        self._cards.remove(card)
        pass


class Deck(CardSet):
    def get_next_card(self) -> Card:
        if self.is_empty():
            raise Exception("No Card Left")
        else:
            returned_cards=self._cards.pop(0)
            return returned_cards
class Player:
    def sort_cards(self, cards: List[Card]) -> List[Card]:
        # YOUR CODE HERE
        return sorted(cards,reverse=True)
        pass
    def action(self, cards: List[Card], last_card: Card, is_last_player_drop: bool) -> Tuple[ActionType, Card | None]: 
        # YOUR CODE HERE
        cards=self.sort_cards(cards)
        if is_last_player_drop==False:
            if not isinstance(last_card,SpecialCard) and not isinstance(last_card,NumericCard) :
                return ActionType.DROP,cards[0]
            elif isinstance(last_card, NumericCard):
                n=0
                for card in cards:
                    if isinstance(card, SpecialCard) :
                        if card.get_effect()==0:
                            return ActionType.DROP,card
                        elif card.get_color()==last_card.get_color():
                            return ActionType.DROP,card
                            break
                    elif  isinstance(card,NumericCard):
                        if card.get_color()==last_card.get_color() or card.get_number()==last_card.get_number() :
                            return ActionType.DROP,card
                            break
                    n+=1
                if n==len(cards):
                    return ActionType.DRAW,None
            elif isinstance(last_card, SpecialCard):
                if last_card.get_effect()==0:
                    n=0
                    for card in cards:
                        if isinstance(card, SpecialCard):
                            if card.get_effect()==0:
                                return ActionType.DROP,card 
                            elif card.get_color()==last_card.get_color():
                                return ActionType.DROP,card
                        elif  isinstance(card,NumericCard):
                            if card.get_color()==last_card.get_color()  :
                                return ActionType.DROP,card
                                break
                        n+=1
                    if n==len(cards):
                        return ActionType.DRAW,None
                elif last_card.get_effect()==1:
                    n=0
                    for card in cards:
                        if isinstance(card, SpecialCard):
                            if card.get_effect()==1 or card.get_effect()==0:
                                return ActionType.DROP,card 
                            elif card.get_color()==last_card.get_color():
                                return ActionType.DROP,card 
                        elif  isinstance(card,NumericCard):
                            if card.get_color()==last_card.get_color():
                                return ActionType.DROP,card
                                break
                        n+=1
                    if n==len(cards):
                        return ActionType.DRAW,None
                else:
                    n=0
                    for card in cards:
                        if isinstance(card, SpecialCard) :
                            if card.get_effect()==2 or card.get_effect()==0:
                                return ActionType.DROP,card 
                            elif card.get_color()==last_card.get_color():
                                return ActionType.DROP,card 
                        elif  isinstance(card,NumericCard):
                            if card.get_color()==last_card.get_color()  :
                                return ActionType.DROP,card
                                break
                        n+=1
                    if n==len(cards):
                        return ActionType.DRAW,None               
        else:
            if isinstance(last_card, NumericCard):
                n=0
                for card in cards:
                    if isinstance(card, SpecialCard) :
                        if card.get_effect()==0:
                            return ActionType.DROP,card
                        elif card.get_color()==last_card.get_color():
                            return ActionType.DROP,card
                            break
                    elif  isinstance(card,NumericCard):
                        if card.get_color()==last_card.get_color() or card.get_number()==last_card.get_number() :
                            return ActionType.DROP,card
                            break
                    n+=1
                if n==len(cards):
                    return ActionType.DRAW,None
            elif isinstance(last_card, SpecialCard):
                if last_card.get_effect()==0:
                    n=0
                    for card in cards:
                        if isinstance(card, SpecialCard): 
                            if card.get_effect()==0:
                                return ActionType.DROP,card
                            elif card.get_color()==last_card.get_color():
                                return ActionType.DROP,card
                                break
                        elif  isinstance(card,NumericCard):
                            if card.get_color()==last_card.get_color()  :
                                return ActionType.DROP,card
                                break
                        n+=1
                    if n==len(cards):
                        return ActionType.DRAW,None
                elif last_card.get_effect()==1:
                    return ActionType.PASS,None
                else:
                    n=0
                    for card in cards:
                        if isinstance(card, SpecialCard): 
                            if  card.get_effect()==2:
                                return ActionType.DROP,card
                                break
                        n+=1
                    if n==len(cards):
                        return ActionType.PASS,None 
class Game:
    _player_hands: List[Hand]
    the_winner:int
    # Construct Game and initialize the deck and players
    def __init__(self, cards: List[Card], num_player: int = 7, hand_card_num: int = 7, dealer_id: int = 0) -> None:
        self._deck = Deck(cards)
        self._players = [Player() for _ in range(num_player)]
        
        '''
        We add a '-1' because _current_player_id will +1 when we call turn() at the first time,
        and we need to -1 before that to keep the correctness.
        '''
        self._current_player_id = dealer_id - 1
        self._last_card = None
        self._is_last_player_drop = False   
        self._plus_two_cnt = 0   
        self._player_hands=[Hand([self._deck.get_next_card() for _ in range(hand_card_num)]) for _ in range(num_player)]
        # Implement self._player_hands.
        # YOUR CODE HERE

    # This is used for our test. Please DO NOT CHANGE it.
    def get_info(self) -> Tuple[int, Card, bool, int, List[Hand]]:
        return self._current_player_id, self._last_card, self._is_last_player_drop, self._plus_two_cnt, self._player_hands

    def is_end(self) -> bool:
        if self._deck.is_empty():
            return True
        for han in self._player_hands:
            if len(han.get_cards())==0:
                self.the_winner=self._player_hands.index(han)
                return True
        return False
        # YOUR CODE HERE
        pass

    def is_not_end(self) -> bool:
        return not self.is_end()

    def current_player_drop_card(self, card: Card) -> None:
        # YOUR CODE HERE
        self._last_card=card
        self._is_last_player_drop = True
        self._player_hands[self._current_player_id].remove_card(card)
        pass
        
    def get_scores(self) -> List[int]:
        self.scores_list=[]
        for cardsI in self._player_hands:
            scores=0
            for cardII in cardsI.get_cards():
                if isinstance(cardII,NumericCard):
                    scores+=cardII.get_number()
                elif isinstance(cardII,SpecialCard):
                    scores+=(cardII.get_effect()+1)*10
            self.scores_list.append(scores)
        return self.scores_list
        # YODE HERE
        pass
    
    def get_winner(self) -> int:
        if self.is_not_end():
            raise Exception("Game is not end")
        else:
            if self._deck.is_empty():
                min_value = min(self.get_scores())  # 获取列表中的最小值
                return self.get_scores().index(min_value)
            else:
                for han in self._player_hands:
                    if len(han.get_cards())==0:
                        self.the_winner=self._player_hands.index(han)
                return self.the_winner

        
        # YOUR CODE HERE
    
    def turn(self) -> Tuple[Tuple[ActionType, Card | None], Tuple[int, Card, bool, int, List[Hand]], bool]:
        if self.is_end():
            raise Exception("Game is end")
        
        self._current_player_id = (self._current_player_id + 1) % len(self._players)
        action = self._players[self._current_player_id].action(
            self._player_hands[self._current_player_id].get_cards(), self._last_card, self._is_last_player_drop)
            
        if action[0] == ActionType.DRAW:
            # YOUR CODE HERE
            self._player_hands[self._current_player_id].add_card(self._deck.get_next_card())
            self._is_last_player_drop=False
        elif action[0] == ActionType.DROP:
            self.current_player_drop_card(action[1])
            if isinstance(action[1],SpecialCard):
                if action[1].get_effect()==2:
                    self._plus_two_cnt+=1

            # What do you still need to do here?
            # YOUR CODE HERE

        elif action[0] == ActionType.PASS:
            # YOUR CODE HERE
            if isinstance(self._last_card,SpecialCard) and self._last_card.get_effect()==2:
                for i in range(0,2*self._plus_two_cnt):
                  self._player_hands[self._current_player_id].add_card(self._deck.get_next_card())
                  if self._deck.is_empty():
                      break
                self._plus_two_cnt=0
            self._is_last_player_drop=False
        else:
            raise Exception("Invalid Action")
        
        return action, self.get_info(), self.is_not_end()

def Action_test():
    action_type_list = [0, 0, 0]
    m_card_list = [0, 0, 0]
    cards = [NumericCard(Color.WHITE, 5), NumericCard(Color.PURPLE, 1), 
             SpecialCard(Color.BLUE, Effect.PLUS_TWO)]
    player_ex = Player()
    action_type_list[0], m_card_list[0] = player_ex.action(cards, NumericCard(Color.BLACK, 13), False)
    action_type_list[1], m_card_list[1] = player_ex.action(cards, SpecialCard(Color.BLUE, Effect.BAN), False)
    action_type_list[2], m_card_list[2] = player_ex.action(cards, SpecialCard(Color.VIOLET, Effect.BAN), True)
    for action in action_type_list:
        action = action.value

    action_ans = [action_type_list[0].value, action_type_list[1].value, action_type_list[2].value]

    if action_ans == [0, 1, 2] and m_card_list == [None, SpecialCard(Color.BLUE, Effect.PLUS_TWO), None]:
        print("Action test passed")
    else:
        print("Action test failed.")
        print(f"This means that your function for player action may not work correctly.")
        print("We provide three actions in this test.")
        print(f"The expected action types are [0, 1, 2], yours are {action_ans}")
        print(f"The expected card are [None, PLUS_TWO card BLUE, None], yours are {m_card_list}")


if __name__ == "__main__":
    # If you need a traceback (i.e. tell you where your code is crashed), 
    # you can simply delete this try-except block.
    try:
        Action_test()

    except Exception as e:
        print(e)
        print("Code cannot be runned. May cause Runtime Error (Hangup) on OJ.")
