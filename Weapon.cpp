#include "Weapon.h"

Weapon::Weapon(int type_)
{
	type = type_;
	shot_tick = 0;

	sprite_data = CSV_read_row("files\\weapons\\sprites.csv", type_);
	weapon_data = CSV_read_row("files\\weapons\\data.csv", type_);
}

void Weapon::Get_sprite(int& x, int& y, int& width, int& height, int& offset)
{
	x = stoi(sprite_data[2]);
	y = stoi(sprite_data[3]);
	width = stoi(sprite_data[4]);
	height = stoi(sprite_data[5]);
	offset = stoi(sprite_data[6]);
}

vector<Bullet*> Weapon::shoot(int pos_x, int pos_y, float angle, int dir, int& n)
{
	vector<Bullet*> res = {};
	float disp;
	pos_y += 8;

	if (SDL_GetTicks() - shot_tick > stoi(weapon_data[1])) {
		n = stoi(weapon_data[2]);
		int dist_x = cos(angle) * stoi(weapon_data[4]) * dir;
		int dist_y = sin(angle) * stoi(weapon_data[4]);

		for (int i = 0; i < stoi(weapon_data[2]); i++) {
			disp = (float)(rand() % (stoi(weapon_data[3]) * 2) - stoi(weapon_data[3])) / 180 * (3.1415);
			res.push_back(new Bullet(stoi(weapon_data[0]), pos_x + dist_x, pos_y + dist_y, angle + disp, dir));
		}
		shot_tick = SDL_GetTicks();
	}
	return res;
}

Bullet::Bullet(int type, int _pos_x, int _pos_y, float _angle, int _dir)
{
	pos_x = _pos_x;
	pos_y = _pos_y;
	prev_pos_x = _pos_x;
	prev_pos_y = _pos_y;

	deg = _angle;
	dir = _dir;

	bullet_data = CSV_read_row("files/bullets/data.csv", type);

	if (dir == 1) {
		speed_x = stoi(bullet_data[2]) * cos(_angle);
		speed_y = stoi(bullet_data[2]) * sin(_angle);
	}
	else {
		speed_x = stoi(bullet_data[2]) * cos(-_angle + 3.1415);
		speed_y = stoi(bullet_data[2]) * sin(-_angle + 3.1415);
	}

	current_frame = 0;
	move_tick = SDL_GetTicks();
	spawn_tick = move_tick;
}

void Bullet::Get_pos(int& res_x, int& res_y) const
{
	res_x = (int)pos_x;
	res_y = (int)pos_y;
}

void Bullet::Get_hitbox(int& res_rel_x, int& res_rel_y, int& res_width)
{
	res_rel_x = pos_x - stoi(bullet_data[5]) / 2;
	res_rel_y = pos_y - stoi(bullet_data[5]) / 2;
	res_width = stoi(bullet_data[5]);
}

int Bullet::update_pos()
{
	prev_pos_x = pos_x;
	prev_pos_y = pos_y;

	float quantum = (float)(SDL_GetTicks() - move_tick) / 1000;
	pos_x += speed_x * quantum;
	pos_y += speed_y * quantum;
	move_tick = SDL_GetTicks();

	if (SDL_GetTicks() - spawn_tick > static_cast<long long>(stoi(bullet_data[3])) * 1000) {
		return 1;
	}
	else return 0;
}

void Bullet::revert_pos()
{
	pos_x = prev_pos_x;
	pos_y = prev_pos_y;
}

int Bullet::update_anim()
{
	current_frame++;
	if (current_frame > stoi(bullet_data[12])) {
		current_frame = 0;
		return 1;
	}
	else return 0;
}

void Bullet::Get_anim(int& res_idx, int& res_sheet, int& res_frame, int& res_dir, float& res_deg)
{
	res_idx = stoi(bullet_data[0]);
	res_sheet = stoi(bullet_data[1]);
	res_frame = current_frame;
	res_dir = dir;
	res_deg = deg;
}