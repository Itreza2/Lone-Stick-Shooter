#include "Sprite_lib.h"

int load_csv(const char* src_path, vector<vector<string>>& target)
{
	FILE* file;
	char car = NULL;
	string magic;
	vector<string> res;
	int row_nbr = 0;

	fopen_s(&file, src_path, "r");
	if (file != NULL) {
		car = fgetc(file);

		while (car != EOF) {
			res = { "" };

			while (car != '\n') {
				if (car == ',') {
					res.push_back("");
				}
				else {
					magic = car;
					res.back() = res.back() + magic;
				} car = fgetc(file);
			} car = fgetc(file);
			target.push_back(res);
			row_nbr++;
		}
		fclose(file);
	}
	return row_nbr;
}

Sprite_lib::Sprite_lib()
{	
	//Environment
	floor_sheet = IMG_Load("Sprites\\Ruin\\floor.png");
	if (floor_sheet == NULL) {
		cout << "Echec chargement spritesheet" << endl;
	} floor_sheet = SDL_ConvertSurfaceFormat(floor_sheet, SDL_PIXELFORMAT_RGB888, 0);
	wall_sheet = IMG_Load("Sprites\\Ruin\\wall.png");
	if (wall_sheet == NULL) {
		cout << "Echec chargement spritesheet" << endl;
	} wall_sheet = SDL_ConvertSurfaceFormat(wall_sheet, SDL_PIXELFORMAT_RGB888, 0);
	prop_sheet = IMG_Load("Sprites\\Ruin\\prop.png");
	if (prop_sheet == NULL) {
		cout << "Echec chargement spritesheet" << endl;
	} prop_sheet = SDL_ConvertSurfaceFormat(prop_sheet, SDL_PIXELFORMAT_RGB888, 0);
	void_sheet = IMG_Load("Sprites\\Ruin\\void.png");
	if (void_sheet == NULL) {
		cout << "Echec chargement spritesheet" << endl;
	} void_sheet = SDL_ConvertSurfaceFormat(void_sheet, SDL_PIXELFORMAT_RGB888, 0);

	//To put in a vector later, maybe...
	weapons_sheet = IMG_Load("Sprites\\weapons\\2.png");
	if (weapons_sheet == NULL) {
		cout << "Echec chargement spritesheet" << endl;
	} weapons_sheet = SDL_ConvertSurfaceFormat(weapons_sheet, SDL_PIXELFORMAT_RGB888, 0);

	character_anim_nbr = load_csv("files\\characters\\sprites.csv", character_anim);
	load_sprites();
}

void Sprite_lib::load_sprites()
{
	SDL_Surface* loaded_sheet;
	string source_path;

	for (int i = 0; i < character_anim_nbr; i++) {
		source_path = "Sprites\\characters\\" + character_anim[i][0] + ".png";

		loaded_sheet = IMG_Load(source_path.c_str());
		if (loaded_sheet == NULL) {
			cout << "Echec chargement spritesheet" << endl;
		} loaded_sheet = SDL_ConvertSurfaceFormat(loaded_sheet, SDL_PIXELFORMAT_RGB888, 0);
		character_sheet.push_back(loaded_sheet);
	}
}

vector<string> CSV_read_row(const char* file_path, int row_num)
{
	FILE* file;
	char car = NULL;
	string magic;
	vector<string> res = { "" };

	fopen_s(&file, file_path, "r");
	if (file != NULL) {

		car = fgetc(file);
		for (int i = 0; i < row_num; i++) {
			while (car != '\n') car = fgetc(file);
			car = fgetc(file);
		}
		while (car != '\n') {
			if (car == ',') {
				res.push_back("");
			}
			else {
				magic = car;
				res.back() = res.back() + magic;
			} car = fgetc(file);
		}
		fclose(file);
	}
	return res;
}