#pragma once
#include <cstdlib>
#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

#include "Room.h"
#include "text.h"
#include "Character.h"
#include "Sprite_lib.h"
using namespace std;

struct Prop {
	//Coordinates of the top-left corner of the hitbox
	int pos_x;
	int pos_y;

	//Coordinates of the top-left corner of the sprite relative to the hitbox
	int sprite_relx;
	int sprite_rely;

	//Size of the hitbox
	int hbox_width;
	int hbox_height;

	//Size of the sprite
	int sprite_width;
	int sprite_height;

	//Coordinates of the top-left corner of the sprite on the sprite sheet
	int sheet_x;
	int sheet_y;

	//Explosive props !!!
	int explosive;
	int weapon_ref;
};

class World
{
private:
	//A 5*5 array representing the type of each room in the map (0 if void, 1 2 and 3 for the sizes)
	char* room_map;

	//A 175*175 array representing the nature of each tile (void, wall or floor)
	int* wall_map;

	//A 175*175 array containing the references to the sprites of each floor and wall tile
	int* tile_map;

	//Sprite lib object used to initialise Characters
	Sprite_lib* sprite_lib;

public: //break the principle of encapsulation but... I don't care
	//A vector containing a pointer torward every room on the map
	vector<Room*> rooms_idx;

	//The number of rooms on the map
	int rooms_nb;

	//A vector containing a pointer torward every prop on the map
	vector<Prop*> props_idx;

	//The number of props on the map
	int props_nb;

	//A vector containing a pointer torward every character on the map
	vector<Character*> char_idx;

	//The number of characters on the map
	int char_nb;

	//A vector containing a pointer torward every character on the map
	vector<Bullet*> proj_idx;

	//The number of characters on the map
	int proj_nb;

	vector<Text*> text_idx;

private:
	/*
	@Brief randomly generate @m tile_map from @m wall_map
	This method must only be called during the world generation process
	*/
	void generate_tiles();

	//The following methods are all part of the same map generation process
	/*
	@Brief Generate a coherent layout and fill @m room_map
	@param player1 as it's name suggest, a player, its position will be set on the spawn point
	@param first_x an integrer where the x coordinate of the first combat room will be stored
	@param first_y an integrer where the y coordinate of the first combat room will be stored
	*/
	void generate_layer(Character* player1, int& first_x, int& first_y);

	/*
	@Brief generate @m wall_map from the layer contained in @m room_map
	*/
	void generate_rooms();

	/*
	@Brief complement of generate_rooms, generate the hallways between each room
	@param first_x the x coordinate of the first combat room in @m room_map
	@param first_y the y coordinate of the first combat room in @m room_map
	*/
	void generate_hallways(int first_x, int first_y);

	/*
	@Brief generate wall tiles between void and non-void tiles
	*/
	void generate_walls();

	void place_props(int top_left_x, int top_left_y, int width);

	void place_wave(int room_ref);

	void create_prop(int center_x, int center_y, int type, int centered = 0);

	void hoDoor(int room_ref, int tile_type);

	/**
	@brief a simple tool te check box collisions
	*/
	int box_collision(int x1, int y1, int w1, int h1, int x2, int y2, int w2, int h2);

	/**
	* @brief check the presence of a solid wall between two points via a raycast
	*/
	int raycast(double x1, double y1, double x2, double y2);

public:

	/*
	@Brief default constructor of the class World
	*/
	World(Character* player1, Sprite_lib* sprite_lib_);

	/*
	@Brief Method used to acces the sprite reference of a given tile
	@param x the x coordinate of the tile
	@param y the y coordinate of the tile
	@return the reference of the tile's sprite in the relevent sprite sheet
	*/
	int get_tile(int x, int y);

	/*
	@Brief Method used to verify if a given tile is solid or empty
	Unused method in the current organisation
	@param x the x coordinate of the tile
	@param y the y coordinate of the tile
	@return 1 if the tile is solid, otherwise 0
	*/
	int get_collision(int x, int y);

	/*
	@Brief Check if the characters are colliding with walls or props,
	revert their position if it is the case
	*/
	void check_collision();

	/**
	* @brief find the closest character from the opposing team and in the line of sigth
	* of a given character
	*/
	Character* find_closest_foe(Character* origin);

	void update_anims();

	void update_targets();

	void delete_text();
};