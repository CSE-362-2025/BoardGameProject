## Design Decisions

### StopTile

- Is a decision event with two paths
- Player can choose which path to take

- Switching paths:
    - The "main" path will follow the same 5 -> 6 -> ... -> 11 ect
    - The "alt" path will add 100 to the position 5 -> 106 -> 107 -> ... -> 111 -> 12
    - The player's position will be at 105 after the decision
    - CAN NO LONGER USE THE INDEX OF TILES IN BOARD TO DETERMINE POSITION, MUST ALWAYS ITERATE THROUGH AND SEARCH POSITIONS


### EventTile

- Will have three tiers of rarity (2: common, 1: rare, 0: super rare)
- Must produce an event so must grab an event then check the criteria and then pull another if fails
- Each choice has a hide field, if hide is true, the choice will not be shown to the player if the player does not have the required stats. If false, it will be showed and grayed out.

### Player

- for events_played, choice_idx will be 0 if it is a non-decision event

### Good/BadTile

- I'm going with each tile generates a random effect

### Board

- Tile positions start at 1 and increase sequentially
- Side paths are normal paths + 100 to their position

### Player Interaction

- Have a pool of events that 

### EndScreen

player.awards: Dict of stats with bool
player.end_text: string of unique text

## To-do

- Add a way to move in a different direction after a stop tile. (done ish)

- Add "summer" events that can only happen when waiting for other players to finish the board. (not priority)

- Make a way for different boards to be in the game. (later)

- Make interaction between players for event choices.

- Some character customization regarding stats and player image. (not priority)

- In Event generation function, make it so it remembers what events have been done so that it is fairly balanced

- Grid with x -> positive to right and y -> positive down


- Create boards in board.json minus screen position

- Finish end_game_summary

- Add more goodtile and badtile effects

- 

