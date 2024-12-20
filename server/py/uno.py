import random
from enum import Enum
from typing import List, Optional, Any, Union
from pydantic import BaseModel, Field
from server.py.game import Game, Player


class Card(BaseModel):
    """
    Represents a single UNO card.
    
    This class holds the color, number, and symbol of a UNO card.
    """
    color: str = ""               # color of the card (see LIST_COLOR)
    number: Optional[int] = None  # number of the card (if not a symbol card)
    symbol: Optional[str] = None  # special cards (see LIST_SYMBOL)

    def __lt__(self, other: Union['Card', Any]) -> bool:
        """
        Check if this Card object is less than another Card object.

        The comparison is done by comparing the color, number, and symbol 
        of both cards in sequence. If one card has None in a field where 
        the other has a value, the card with None is considered smaller.
        """
        if not isinstance(other, Card):
            return False

        t1 = (self.color, self.number, self.symbol,)
        t2 = (other.color, other.number, other.symbol,)
        v1: Any
        v2: Any
        for v1, v2 in zip(t1, t2):
            if v1 is None and v2 is None:
                continue

            if v1 is None:
                return True

            if v2 is None:
                return False

            if v1 < v2:
                return True

        return False

    def __eq__(self, other:Any)-> bool:
        """
        Check if two Card objects are equal.

        Equality is determined by comparing their color, number, and symbol.
        """
        if not isinstance(other, Card):
            return False

        t1 = (self.color, self.number, self.symbol,)
        t2 = (other.color, other.number, other.symbol,)

        return t1 == t2

class Action(BaseModel):
    """
    Represents an action a player can take.

    An action may involve playing a card, choosing a color, drawing cards for the next player, 
    and announcing "UNO" if the player is about to go down to their last card.
    """
    card: Optional[Card] = None  # the card to play
    color: Optional[str] = None  # the chosen color to play (for wild cards)
    draw: Optional[int] = None   # number of cards to draw for the next player
    uno: bool = False            # announce "UNO" with the second last card

    def __lt__(self, other: Union['Action', Any]) -> bool:
        """
        Method checks if one Card object is less than another one, uses global method lt().
        """
        if not isinstance(other, Action):
            return False

        t1: tuple[Card | None, str | None, int | None, bool] = (self.card, self.color, self.draw, self.uno,)
        t2: tuple[Card | None, str | None, int | None, bool] = (other.card, other.color, other.draw, other.uno,)
        v1: Any
        v2: Any
        for v1, v2 in zip(t1, t2):
            if v1 is None and v2 is None:
                continue

            if v1 is None:
                return True

            if v2 is None:
                return False

            if v1 < v2:
                return True

        return False

class PlayerState(BaseModel):
    """
    Represents the state of a single UNO player.

    Contains the player's name, the list of cards they hold, their current score, 
    and the last action they performed.
    """

    name: Optional[str] = None  # name of player
    list_card: List[Card] = Field(default_factory=list)  # list of cards
    score: int =0 # extended attribute
    last_action: Optional[Action]=None #extended attribute

    def __str__(self) -> str:  #debug function
        """
        Return a debug string representtaion of the PlayerState.
        The string displays the player's cards, score, and the last action performed.
        """
        tabs = '\n\t\t\t'
        return (f"\tPlayer(\n"
                f"\t\tlist_card=\n\t\t\t{tabs.join(map(repr, self.list_card))}"
                f"\t\tscore={self.score}\n"
                f"\t\tlast_action={repr(self.last_action)}\n"
                f"\t)")


class GamePhase(str, Enum):
    """Enumerates the different phases of the game.
    """
    SETUP = 'setup'            # before the game has started
    RUNNING = 'running'        # while the game is running
    FINISHED = 'finished'      # when the game is finished

NOT_SET_DIRECTION = -10
"""An integer constant indicating that the playing direction has not yet been set."""

NOT_SET_CNT_TO_DRAW = -10
"""An integer constant indicating that the number of cards to draw is not set."""

LIST_COLOR: List[str] = ['red', 'green', 'yellow', 'blue', 'any']
"""
A list of valid UNO card colors.

Order:
- red
- green
- yellow
- blue
- any (used for wild cards)
"""

