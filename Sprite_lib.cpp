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
	muzzle_sheet = IMG_Load("Sprites\\weapons\\muzzle.png");
	if (muzzle_sheet == NULL) {
		cout << "Echec chargement spritesheet" << endl;
	} muzzle_sheet = SDL_ConvertSurfaceFormat(muzzle_sheet, SDL_PIXELFORMAT_RGB888, 0);

	void_sheet_nbr = 40;
	char magicD, magicU;
	string file_path;
	for (int i = 0; i < void_sheet_nbr; i++) {
		magicD = i / (int)10 + '0';
		magicU = i % 10 + '0';
		file_path = "Sprites\\Ruin\\void\\00";
		file_path = file_path + magicD;
		file_path = file_path + magicU;
		file_path = file_path + ".png";
		void_sheet.push_back(IMG_Load(file_path.c_str()));
		if (void_sheet[i] == NULL) {
			cout << "Echec chargement spritesheet" << endl;
		} void_sheet[i] = SDL_ConvertSurfaceFormat(void_sheet[i], SDL_PIXELFORMAT_RGB888, 0);
	}

	//To put in a vector later, maybe...
	weapons_sheet = IMG_Load("Sprites\\weapons\\2.png");
	if (weapons_sheet == NULL) {
		cout << "Echec chargement spritesheet" << endl;
	} weapons_sheet = SDL_ConvertSurfaceFormat(weapons_sheet, SDL_PIXELFORMAT_RGB888, 0);

	character_anim_nbr = load_csv("files\\characters\\sprites.csv", character_anim);
	bullet_anim_nbr = load_csv("files\\bullets\\anims.csv", bullet_anim);
	load_csv("files\\weapons\\muzzles.csv", muzzle_data);

	load_sprites();
}

void Sprite_lib::load_sprites()
{
	SDL_Surface* loaded_sheet;
	TTF_Font* loaded_font;
	string source_path;

	for (int i = 0; i < character_anim_nbr; i++) {
		source_path = "Sprites\\characters\\" + character_anim[i][0] + ".png";

		loaded_sheet = IMG_Load(source_path.c_str());
		if (loaded_sheet == NULL) {
			cout << "Echec chargement spritesheet" << endl;
		} loaded_sheet = SDL_ConvertSurfaceFormat(loaded_sheet, SDL_PIXELFORMAT_RGB888, 0);
		character_sheet.push_back(loaded_sheet);
	}
	for (int i = 0; i < 8; i++) {
		source_path = "Sprites\\bullets\\" + to_string(i) + ".png";

		loaded_sheet = IMG_Load(source_path.c_str());
		if (loaded_sheet == NULL) {
			cout << "Echec chargement spritesheet" << endl;
		} loaded_sheet = SDL_ConvertSurfaceFormat(loaded_sheet, SDL_PIXELFORMAT_RGB888, 0);
		bullet_sheet.push_back(loaded_sheet);
	}
	for (int i = 0; i < 1; i++) {
		source_path = "Sprites\\fonts\\" + to_string(i) + ".ttf";

		loaded_font = TTF_OpenFont(source_path.c_str(), 12);
		if (loaded_font == NULL) {
			cout << "Assassin de la police" << endl;
		}
		fonts.push_back(loaded_font);
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