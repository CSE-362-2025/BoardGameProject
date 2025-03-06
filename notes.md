## Design Decisions

### StopTile

- Can be either a decision event or a static event
- Can fail the criteria which displays a message 

### EventTile

- Will have three tiers of rarity (2: common, 1: rare, 0: super rare)
- Must produce an event so must grab an event then check the criteria and then pull another if fails

### Player

- for events_played, choice_idx will be 0 if it is a non-decision event

### Good/BadTile

- I'm going with each tile generates a random effect

## To-do

- Need to add a way for an event to have the criteria and then display another result and message if failes the criteria for the event. This will need some restructuring of the event class.
