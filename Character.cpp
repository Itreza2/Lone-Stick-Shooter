#include "Character.h"

Character::Character()
{
	pos_x = 0;
	pos_y = 0;

	move_tic = SDL_GetTicks();
	speed_x = 0;
	speed_y = 0;
}

Character::Character(float spawn_x, float spawn_y)
{
	pos_x = spawn_x;
	pos_y = spawn_y;

	move_tic = SDL_GetTicks();
	speed_x = 0;
	speed_y = 0;
}

void Character::Get_pos(int& res_x, int& res_y)
{
	res_x = (int) pos_x;
	res_y = (int) pos_y;
}

void Character::set_pos(int x, int y)
{
	pos_x = x;
	pos_y = y;
}

void Character::update_pos()
{
	Uint32 current_time = SDL_GetTicks();
	pos_x += speed_x * (current_time - move_tic) / 1000;
	pos_y += speed_y * (current_time - move_tic) / 1000;

	move_tic = SDL_GetTicks();
}

void Character::update_speed(float speed_x_, float speed_y_)
{
	speed_x = speed_x_;
	speed_y = speed_y_;
}

//Player

Player::Player(float spawn_x, float spawn_y, Events* keyboard_)
{
	car = Character(spawn_x, spawn_y);

	keyboard = keyboard_;
}

void Player::read_inputs()
{
	float newspeed_x = 0;
	float newspeed_y = 0;

	if (keyboard->is_pressed[3]) {
		if (keyboard->is_pressed[0] || keyboard->is_pressed[1]) newspeed_x += 100;
		else newspeed_x += 200;
	} if (keyboard->is_pressed[2]) {
		if (keyboard->is_pressed[0] || keyboard->is_pressed[1]) newspeed_x -= 100;
		else newspeed_x -= 200;
	} if (keyboard->is_pressed[0]) {
		if (keyboard->is_pressed[2] || keyboard->is_pressed[3]) newspeed_y += 100;
		else newspeed_y += 200;
	} if (keyboard->is_pressed[1]) {
		if (keyboard->is_pressed[2] || keyboard->is_pressed[3]) newspeed_y -= 100;
		else newspeed_y -= 200;
	}
	car.update_speed(newspeed_x, newspeed_y);
}