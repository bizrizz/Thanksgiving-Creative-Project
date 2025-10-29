# Platformer Game - Haudenosaunee Thanksgiving Address

This enhanced platformer game incorporates the traditional Haudenosaunee Thanksgiving Address through collectible items that must be gathered before advancing to the next level.

## New Features

### Collectible System
Each level now contains a special collectible that represents a different aspect of the Haudenosaunee Thanksgiving Address:

1. **Level 1 - The People (Onkwe'shón:'a)** 🪶
   - **Collectible**: Unity Symbol (glowing golden circle)
   - **Message**: "We will wrap our minds as one and thank/honor All the People..."
   - **Gameplay**: Cooperation-themed platforms requiring teamwork

2. **Level 2 - Our Mother the Earth (Yethi'nihsténha Ohwéntsya)** 🌎
   - **Collectible**: Heart of the Earth (glowing green crystal)
   - **Message**: "We will wrap our minds as one and thank/honor Our Mother the Earth..."
   - **Gameplay**: Earth restoration with healing elements

3. **Level 3 - The Waters (Kahnekarónnyon)** 💧
   - **Collectible**: Water Drop Spirit (glowing blue crystal)
   - **Message**: "We will wrap our minds as one and thank/honor The Waters..."
   - **Gameplay**: Flowing platforms representing water movement

4. **Level 4 - The Plant World (Sa'oyé:ra Yonthontón:nis)** 🌿
   - **Collectible**: Three Sisters Seed (glowing green crystal)
   - **Message**: "We will wrap our minds as one and thank/honor Everything Natural Growing..."
   - **Gameplay**: Vertical growth platforms representing plant life

5. **Level 5 - The Animal World (Yónnhe Tkontinákerake)** 🐾
   - **Collectible**: Sacred Feather (glowing purple crystal)
   - **Message**: "We will wrap our minds as one and thank/honor All the Life Running About..."
   - **Gameplay**: Flying platforms and animal-themed elements

6. **Level 6 - The Sky World (Skátne Yotiyo'tátye Tsi Tkaronhyá:te)** ☀️
   - **Collectible**: Star Crystal (glowing orange crystal)
   - **Message**: "We will wrap our minds as one and thank/honor Everything Working Together in the Sky..."
   - **Gameplay**: Sky-themed platforms with celestial elements

7. **Level 7 - The Creator (Shonkwaya'tíson)** ✨
   - **Collectible**: Sacred Flame (glowing red crystal)
   - **Message**: "We will wrap our minds as one and thank/honor The Creator..."
   - **Gameplay**: Final level combining all previous elements

### Gameplay Changes

- **Required Collectibles**: Players must collect the level's special collectible before they can exit to the next level
- **On-Screen Messages**: When a collectible is collected, the corresponding Thanksgiving Address message is displayed
- **Visual Feedback**: Collectibles have glowing effects and unique colors for each level
- **Final Message**: After completing all levels, players see the traditional closing message

### Technical Implementation

- **New Tile Type**: Added tile type 9 for level collectibles
- **Enhanced Level Editor**: Updated to support placing collectible tiles
- **Message System**: Implemented overlay system for displaying Thanksgiving Address text
- **Level Generation**: Created script to generate themed levels with appropriate collectibles

## Files

- `platformer_with_collectibles.py` - Main game with collectible system
- `level_editor.py` - Updated level editor supporting collectibles
- `create_levels.py` - Script to generate level data with collectibles
- `level1_data` through `level7_data` - Level data files with collectibles

## How to Play

1. Run `python3 platformer_with_collectibles.py`
2. Navigate through each level
3. Collect the glowing collectible (required to advance)
4. Read the Thanksgiving Address message that appears
5. Reach the exit to proceed to the next level
6. Complete all 7 levels to see the final message

## Controls

- **Arrow Keys**: Move left/right
- **Space**: Jump
- **Space**: Dismiss message boxes
- **Mouse**: Menu navigation

The game now serves as an interactive way to experience the Haudenosaunee Thanksgiving Address, with each level teaching about different aspects of gratitude and interconnectedness.
