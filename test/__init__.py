from test.bases import WorldTestBase
from test.general import setup_solo_multiworld
from worlds import AutoWorldRegister


class MZMTestBase(WorldTestBase):
    game = "Metroid Zero Mission"

    def test_default_all_state_can_reach_everything(self):
        """Ensure all state can reach everything and complete the game with the defined options"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            unreachable_regions = []
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                excluded = multiworld.worlds[1].options.exclude_locations.value
                state = multiworld.get_all_state(False)
                for location in multiworld.get_locations():
                    if location.name not in excluded:
                        with self.subTest("Location should be reached", location=location):
                            self.assertTrue(location.can_reach(state), f"{location.name} unreachable")

                for region in multiworld.get_regions():
                    if region.name in unreachable_regions:
                        with self.subTest("Region should be unreachable", region=region):
                            self.assertFalse(region.can_reach(state))
                    else:
                        with self.subTest("Region should be reached", region=region):
                            self.assertTrue(region.can_reach(state))

                with self.subTest("Completion Condition"):
                    self.assertTrue(multiworld.can_beat_game(state))

    def test_always_accessible(self) -> None:
        self.assertTrue(self.can_reach_location("Brinstar Morph Ball"))
        self.assertTrue(self.can_reach_location("Brinstar First Missile"))
