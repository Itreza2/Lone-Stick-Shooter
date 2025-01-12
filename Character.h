#pragma once
#include <SDL.h>
#include <time.h>
#include <string>
#include <vector>
#include <iostream>

#include "Events.h"
#include "Sprite_lib.h"

class Character
{
protected:
		float pos_x;
		float pos_y;
		int dir;

		Uint32 move_tic;
		float speed_x;
		float speed_y;

		vector<string> anim_data;
		int current_anim;
		int current_frame;

public:
		Character(Sprite_lib* lib);

		Character(Sprite_lib* lib, float pos_x, float pos_y);

		/*
		@brief this method can be used to access the position of the Character
		@param res_x the variable in which the x position of the Character is to be stored
		@param res_y the variable in which the y position of the Character is to be stored
		*/
		void Get_pos(int& res_x, int& res_y);

		void set_pos(int x, int y);

		void update_pos();

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
	Player(Sprite_lib* lib, float pos_x, float pos_y, Events* keyboard_);

	void read_inputs();
};
