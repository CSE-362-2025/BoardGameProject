## Design Decisions

### StopTile

- Can be either a decision event or a static event
- Can fail the criteria which displays a message 

### EventTile

- Will have three tiers of rarity (2: common, 1: rare, 0: super rare)
- Must produce an event so must grab an event then check the criteria and then pull another if fails
- Each choice has a hide field, if hide is true, the choice will not be shown to the player if the player does not have the required stats. If false, it will be showed and grayed out.

### Player

- for events_played, choice_idx will be 0 if it is a non-decision event

### Good/BadTile

- I'm going with each tile generates a random effect

## To-do

- Need to add a way for an event to have the criteria and then display another result and message if failes the criteria for the event. This will need some restructuring of the event class.

- Add a way to move in a different direction after a stop tile.

- Add "summer" events that can only happen when waiting for other players to finish the board. (not priority)

- Make a way for different boards to be in the game.

- Make it so all options are shown but only the options you can do based on your stats can be chosen

- Make interaction between players for event choices.

- Some character customization regarding stats and player image. (not priority)
