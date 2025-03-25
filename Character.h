#pragma once
#include <SDL.h>
#include <time.h>
#include <cmath>
#include <string>
#include <vector>
#include <iostream>

#include "Events.h"
#include "Weapon.h"
#include "Room.h"
#include "Sprite_lib.h"

class Character
{
protected:
	int team;

	float pos_x, pos_y;
	float prev_pos_x, prev_pos_y;
		
	//The direction faced by the character's sprite (left -1 or right 1)
	int dir;
	//The angle from direction of the aimed at position (confusing description, I know...)
	float deg;

	Uint32 move_tic;
	float speed_x;
	float speed_y;

	/*
	Contain all the usefull informations about the characteristics of the character's type
	In order : [0] animation data ref, [1] hitbox data ref, [2] default weapon, [3] max health,
	[4] base speed, (+[5] type name)
	*/
	vector<string> character_data;

	/*
	Contain the necessary informations for animating the sprite
	In order : [0] name of the sprite sheet, [1] type nbr, [2] number of animations,
	[3] width of the sprite sheet, [4] width of a sprite, [5] height of a sprite,
	[6] number of frame in each animition
	*/
	vector<string> anim_data;
	int current_anim;
	int current_frame; 

	/*
	Contain the informations relative to the hitbox of the character
	In order : [0]type nbr,[1] x and [2] y position of the ground hitbox relative to the
	character's position,[3] width and [4] height of the ground hitbox,
	[5] x and [6] y position of the damage hitbox relative to the
	character's position,[7] width and [8] height of the damage hitbox,
	*/
	vector<string> hitbox_data;

	//Raised if the character has been damaged since the last printed frame
	int dmg_flag;

	float health;

public:
	Weapon* weapon;
	int is_shooting;

public:
	Character(Sprite_lib* lib, int type_ref, float pos_x, float pos_y, int team_);

	/*
	@brief this method can be used to access the position of the Character
	@param res_x the variable in which the x position of the Character is to be stored
	@param res_y the variable in which the y position of the Character is to be stored
	*/
	void Get_pos(int& res_x, int& res_y);

	void set_pos(int x, int y);

	void update_pos();

	void revert_pos();

	void Get_ground_hitbox(int& res_rel_x, int& res_rel_y, int& res_width, int& res_height);

	void Get_damage_hitbox(int& res_rel_x, int& res_rel_y, int& res_width, int& res_height);

	int Get_team() const { return team; };

	int is_damaged() { int res = dmg_flag; if (dmg_flag) dmg_flag --; return res; };

	int is_dead() const { if (health <= 0) return 1; else return 0; };

	void raise_dmg_flag(float dmg);

	void update_speed(float speed_x_, float speed_y_);

	/**
	* @brief set @m dir and @m deg to point torward a new target
	*/
	void set_target(Character* target);

	/**
	* @brief return 1 if the character is active elsewise 0
	*/
	virtual int is_active() { return 0; };

	/*
	@brief pick the next sprite to show on camera
	@return 1 if the current animation loop has ended, otherwise 0
	*/
	int update_anim();

	void Get_anim(int& res_idx, int& res_anim, int& res_frame, int& res_dir, float& res_deg);
};

class Player : public Character
{
private:
	Events* keyboard;

	int key_0;

public:
	Player(Sprite_lib* lib, int type_ref, float pos_x, float pos_y, Events* keyboard_, int key_0_, int team_);

	void read_inputs();

	virtual int is_active() { return 1; };  //A player is always active (except when dead maybe)
};

class NPC : public Character
{
private:
	Room* room_ref;

public:
	NPC(Sprite_lib* lib, int type_ref, float pos_x, float pos_y, int team_, Room* room_ref_);

	Room* get_Room() const { return room_ref; };

	virtual int is_active() { return room_ref->active; };
};