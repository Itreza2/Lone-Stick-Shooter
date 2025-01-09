#include "Sprite_lib.h"

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

	//Player (temporary)
	player_sheet = IMG_Load("Sprites\\Characters\\player1.png");
	if (player_sheet == NULL) {
		cout << "Echec chargement spritesheet" << endl;
	} player_sheet = SDL_ConvertSurfaceFormat(player_sheet, SDL_PIXELFORMAT_RGB888, 0);
}