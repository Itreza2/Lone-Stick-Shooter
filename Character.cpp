#include "Character.h"

Character::Character(Sprite_lib* lib, int type_ref, float spawn_x, float spawn_y, int team_)
{
	team = team_;
	dmg_flag = 0;

	character_data = CSV_read_row("files\\characters\\data.csv", type_ref);
	anim_data = lib->character_anim[stoi(character_data[0])];
	hitbox_data = CSV_read_row("files\\characters\\hitbox.csv", stoi(character_data[1]));
	health = stoi(character_data[3]);

	current_anim = 0;
	current_frame = 0;

	pos_x = spawn_x;
	pos_y = spawn_y;
	prev_pos_x = spawn_x;
	prev_pos_y = spawn_y;
	dir = 1;
	deg = 0;

	move_tic = SDL_GetTicks();
	speed_x = 0;
	speed_y = 0;

	weapon = new Weapon(stoi(character_data[2]));
	is_shooting = 0;
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

	prev_pos_x = pos_x;
	prev_pos_y = pos_y;

	pos_x += speed_x * (current_time - move_tic) / 1000;
	pos_y += speed_y * (current_time - move_tic) / 1000;
	if (speed_y > 0) dir = 1;
	if (speed_y < 0) dir = -1;

	if (speed_y != 0) deg = 0;
	if (speed_x > 0) {
		if (speed_y == 0) {
			deg = 3.1415 / 2;
		} else {
			deg = 3.1415 / 4;
		}
	} if (speed_x < 0) {
		if (speed_y == 0) {
			deg = - 3.1415 / 2;
		} else {
			deg = - 3.1415 / 4;
		}
	}

	move_tic = SDL_GetTicks();
}

void Character::raise_dmg_flag(float dmg)
{
	if (health > 0) {
		health -= dmg;

		if (health > 0) {
			dmg_flag = 2;
		} else {
			current_anim = 2;
			current_frame = 0;
		}
	}
}

void Character::revert_pos()
{
	pos_x = prev_pos_x;
	pos_y = prev_pos_y;
}

void Character::Get_ground_hitbox(int& res_rel_x, int& res_rel_y, int& res_width, int& res_height)
{
	res_rel_x = stoi(hitbox_data[1]);
	res_rel_y = stoi(hitbox_data[2]);
	res_width = stoi(hitbox_data[3]);
	res_height = stoi(hitbox_data[4]);
}

void Character::Get_damage_hitbox(int& res_rel_x, int& res_rel_y, int& res_width, int& res_height)
{
	res_rel_x = stoi(hitbox_data[5]);
	res_rel_y = stoi(hitbox_data[6]);
	res_width = stoi(hitbox_data[7]);
	res_height = stoi(hitbox_data[8]);
}

void Character::Get_anim(int& res_idx, int& res_anim, int& res_frame, int& res_dir, float& res_deg)
{
	res_idx = stoi(anim_data[1]);
	res_anim = current_anim;
	res_frame = current_frame;
	res_dir = dir;
	res_deg = deg;
}

int Character::update_anim()
{
	current_frame++;
	
	if (current_anim < 2) {
		if (speed_x == 0 && speed_y == 0) {
			current_anim = 0;
		}
		else current_anim = 1;
	}
	if (current_frame + 1 > stoi(anim_data[6 + current_anim])) {
		current_frame = 0;
		return 1;
	}
	else return 0;
}

void Character::update_speed(float speed_x_, float speed_y_)
{
	speed_x = speed_x_;
	speed_y = speed_y_;
}

void Character::set_target(Character* target) //Note : x and y are inverted
{
	if (pos_x < target->pos_x) {
		deg = atan(abs(pos_x - target->pos_x) / (abs(pos_y - target->pos_y)));
	}
	else deg = atan(-abs(pos_x - target->pos_x) / (abs(pos_y - target->pos_y)));

	if (pos_y < target->pos_y) {
		dir = 1;
	}
	else dir = -1;
}

//Player

Player::Player(Sprite_lib* lib, int type_ref, float spawn_x, float spawn_y, Events* keyboard_, int key_0_, int team_) : Character(lib, type_ref, spawn_x, spawn_y, team_)
{
	key_0 = key_0_;
	keyboard = keyboard_;
	target_distance = 0;
}

void Player::read_inputs()
{
	float newspeed_x = 0;
	float newspeed_y = 0;

	target_distance = 0;

	if (keyboard->is_pressed[3 + key_0]) {
		if (keyboard->is_pressed[0 + key_0] || keyboard->is_pressed[1 + key_0]) newspeed_x += 141;
		else newspeed_x += 200;
	} if (keyboard->is_pressed[2 + key_0]) {
		if (keyboard->is_pressed[0 + key_0] || keyboard->is_pressed[1 + key_0]) newspeed_x -= 141;
		else newspeed_x -= 200;
	} if (keyboard->is_pressed[0 + key_0]) {
		if (keyboard->is_pressed[2 + key_0] || keyboard->is_pressed[3 + key_0]) newspeed_y += 141;
		else newspeed_y += 200;
	} if (keyboard->is_pressed[1 + key_0]) {
		if (keyboard->is_pressed[2 + key_0] || keyboard->is_pressed[3 + key_0]) newspeed_y -= 141;
		else newspeed_y -= 200;
	}
	if (keyboard->is_pressed[4 + key_0]) {
		is_shooting = 1;
	} else is_shooting = 0;

	update_speed(newspeed_x, newspeed_y);
}

void Player::set_target(Character* target) //Note : x and y are inverted
{
	int target_x, target_y;
	target->Get_pos(target_x, target_y);

	target_distance = sqrt(pow(pos_x - target_x, 2) + pow(pos_y - target_y, 2));

	if (pos_x < target_x) {
		deg = atan(abs(pos_x - target_x) / (abs(pos_y - target_y)));
	}
	else deg = atan(-abs(pos_x - target_x) / (abs(pos_y - target_y)));

	if (pos_y < target_y) {
		dir = 1;
	}
	else dir = -1;
}

NPC::NPC(Sprite_lib* lib, int type_ref, float pos_x, float pos_y, int team_, Room* room_ref_) : Character(lib, type_ref, pos_x, pos_y, team_)
{
	room_ref = room_ref_;
}