# draw2 = draw two cards, wild = chose color, wilddraw4 = chose color and draw 4
LIST_SYMBOL: List[str] = ['skip', 'reverse', 'draw2', 'wild', 'wilddraw4']
"""
A list of special symbols representing non-numbered UNO cards.

Includes:
- skip: skip the next player's turn
- reverse: reverse the playing direction
- draw2: next player must draw two cards
- wild: current player chooses the next color to play
- wilddraw4: current player chooses the next color, and next player draws four cards
"""

LIST_CARD: List[Card] = [
    Card(color='red', number=0), Card(color='green', number=0), Card(color='yellow', number=0),
    Card(color='blue', number=0),
    Card(color='red', number=1), Card(color='green', number=1), Card(color='yellow', number=1),
    Card(color='blue', number=1),
    Card(color='red', number=2), Card(color='green', number=2), Card(color='yellow', number=2),
    Card(color='blue', number=2),
    Card(color='red', number=3), Card(color='green', number=3), Card(color='yellow', number=3),
    Card(color='blue', number=3),
    Card(color='red', number=4), Card(color='green', number=4), Card(color='yellow', number=4),
    Card(color='blue', number=4),
    Card(color='red', number=5), Card(color='green', number=5), Card(color='yellow', number=5),
    Card(color='blue', number=5),
    Card(color='red', number=6), Card(color='green', number=6), Card(color='yellow', number=6),
    Card(color='blue', number=6),
    Card(color='red', number=7), Card(color='green', number=7), Card(color='yellow', number=7),
    Card(color='blue', number=7),
    Card(color='red', number=8), Card(color='green', number=8), Card(color='yellow', number=8),
    Card(color='blue', number=8),
    Card(color='red', number=9), Card(color='green', number=9), Card(color='yellow', number=9),
    Card(color='blue', number=9),
    Card(color='red', number=1), Card(color='green', number=1), Card(color='yellow', number=1),
    Card(color='blue', number=1),
    Card(color='red', number=2), Card(color='green', number=2), Card(color='yellow', number=2),
    Card(color='blue', number=2),
    Card(color='red', number=3), Card(color='green', number=3), Card(color='yellow', number=3),
    Card(color='blue', number=3),
    Card(color='red', number=4), Card(color='green', number=4), Card(color='yellow', number=4),
    Card(color='blue', number=4),
    Card(color='red', number=5), Card(color='green', number=5), Card(color='yellow', number=5),
    Card(color='blue', number=5),
    Card(color='red', number=6), Card(color='green', number=6), Card(color='yellow', number=6),
    Card(color='blue', number=6),
    Card(color='red', number=7), Card(color='green', number=7), Card(color='yellow', number=7),
    Card(color='blue', number=7),
    Card(color='red', number=8), Card(color='green', number=8), Card(color='yellow', number=8),
    Card(color='blue', number=8),
    Card(color='red', number=9), Card(color='green', number=9), Card(color='yellow', number=9),
    Card(color='blue', number=9),
    # skip next player
    Card(color='red', symbol='skip'), Card(color='green', symbol='skip'), Card(color='yellow', symbol='skip'),
    Card(color='blue', symbol='skip'),
    Card(color='red', symbol='skip'), Card(color='green', symbol='skip'), Card(color='yellow', symbol='skip'),
    Card(color='blue', symbol='skip'),
    # revers playing direction
    Card(color='red', symbol='reverse'), Card(color='green', symbol='reverse'),
    Card(color='yellow', symbol='reverse'),
    Card(color='blue', symbol='reverse'),
    Card(color='red', symbol='reverse'), Card(color='green', symbol='reverse'),
    Card(color='yellow', symbol='reverse'),
    Card(color='blue', symbol='reverse'),
    # next player must draw 2 cards
    Card(color='red', symbol='draw2'), Card(color='green', symbol='draw2'), Card(color='yellow', symbol='draw2'),
    Card(color='blue', symbol='draw2'),
    Card(color='red', symbol='draw2'), Card(color='green', symbol='draw2'), Card(color='yellow', symbol='draw2'),
    Card(color='blue', symbol='draw2'),
    # current player choses color for next player to play
    Card(color='any', symbol='wild'), Card(color='any', symbol='wild'),
    Card(color='any', symbol='wild'), Card(color='any', symbol='wild'),
    # current player choses color for next player to play and next player must draw 4 cards
    Card(color='any', symbol='wilddraw4'), Card(color='any', symbol='wilddraw4'),
    Card(color='any', symbol='wilddraw4'), Card(color='any', symbol='wilddraw4'),
]
"""
A comprehensive list representing a standard UNO deck of cards.

- Contains all number cards from 0-9 in four colors (red, green, yellow, blue).
- Includes duplicates to match a standard UNO deck composition.
- Contains special cards: skip, reverse, draw2 (for each color),
  and wild, wilddraw4 (color 'any').
"""

