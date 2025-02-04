#pragma once
#include <stdlib.h>
#include <math.h>
#include <string>
#include <vector>

#include "Sprite_lib.h"

using namespace std;

//If I was smart and organized, this would inherit Character...
class Bullet
{
private:
	time_t spawn_tick;
	time_t move_tick;

	float pos_x, pos_y;
	float prev_pos_x, prev_pos_y;

	int speed_x, speed_y;

	float deg;
	int dir;

	//Melting pot of all the characteristics of the bullet... (I'm a bad developper)
	//In order : [0]sprite ref, [1]sprite sheet, [2]speed at spawn, [3]lifetime, [4]speed reduction over time, [5]hitbox width, [6]damages, 
	//			 [7]explosion radius, [8]explosive damages reduction, [9]number of bullets spawned on collision, [10]data ref of spawned bullets,
	//			 [11]angle at which bullets are spawned, [12]number of frames in the animation
	vector<string> bullet_data;

	int current_frame;

public:

	Bullet(int type, int _pos_x, int _pos_y, float _angle, int _dir);

	void Get_pos(int& res_x, int& res_y) const;

	int update_pos();

	void revert_pos();

	void Get_hitbox(int& res_rel_x, int& res_rel_y, int& res_width);

	/*
	@brief pick the next sprite to show on camera
	@return 1 if the current animation loop has ended, otherwise 0
	*/
	int update_anim();

	void Get_anim(int& res_idx, int& res_sheet, int& res_frame, int& res_dir, float& res_deg);

	vector<Bullet*> last_will(int& n);
};

class Weapon
{
private:
	int type;

	Uint32 shot_tick;

	vector<string> sprite_data;

	/*
	In order : [0]bullet_type, [1]cooldown (in millisecond), [2]nbr of bullets per shot,
			   [3]dispersion (in degrees), [4]radius, [5]offset
	*/
	vector<string> weapon_data;

public:
	int muzzle_flag;

public:
	Weapon(int type_);

	void Get_sprite(int& x, int& y, int& width, int& height, int& offset);

	int Get_muzzle(int& size);

	vector<Bullet*> shoot(int pos_x, int pos_y, float angle, int dir, int& n);
};