from database import gamedb

# PoC of GameDataBase class


def main():
    # initialize DB
    db = gamedb.GameDataBase()
    db.initialize_db()

    # create player
    db.create_player("John")
    print("Created a player")

    # get player row
    player = db.get_player(1)
    print(f"Print player={player}")

    # update position col
    db.update_player_position(1, 999)
    print("Updated the player's row into 999")

    player = db.get_player(1)
    print(f"Print player={player}")



if __name__ == "__main__":
    main()