class GameState(BaseModel):
    """Represents the overall state of the UNO game, including decks,
    discard piles, players, and the current game phase.
    
    """
    # numbers of cards for each player to start with
    CNT_HAND_CARDS: int = 7

    list_card_draw: Optional[List[Card]] = None  # list of cards to draw
    list_card_discard: Optional[List[Card]] = None
    list_player: Optional[List[PlayerState]] = None
    phase: GamePhase = GamePhase.SETUP
    cnt_player: int = -1
    idx_player_active: Optional[int] = None
    direction: int = NOT_SET_DIRECTION
    color: str = ""
    cnt_to_draw: int = NOT_SET_CNT_TO_DRAW
    has_drawn: bool = False
    card_was_used: bool = False

    def initialize(self) -> None:
        """Initialize the game state when the phase is setup."""
        if not self.list_card_draw:
            self.initialize_list_card_draw()

        if self.cnt_player == -1:
            self.cnt_player = 2

        if not self.list_player:
            self.deal_cards()

        if not self.list_card_discard:
            self.initialize_list_card_discard()

        if self.list_card_discard is None:
            raise ValueError()
        top_card = self.list_card_discard[-1]

        self.reverse_direction(top_card)

        self.initialize_idx_player(top_card)

        self.initialize_cnt_to_draw(top_card)

        self.initialize_has_drawn()

        self.phase = GamePhase.RUNNING

    def initialize_has_drawn(self) -> None:
        """Initialize the has_drawn flag if needed."""
        if self.has_drawn is None:
            self.has_drawn = False


    def initialize_cnt_to_draw(self, top_card: Card) -> None:
        """Initialize how many cards the next player must draw, if any."""
        if self.cnt_to_draw == NOT_SET_CNT_TO_DRAW and top_card.symbol is None:
            self.cnt_to_draw = 0
        elif self.cnt_to_draw == NOT_SET_CNT_TO_DRAW and top_card.symbol is not None:
            self.cnt_to_draw = 0
            if top_card.symbol == "draw2":
                self.cnt_to_draw = 2


    def initialize_idx_player(self, top_card: Card) -> None:
        """Initialize the index of the active player based on the top card."""
        if (self.idx_player_active is None) and (top_card.symbol is None):
            self.idx_player_active = 0
        elif (self.idx_player_active is None) and (top_card.symbol is not None):
            self.idx_player_active = 0
            if top_card.symbol == 'skip':
                self.idx_player_active = (self.idx_player_active + self.direction) % self.cnt_player
        elif (self.idx_player_active is not None) and (top_card.symbol is not None):
            # self.idx_player_active = 0
            if top_card.symbol == 'skip':
                self.idx_player_active = (self.idx_player_active + self.direction) % self.cnt_player


    def get_current_player(self) -> PlayerState:
        """Return the currently active player."""
        if self.list_player is None or self.idx_player_active is None:
            raise ValueError()
        return self.list_player[self.idx_player_active]


    def deal_cards(self) -> None:
        """Deal cards to each player at the start of the game."""
        if self.list_card_draw is None:
            raise ValueError()
        self.list_player = [PlayerState() for i in range(self.cnt_player)]
        player: PlayerState
        for i in range(self.CNT_HAND_CARDS):
            for player in self.list_player:
                player.list_card.append(self.list_card_draw.pop())


    def initialize_list_card_draw(self) -> None:
        """Initialize the draw pile with shuffled cards."""
        self.list_card_draw = LIST_CARD[:]
        random.shuffle(self.list_card_draw)


    def next_player(self) -> None:
        """Advance to the next player."""
        if self.idx_player_active is None:
            raise ValueError()
        self.idx_player_active = (self.idx_player_active + self.direction) % self.cnt_player


    def reverse_direction(self, top_card: Card) -> None:
        """Sets the game direction based on the `top_card` symbol if the direction is not yet set."""
        if self.direction == NOT_SET_DIRECTION and top_card.symbol is None:
            self.direction = 1
        elif self.direction == NOT_SET_DIRECTION and top_card.symbol is not None:
            if top_card.symbol == 'reverse':
                self.direction = -1
            else:
                self.direction = 1

    def initialize_list_card_discard(self) -> None:
        """Initialize the discard pile with a valid starting card."""
        self.list_card_discard = []
        while True:
            if self.list_card_draw is None:
                raise ValueError()
            top_card = self.list_card_draw.pop()

            if top_card.symbol == 'wilddraw4':
                index = random.randint(0, len(self.list_card_draw))
                self.list_card_draw.insert(index, top_card)
                continue
            if top_card.symbol == 'draw2':
                self.cnt_to_draw = 2

            self.list_card_discard.append(top_card)
            self.color = top_card.color
            break


    def __str__(self) -> str:
        """Return a string representation of the current game state for debugging."""
        if self.idx_player_active is None or self.list_card_discard is None or self.list_player is None:
            raise ValueError()

        return (f"(\n"
                f"\tlist_card_discard={list(reversed(self.list_card_discard))}\n"
                f"\ttop_card={repr(self.list_card_discard[-1])}\n"
                f"\tcurrent_inx={self.idx_player_active}\n"
                f"\tcurrent_player={self.list_player[self.idx_player_active]}\n"
                f"\tnext_player={self.list_player[(self.idx_player_active + self.direction) % self.cnt_player]}\n"
                f"\tcurrent_color={self.color}\n"
                f")")

