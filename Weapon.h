#pragma once
#include <string>
#include <vector>

#include "Sprite_lib.h"

using namespace std;

class Weapon
{
private:
	int type;

	vector<string> sprite_data;

public:
	Weapon();

	void Get_sprite(int& x, int& y, int& width, int& height, int& offset);
};

