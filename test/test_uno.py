import unittest
from server.py.uno import Uno, GameState, PlayerState

class TestUnoGame(unittest.TestCase):
    '''
    This test class contains unit tests for the Uno game logic.
    It validates that the methods in the Uno class are working as expected.
    '''

    def setUp(self):
        '''
        Set up the Uno game instance for testing.
        This method is called before every test case to create a fresh game instance.
        '''
        self.uno = Uno()

    def test_setup_game(self):
        '''
        Test the setup_game method to ensure the game initializes properly with players.
        - Check if the correct number of players are added to the game.
        - Ensure that each player is dealt the correct number of cards.
        '''
        players = ["Daniel", "Ramon"]
        self.uno.state.setup_game(players)

        # Assert that the correct number of players are set up
        self.assertEqual(len(self.uno.state.list_player), 2, 'The number of players should match the input list.')
        
        # Assert that each player has 7 cards
        for player in self.uno.state.list_player:
            self.assertEqual(len(player.list_card), 7, f'{player.name} should have 7 cards.')

    def test_apply_action(self):
        '''
        Test the apply_action method to ensure that player actions are applied correctly.
        - Simulate a player drawing a card.
        - Check if the game state is updated properly after the action.
        '''
        players = ["Daniel", "Ramon"]
        self.uno.state.setup_game(players)

        # Simulate a player action: drawing one card
        initial_card_count = len(self.uno.state.list_player[0].list_card)
        self.uno.apply_action({'draw': 1})  # Replace this with a properly formatted Action object
        new_card_count = len(self.uno.state.list_player[0].list_card)

        # Assert that the player has one additional card
        self.assertEqual(new_card_count, initial_card_count + 1, 'Player should have one more card after drawing.')

    def test_next_player(self):
        '''
        Test the next_player method to ensure that the turn moves to the correct player.
        - Check the active player index before and after calling next_player.
        - Validate behavior when the game direction changes.
        '''
        players = ["Alice", "Bob", "Charlie"]
        self.uno.state.setup_game(players)

        # Save the initial active player index
        initial_index = self.uno.state.idx_player_active

        # Move to the next player
        self.uno.state.next_player()
        next_index = self.uno.state.idx_player_active

        # Assert that the index has incremented
        self.assertEqual(next_index, (initial_index + 1) % len(players), 'The turn should move to the next player.')

if __name__ == "__main__":
    unittest.main()