class Uno(Game):
    """Represents the UNO game logic, managing the state and player actions."""

    def __init__(self) -> None:
        """ Important: Game initialization also requires a 
        set_state call to set the number of players """
        self.state = GameState()

    def get_state(self) -> GameState:
        """ Get the complete, unmasked game state """
        return self.state

    def set_state(self, state: GameState) -> None:
        """ Set the game to a given state """
        self.state = state

        if self.state.phase == GamePhase.SETUP:
            self.state.initialize()

    def get_list_action(self) -> List[Action]:
        """ Get a list of possible actions for the active player """

        # Ensure there is a discard pile to check the top card from
        if self.state.list_card_discard is None:
            raise ValueError()

        # Get the top card of the discard pile to determine valid moves
        top_card = self.state.list_card_discard[-1]
        current_player = self.state.get_current_player()

        actions = []

        # Determine possible actions based on whether the top card has a symbol or not
        if top_card.symbol is None:
            actions = self._get_list_action_not_specific(top_card)
        else:
            actions = self._get_list_action_specific(top_card)
        # Check if the player has exactly 2 cards in their hand (UNO condition)
        if len(current_player.list_card) == 2:
            result = []
            for action in actions:
                if action.card is None and action.draw != 0:
                    result.append(action)
                elif action.card is not None:
                    result.append(action)
                    result.append(Action(card=action.card, draw=action.draw, color=action.color, uno=True))
                else:
                    result.append(action)
            actions = result

        return actions

    def _get_list_action_not_specific(self, top_card: Card) -> List[Action]:
        """Retrieve actions when the topc card has no special symbol."""
        player_state = self.state.get_current_player()
        actions = []
        if not self.state.has_drawn:
            actions.append(Action(draw=self.state.cnt_to_draw or 1))
        has_color_full_card = self.check_with_simple_cards(player_state, top_card)
        for card in player_state.list_card:
            if card.symbol not in ['wild', 'wilddraw4', 'draw2']:
                if card.color == self.state.color or card.number == top_card.number:
                    actions.append(Action(card=card, color=card.color))
            elif card.symbol == 'wild':
                for color in LIST_COLOR[:-1]:
                    actions.append(Action(card=card, color=color, draw=None))
            elif card.symbol == 'wilddraw4':
                if not has_color_full_card:
                    for color in LIST_COLOR[:-1]:
                        actions.append(Action(card=card, color=color, draw=4))
            elif card.symbol == 'draw2':
                actions.append(Action(card=card, color='any', draw=2))
            else:
                raise ValueError("Unsupported symbol")

        return actions

    def check_with_simple_cards(self, player_state: PlayerState, top_card: Card) -> bool:
        """Check if the player has a card matching the top card's color or number."""
        has_color_card = False
        for card in player_state.list_card:
            if card.symbol not in ['wild', 'wilddraw4']:
                if card.color == self.state.color or card.number == top_card.number:
                    has_color_card = True

        return has_color_card

    def _get_list_action_specific(self, top_card: Card) -> List[Action]:
        """"Retrieve the actions when the top card has a special symbol."""
        player_state = self.state.get_current_player()
        actions = []

        if not self.state.has_drawn:
            actions.append(Action(draw=self.state.cnt_to_draw or 1))

        if top_card.symbol == 'skip':
            self._get_list_action_specific_skip(actions, player_state, top_card)

        if top_card.symbol == 'reverse':
            self._get_list_action_specific_reverse(actions, player_state, top_card)

        if top_card.symbol == 'draw2':
            self._get_list_action_specific_draw2(actions, player_state)

        if top_card.symbol == 'wild':
            self._get_list_action_specific_wild(actions, player_state, top_card)

        if top_card.symbol == 'wilddraw4':
            pass

        return actions

    def _get_list_action_specific_wild(self, actions: List[Action], player_state: PlayerState, top_card: Card) -> None:
        """Handle actions for wild cards."""
        actions.pop()
        for card in player_state.list_card:
            if top_card.color in [card.color, "any", ]:
                if card.symbol is None:
                    actions.append(Action(card=card, color=card.color))
                    actions.append(Action(draw=1))

    def _get_list_action_specific_draw2(self, actions: List[Action], player_state: PlayerState) -> None:
        for card in player_state.list_card:
            if card.symbol == 'draw2':
                actions.append(Action(card=card, color=card.color, draw=self.state.cnt_to_draw + 2))

    def _get_list_action_specific_reverse(self, actions: List[Action], player_state: PlayerState,
                                          top_card: Card) -> None:
        for card in player_state.list_card:
            if card.symbol == 'reverse':
                actions.append(Action(card=card, color=card.color))
            elif card.symbol == 'draw2' and card.color == top_card.color:
                actions.append(Action(card=card, color=card.color, draw=2))


    def _get_list_action_specific_skip(self, actions: List[Action], player_state: PlayerState, top_card: Card) -> None:
        for card in player_state.list_card:
            if card.symbol == 'skip':
                actions.append(Action(card=card, color=card.color))
            elif card.symbol == 'reverse' and card.color == top_card.color:
                actions.append(Action(card=card, color=card.color))

    def apply_action(self, action: Action) -> None:
        """ Apply the given action to the game """

        player = self.state.get_current_player()
        if len(player.list_card) == 2 and not action.uno and action.card is not None:
            if self.state.list_card_draw is None:
                raise ValueError
            player.list_card.extend([self.state.list_card_draw.pop() for _ in range(4)])

        if action.card is None and action.draw != 0:
            player = self.state.get_current_player()
            if action.draw is None or self.state.list_card_draw is None:
                raise ValueError
            player.list_card.extend([self.state.list_card_draw.pop() for _ in range(action.draw)])
            self.state.has_drawn = True
            self.state.cnt_to_draw = 0
            return

        if action.card is not None:
            if self.state.list_card_draw is None:
                raise ValueError
            self.state.list_card_draw.append(action.card)
            player.list_card.remove(action.card)
            self.state.cnt_to_draw = action.draw or 0
            if action.card.symbol == 'skip':
                self.state.next_player()

            if len(player.list_card) == 0:
                self.state.phase = GamePhase.FINISHED
                return

        self.state.next_player()


    def print_state(self) -> None:
        """ Print the current game state for debbuging"""
        if not self.state:
            print("Game state has not been initialized")
            return
        print("\n==== Game State ====")
        print(f"Phase: {self.state.phase}")
        print(f"""Direction: {
            'Clockwise' if self.state.direction == 1 else 'Counterclockwise'
            }""")
        print(f"Active Player Index: {self.state.idx_player_active}")
        print(f"Active Color: {self.state.color}")
        print(f"Cards to Draw: {self.state.cnt_to_draw}")
        print(f"Has Drawn: {'Yes' if self.state.has_drawn else 'No'}")
        print("\n-- Players --")
        print("\n-- Discard Pile --")
        if self.state.list_card_discard:
            print(f"Top Card: {self.state.list_card_discard[-1]}")
        else:
            print("Discard pile is empty.")
        print("====================\n")

    def get_player_view(self, idx_player: int) -> GameState:
        """ Get the masked state for the active player (e.g. the oppontent's cards are face down)"""
        return GameState(cnt_player=idx_player)


class RandomPlayer(Player):
    def select_action(self, state: GameState, actions: List[Action]) -> Optional[Action]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0 and state:
            return random.choice(actions)
        return None

    def game_is_running(self) -> bool:
        return True
