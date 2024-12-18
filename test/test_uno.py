import sys
import os
from server.py.uno import GameState, GamePhase, Uno, LIST_CARD, PlayerState, Card, Action

# Add the root project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test for creating a new GameState instance
def test_create():
    game_state = GameState()
    assert game_state.phase == GamePhase.SETUP

# Test for initializing the game state
def test_initialize():
    game_state = GameState()
    game_state.initialize()
    assert game_state.phase == GamePhase.RUNNING

# Test for creating and initializing a game
def test_create_game():
    game = Uno()
    init_state = GameState()

    game.set_state(init_state)
    state = game.get_state()
    assert state.phase == GamePhase.RUNNING

# Test for moving one card and validating the actions available
def test_move_one_card():
    game = Uno()
    init_state = GameState(
        cnt_player=2,
        list_card_draw=[Card(color='green', number=3)],
        list_player=[
            PlayerState(
                list_card=[
                    Card(color='red', number=1),
                    Card(color='red', number=2),
                    Card(color='red', number=3),
                ]
            ),
            PlayerState(
                list_card=[
                    Card(color='blue', number=1),
                    Card(color='blue', number=2),
                    Card(color='blue', number=3),
                ]
            ),
        ],
    )

    game.set_state(init_state)

    # Expected actions for the first player's turn
    expected_actions = [
        Action(card=None, color=None, draw=1, uno=False),
        Action(card=Card(color='red', number=3, symbol=None), color='red'),
    ]

    assert sorted(expected_actions) == sorted(game.get_list_action())

# Test for a player having all special cards and the actions available
def test_have_all_special_card():
    game = Uno()
    init_state = GameState(
        cnt_player=2,
        list_card_draw=[Card(color='green', number=3)],
        list_player=[
            PlayerState(
                list_card=[
                    Card(color='red', symbol='skip'),
                    Card(color='red', symbol='reverse'),
                    Card(color='red', symbol='draw2'),
                    Card(color='any', symbol='wild'),
                    Card(color='any', symbol='wilddraw4'),
                ]
            ),
            PlayerState(
                list_card=[
                    Card(color='blue', number=1),
                    Card(color='blue', number=2),
                    Card(color='blue', number=3),
                ]
            ),
        ],
    )

    game.set_state(init_state)

    # Actions corresponding to the special cards in hand
    expected_actions = [
        Action(card=None, color=None, draw=1, uno=False),
        Action(card=Card(color='red', number=None, symbol='draw2'), color='any', draw=2, uno=False),
        Action(card=Card(color='any', number=None, symbol='wild'), color='red', draw=None, uno=False),
        Action(card=Card(color='any', number=None, symbol='wild'), color='green', draw=None, uno=False),
        Action(card=Card(color='any', number=None, symbol='wild'), color='yellow', draw=None, uno=False),
        Action(card=Card(color='any', number=None, symbol='wild'), color='blue', draw=None, uno=False),
        Action(card=Card(color='any', number=None, symbol='wilddraw4'), color='red', draw=4, uno=False),
        Action(card=Card(color='any', number=None, symbol='wilddraw4'), color='green', draw=4, uno=False),
        Action(card=Card(color='any', number=None, symbol='wilddraw4'), color='yellow', draw=4, uno=False),
        Action(card=Card(color='any', number=None, symbol='wilddraw4'), color='blue', draw=4, uno=False)
    ]

    assert sorted(expected_actions) == sorted(game.get_list_action())

# Test for each special card (skip, reverse, draw2, wild, wilddraw4)
def test_all_special_card():
    top_card_actions = [
        (
            Card(color='red', symbol='skip', ),
            [Action(card=None, color=None, draw=1, uno=False)],

        ),
        (
            Card(color='red', symbol='reverse', ),
            [Action(card=None, color=None, draw=1, uno=False)]
        ),
        (
            Card(color='red', symbol='draw2', ),
            [Action(card=None, color=None, draw=2, uno=False)]
        ),
        (
            Card(color='any', symbol='wild', ),
            [
                Action(card=Card(color='green', number=1, symbol=None), color='green', draw=None, uno=False),
                Action(card=Card(color='green', number=2, symbol=None), color='green', draw=None, uno=False),
                Action(card=Card(color='green', number=3, symbol=None), color='green', draw=None, uno=False),
            ]
        ),
        (
            Card(color='any', symbol='wilddraw4', ),
            [Action(card=None, color=None, draw=1, uno=False)]
        ),
    ]
    for top_card, expected_actions in top_card_actions:
        game = Uno()
        init_state = GameState(
            cnt_player=2,
            list_card_draw=[Card(color='red', number=7), top_card],
            list_player=[
                PlayerState(
                    list_card=[
                        Card(color='green', number=1),
                        Card(color='green', number=2),
                        Card(color='green', number=3),
                    ]
                ),
                PlayerState(
                    list_card=[
                        Card(color='blue', number=1),
                        Card(color='blue', number=2),
                        Card(color='blue', number=3),
                    ]
                ),
            ],
        )

        game.set_state(init_state)
        # print(top_card)
        # print(game.get_list_action())

        assert sorted(expected_actions) == sorted(game.get_list_action())

