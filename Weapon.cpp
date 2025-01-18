#include "Weapon.h"

Weapon::Weapon()
{
	type = rand() % 4;

	sprite_data = CSV_read_row("files\\weapons\\sprites.csv", type);
}

void Weapon::Get_sprite(int& x, int& y, int& width, int& height, int& offset)
{
	x = stoi(sprite_data[2]);
	y = stoi(sprite_data[3]);
	width = stoi(sprite_data[4]);
	height = stoi(sprite_data[5]);
	offset = stoi(sprite_data[6]);
}