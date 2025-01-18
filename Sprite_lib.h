#pragma once
#include <SDL.h>
#include <SDL_image.h>
#include <vector>
#include <iostream>

using namespace std;

/*
@Brief load the content of a csv file in a vector
@param src_path the directory of the csv file to read
@target the vector that will be filled with the file content
@return the number of elements added in the vector
*/
int load_csv(const char* src_path, vector<vector<string>>& target);

class Sprite_lib
{
public: //temporary

	SDL_Surface* floor_sheet;

	SDL_Surface* wall_sheet;

	SDL_Surface* prop_sheet;

	SDL_Surface* void_sheet;

	SDL_Surface* weapons_sheet;

	unsigned int character_anim_nbr;

	vector<vector<string>> character_anim;

	vector<SDL_Surface*> character_sheet;

private:

	void load_sprites();

public:

	Sprite_lib();
};

//The following methods are general tools that could be used elsewhere
/*
@Brief read a row of a given csv file
@param file the path of the file to read
@param row the position of the row to read
@return a vector containing the row elements as strings
*/
vector<string> CSV_read_row(const char* file_path, int row_num);