# Define test cases for top cards (skip, reverse, draw2) and their expected actions
def test_skip_reverse_draw2():
    top_card_actions = [
        (
            Card(color='red', symbol='skip', ),
            [
                Action(card=None, color=None, draw=1, uno=False),
                Action(card=Card(color='blue', number=None, symbol='skip'), color='blue', draw=None, uno=False)
            ],

        ),
        (
            Card(color='red', symbol='reverse', ),
            [
                Action(card=None, color=None, draw=1, uno=False),
                Action(card=Card(color='green', number=None, symbol='reverse'), color='green', draw=None, uno=False),
            ]
        ),
        (
            Card(color='red', symbol='draw2', ),
            [
                Action(card=None, color=None, draw=2, uno=False),
                Action(card=Card(color='green', number=None, symbol='draw2'), color='green', draw=4, uno=False),
            ]
        ),
    ]
    for top_card, expected_actions in top_card_actions:
        game = Uno()
        init_state = GameState(
            cnt_player=2,
            list_card_draw=[Card(color='red', number=7), top_card],
            list_player=[
                PlayerState(
                    list_card=[
                        Card(color='green', symbol='skip'),
                        Card(color='green', symbol='reverse'),
                        Card(color='green', symbol='draw2'),
                    ]
                ),
                PlayerState(
                    list_card=[
                        Card(color='blue', symbol='skip'),
                        Card(color='blue', symbol='reverse'),
                        Card(color='blue', symbol='draw2'),
                    ]
                ),
            ],
        )

        game.set_state(init_state)
        print(top_card)
        print(game.get_list_action())

        # Assert that the expected actions match the actual actions in the game
        assert sorted(expected_actions) == sorted(game.get_list_action())

# Additional tests for applying cards and Uno behavior
def test_apply_one_card():
    game = Uno()
    init_state = GameState(
        cnt_player=2,
        list_card_draw=LIST_CARD[:] + [Card(color='green', number=3)],
        list_player=[
            PlayerState(
                list_card=[
                    Card(color='red', number=1),
                    Card(color='red', number=2),
                    Card(color='red', number=3),
                ]
            ),
            PlayerState(
                list_card=[
                    Card(color='blue', number=1),
                    Card(color='blue', number=2),
                    Card(color='blue', number=3),
                ]
            ),
        ],
    )

    game.set_state(init_state)

    expected_actions = [
        Action(card=None, color=None, draw=1, uno=False),
        Action(card=Card(color='red', number=3, symbol=None), color='red'),
    ]

    assert sorted(expected_actions) == sorted(game.get_list_action())

    game.apply_action(expected_actions[0])

    assert len(init_state.list_player[0].list_card) == 4

# Ensure calling Uno applies the rule correctly
def test_apply_one_uno():
    game = Uno()
    init_state = GameState(
        cnt_player=2,
        list_card_draw=LIST_CARD[:] + [Card(color='green', number=1)],
        list_player=[
            PlayerState(
                list_card=[
                    Card(color='red', number=1),
                    Card(color='red', number=2),
                ]
            ),
            PlayerState(
                list_card=[
                    Card(color='blue', number=1),
                    Card(color='blue', number=2),
                    Card(color='blue', number=3),
                ]
            ),
        ],
    )

    game.set_state(init_state)

    expected_actions = [
        Action(card=Card(color='red', number=1, symbol=None), color='red', uno=True),
        Action(card=None, color=None, draw=1, uno=False),
        Action(card=Card(color='red', number=1, symbol=None), color='red'),
    ]
    print(game.get_list_action())
    assert sorted(expected_actions) == sorted(game.get_list_action())

    game.apply_action(expected_actions[0])

    assert len(init_state.list_player[0].list_card) == 1
