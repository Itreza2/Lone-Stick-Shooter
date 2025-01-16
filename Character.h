#pragma once
#include <SDL.h>
#include <time.h>
#include <cmath>
#include <string>
#include <vector>
#include <iostream>

#include "Events.h"
#include "Sprite_lib.h"

class Character
{
protected:
		float pos_x, pos_y;
		float prev_pos_x, prev_pos_y;
		int dir;

		Uint32 move_tic;
		float speed_x;
		float speed_y;

		/*
		Contain the necessary informations for animating the sprite
		In order : name of the sprite sheet, type nbr, number of animations,
		width of the sprite sheet, width of a sprite, height of a sprite,
		number of frame in each animition
		*/
		vector<string> anim_data;
		int current_anim;
		int current_frame;

		/*
		Contain the informations relative to the hitbox of the character
		In order : type nbr, x and y position of the ground hitbox relative to the
		character's position, width and height of the ground hitbox,
		x and y position of the damage hitbox relative to the
		character's position, width and height of the damage hitbox,
		*/
		vector<string> hitbox_data;

public:
		Character(Sprite_lib* lib, int type_ref);

		Character(Sprite_lib* lib, int type_ref, float pos_x, float pos_y);

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

		void update_speed(float speed_x_, float speed_y_);

		/*
		@brief pick the next sprite to show on camera
		@return 1 if the current animation loop has ended, otherwise 0
		*/
		int update_anim();

		void Get_anim(int& res_idx, int& res_anim, int& res_frame, int& res_dir);
};

class Player : public Character
{
private:
	Events* keyboard;

public:
	Player(Sprite_lib* lib, int type_ref, float pos_x, float pos_y, Events* keyboard_);

	void read_inputs();
};
