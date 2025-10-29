import pickle

def create_level_with_collectible(level_num, collectible_x=15, collectible_y=5):
    """
    Create a level data array with a collectible placed at the specified position.
    Each level will have basic platforming elements plus the level-specific collectible.
    """
    # Create empty 20x20 grid
    world_data = []
    for row in range(20):
        r = [0] * 20
        world_data.append(r)
    
    # Create boundary walls
    for tile in range(0, 20):
        world_data[19][tile] = 2  # Grass floor
        world_data[0][tile] = 1   # Dirt ceiling
        world_data[tile][0] = 1   # Left wall
        world_data[tile][19] = 1  # Right wall
    
    # Level-specific designs
    if level_num == 1:  # Unity Symbol - The People
        # Create platforms for cooperation puzzle
        world_data[15][5] = 2   # Platform
        world_data[15][6] = 2
        world_data[15][7] = 2
        world_data[12][10] = 2  # Higher platform
        world_data[12][11] = 2
        world_data[12][12] = 2
        world_data[9][14] = 2   # Highest platform
        world_data[9][15] = 2
        world_data[9][16] = 2
        # Add some enemies
        world_data[16][8] = 3
        world_data[13][13] = 3
        # Add coins
        world_data[14][6] = 7
        world_data[11][11] = 7
        world_data[8][15] = 7
        # Place collectible
        world_data[collectible_y][collectible_x] = 9
        # Exit
        world_data[8][18] = 8
        
    elif level_num == 2:  # Heart of the Earth
        # Create earth-themed level with plants and restoration elements
        world_data[15][3] = 2   # Lower platforms
        world_data[15][4] = 2
        world_data[15][5] = 2
        world_data[12][8] = 2   # Middle platforms
        world_data[12][9] = 2
        world_data[12][10] = 2
        world_data[9][13] = 2   # Upper platforms
        world_data[9][14] = 2
        world_data[9][15] = 2
        # Add some lava (dry earth that needs healing)
        world_data[18][6] = 6
        world_data[18][7] = 6
        world_data[18][11] = 6
        world_data[18][12] = 6
        # Add coins (seeds)
        world_data[14][4] = 7
        world_data[11][9] = 7
        world_data[8][14] = 7
        # Place collectible
        world_data[collectible_y][collectible_x] = 9
        # Exit
        world_data[8][17] = 8
        
    elif level_num == 3:  # Water Drop Spirit
        # Create water-themed level with flowing platforms
        world_data[16][4] = 4   # Moving horizontal platforms (water flow)
        world_data[13][7] = 4
        world_data[10][10] = 4
        world_data[7][13] = 4
        # Add some enemies
        world_data[17][6] = 3
        world_data[14][9] = 3
        world_data[11][12] = 3
        # Add coins
        world_data[15][5] = 7
        world_data[12][8] = 7
        world_data[9][11] = 7
        world_data[6][14] = 7
        # Place collectible
        world_data[collectible_y][collectible_x] = 9
        # Exit
        world_data[6][17] = 8
        
    elif level_num == 4:  # Three Sisters Seed
        # Create plant-themed level with vertical growth
        world_data[15][5] = 2   # Base platforms
        world_data[15][6] = 2
        world_data[12][8] = 2   # Growing platforms
        world_data[12][9] = 2
        world_data[12][10] = 2
        world_data[9][11] = 2   # Higher platforms
        world_data[9][12] = 2
        world_data[9][13] = 2
        world_data[6][14] = 2   # Tallest platforms
        world_data[6][15] = 2
        world_data[6][16] = 2
        # Add some enemies
        world_data[16][7] = 3
        world_data[13][11] = 3
        world_data[10][14] = 3
        # Add coins (plant materials)
        world_data[14][6] = 7
        world_data[11][9] = 7
        world_data[8][12] = 7
        world_data[5][15] = 7
        # Place collectible
        world_data[collectible_y][collectible_x] = 9
        # Exit
        world_data[5][18] = 8
        
    elif level_num == 5:  # Sacred Feather
        # Create animal-themed level with flying elements
        world_data[15][3] = 2   # Ground platforms
        world_data[15][4] = 2
        world_data[12][6] = 2   # Mid-air platforms
        world_data[12][7] = 2
        world_data[9][9] = 2    # Higher platforms
        world_data[9][10] = 2
        world_data[6][12] = 2   # Sky platforms
        world_data[6][13] = 2
        world_data[3][15] = 2   # Highest platforms
        world_data[3][16] = 2
        # Add moving platforms (flying animals)
        world_data[14][8] = 5   # Vertical moving platform
        world_data[11][11] = 5
        world_data[8][14] = 5
        # Add enemies (predators)
        world_data[16][5] = 3
        world_data[13][8] = 3
        world_data[10][11] = 3
        world_data[7][14] = 3
        # Add coins
        world_data[14][4] = 7
        world_data[11][7] = 7
        world_data[8][10] = 7
        world_data[5][13] = 7
        world_data[2][16] = 7
        # Place collectible
        world_data[collectible_y][collectible_x] = 9
        # Clear a blocking top platform and reposition exit for better access
        world_data[3][16] = 0
        world_data[2][18] = 0
        world_data[3][17] = 8
        
    elif level_num == 6:  # Star Crystal
        # Create sky-themed level with celestial elements
        world_data[16][2] = 2   # Cloud platforms
        world_data[16][3] = 2
        world_data[13][5] = 2
        world_data[13][6] = 2
        world_data[10][8] = 2
        world_data[10][9] = 2
        world_data[7][11] = 2
        world_data[7][12] = 2
        world_data[4][14] = 2
        world_data[4][15] = 2
        world_data[1][17] = 0   # Clear near exit for access
        world_data[1][18] = 0
        # Add moving platforms (winds)
        world_data[15][7] = 4   # Horizontal moving
        world_data[12][10] = 4
        world_data[9][13] = 4
        world_data[6][16] = 4
        # Add enemies (storms)
        world_data[17][4] = 3
        world_data[14][7] = 3
        world_data[11][10] = 3
        world_data[8][13] = 3
        world_data[5][16] = 3
        # Add coins (stars)
        world_data[15][3] = 7
        world_data[12][6] = 7
        world_data[9][9] = 7
        world_data[6][12] = 7
        world_data[3][15] = 7
        world_data[0][18] = 7
        # Place collectible
        world_data[collectible_y][collectible_x] = 9
        # Exit (move down-left one tile so it isn't blocked by the ceiling)
        world_data[0][19] = 0
        world_data[2][18] = 8
        
    elif level_num == 7:  # Sacred Flame
        # Create final level with all elements combined
        world_data[15][2] = 2   # Base platforms
        world_data[15][3] = 2
        world_data[15][4] = 2
        world_data[12][6] = 2   # Mid platforms
        world_data[12][7] = 2
        world_data[12][8] = 2
        world_data[9][10] = 2   # Higher platforms
        world_data[9][11] = 2
        world_data[9][12] = 2
        world_data[6][14] = 2   # Upper platforms
        world_data[6][15] = 2
        world_data[6][16] = 2
        world_data[3][17] = 2   # Highest platforms
        world_data[3][18] = 2
        world_data[3][19] = 2
        # Add all types of moving platforms
        world_data[14][9] = 4   # Horizontal moving
        world_data[11][12] = 5  # Vertical moving
        world_data[8][15] = 4   # Horizontal moving
        world_data[5][18] = 5   # Vertical moving
        # Add enemies (final challenges)
        world_data[16][5] = 3
        world_data[13][9] = 3
        world_data[10][13] = 3
        world_data[7][17] = 3
        world_data[4][19] = 3
        # Add lava (purification)
        world_data[18][7] = 6
        world_data[18][8] = 6
        world_data[18][13] = 6
        world_data[18][14] = 6
        # Add coins (all previous collectibles represented)
        world_data[14][3] = 7
        world_data[11][7] = 7
        world_data[8][11] = 7
        world_data[5][15] = 7
        world_data[2][18] = 7
        # Place collectible
        world_data[collectible_y][collectible_x] = 9
        # Exit: move left and clear overhead so the player can enter
        world_data[2][19] = 0
        world_data[1][19] = 0
        world_data[1][18] = 0
        world_data[2][18] = 8
    
    return world_data

def main():
    """Generate level data files for all 7 levels with collectibles."""
    for level_num in range(1, 8):
        print(f"Creating level {level_num} data...")
        world_data = create_level_with_collectible(level_num)
        
        # Save the level data
        filename = f'level{level_num}_data'
        with open(filename, 'wb') as f:
            pickle.dump(world_data, f)
        
        print(f"Level {level_num} saved to {filename}")
    
    print("All level data files created successfully!")

if __name__ == "__main__":
    main()
