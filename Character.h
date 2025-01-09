#pragma once
#include <SDL.h>
#include <time.h>
#include <iostream>

#include "Events.h"

class Character
{
private:
		float pos_x;
		float pos_y;

		Uint32 move_tic;
		float speed_x;
		float speed_y;

public:
		Character();

		Character(float pos_x, float pos_y);

		/*
		@brief this method can be used to access the position of the Character
		@param res_x the variable in which the x position of the Character is to be stored
		@param res_y the variable in which the y position of the Character is to be stored
		*/
		void Get_pos(int& res_x, int& res_y);

		void set_pos(int x, int y);

		void update_pos();

		void update_speed(float speed_x_, float speed_y_);
};

class Player :Character
{
private:
	Events* keyboard;

public:
	Character car;

	Player(float pos_x, float pos_y, Events* keyboard_);

	void read_inputs();
};
