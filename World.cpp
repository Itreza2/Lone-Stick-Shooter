#include "World.h"

//TODO : actual world generation
World::World(Character* player1, Sprite_lib* sprite_lib_)
{
	int first_x, first_y;

	rooms_idx = {};
	rooms_nb = 0;

	props_idx = {};
	props_nb = 0;

	char_idx = { player1 };
	char_nb = 1;

	proj_idx = { };
	proj_nb = 0;

	sprite_lib = sprite_lib_;

	room_map = (char*)malloc(sizeof(char) * 50);
	if (room_map != NULL) {
		for (int i = 0; i < 50; i++) room_map[i] = 0;
	} this->generate_layer(player1, first_x, first_y);
	wall_map = (int*)malloc(sizeof(int) * (static_cast<unsigned long long>(175) * 175));
	tile_map = (int*)malloc(sizeof(int) * (static_cast<unsigned long long>(175) * 175));

	if (wall_map != NULL && tile_map != NULL) {
		for (int i = 0; i < 175 * 175; i++) wall_map[i] = 0;
		for (int i = 0; i < 175 * 175; i++) tile_map[i] = -1;
		this->generate_rooms();
		this->generate_hallways(first_x, first_y);
		this->generate_walls();
		this->generate_tiles();

		for (int i = 0; i < rooms_nb; i++) {
			hoDoor(i, 1);
			place_wave(i);
		}
	}
}

void World::generate_tiles()
{
	for (int i = 0; i < 175 * 175; i++) {
		
		switch (wall_map[i]) {

		case 1://Grass tile
			tile_map[i] = (rand() % 8) * 16 + (rand() % 8);
			if (tile_map[i] == 0 || tile_map[i] == 1) tile_map[i] = 2;//No idea why this is necessary ¯\_(ツ)_/¯
			break;
		case 2://Grass and flower tile
			tile_map[i] = (rand() % 8) * 16 + ((rand() % 8) + 8);
			break;
		case 3://Paved tile
			tile_map[i] = ((rand() % 8) + 8) * 16 + (rand() % 8);
			break;
		case 4://Paved tile (but a little bit more damaged)
			tile_map[i] = ((rand() % 8) + 8) * 16 + ((rand() % 8) + 8);
			break;
		case 5://Walls (or blocks with grid-based collision anyway)
			tile_map[i] = rand() % 3 + 1;
			break;
		}
	}
}

//This function is too big and should be shortened...
void World::generate_layer(Character* player1, int& first_x, int& first_y)
{
	int pos_x, pos_y;
	int next_pos_x, next_pos_y;
	int pos_found;
	int iter_cpt;//If the current layout is unsolvable, the process must be terminated and restarted

	int gen_unfinished = 1;
	while (gen_unfinished) {
		gen_unfinished = 0;
		for (int i = 0; i < 50; i++) room_map[i] = 0;

		pos_x = rand() % 5; pos_y = rand() % 5;
		player1->set_pos(pos_y * (35) * 32 + 560, pos_x * (35) * 32 + 560);
		room_map[(pos_x * 5 + pos_y) * 2] = 1;
		room_map[(pos_x * 5 + pos_y) * 2 + 1] = 1;

		for (int i = 0; i < 4; i++) {
			pos_found = 0; iter_cpt = 0;
			while (!pos_found) {
				iter_cpt++;
				next_pos_x = pos_x; next_pos_y = pos_y;
				if (rand() % 2) {
					if (rand() % 2) next_pos_x++;
					else next_pos_x--;
				} else {
					if (rand() % 2) next_pos_y++;
					else next_pos_y--;
				}
				if (next_pos_x >= 0 && next_pos_x < 5 && next_pos_y >= 0 && next_pos_y < 5) {
					if (room_map[(next_pos_x * 5 + next_pos_y) * 2] == 0 || 
						(room_map[(next_pos_x * 5 + next_pos_y) * 2] == 1 && room_map[(next_pos_x * 5 + next_pos_y) * 2 + 1] > 2)) {
						pos_found = 1;
					}
				} if (iter_cpt > 10) { pos_found = 1; gen_unfinished = 1; }
			}
			pos_x = next_pos_x; pos_y = next_pos_y;
			if (i == 0) { //The first room after the spawn can only lead to another combat room to avoid shortcuts
				first_x = pos_x;
				first_y = pos_y;
			}
			if (i == 3) { //End of the level
				room_map[(pos_x * 5 + pos_y) * 2] = 1;
				room_map[(pos_x * 5 + pos_y) * 2 + 1] = 2;
			} else { // Combat room
				room_map[(pos_x * 5 + pos_y) * 2] = rand() %2 + 2;
				room_map[(pos_x * 5 + pos_y) * 2 + 1] = 0;

				//Generation of special rooms (shop, chest...)
				if (rand() % 2) {
					if (rand() % 2) next_pos_x++;
					else next_pos_x--;
				} else {
					if (rand() % 2) next_pos_y++;
					else next_pos_y--;
				}
				if (next_pos_x >= 0 && next_pos_x < 5 && next_pos_y >= 0 && next_pos_y < 5) {
					if (room_map[(next_pos_x * 5 + next_pos_y) * 2] == 0) {
						room_map[(next_pos_x * 5 + next_pos_y) * 2] = 1;
						room_map[(next_pos_x * 5 + next_pos_y) * 2 + 1] = 3;
					}
				}
			}
		}
	}
}

void World::generate_rooms()
{
	FILE* file;
	string file_path;
	string magic; //Seriously why does assignation works fine and concatenation does not ?!
	char car;

	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < 5; j++) {
			if (room_map[(i * 5 + j) * 2] == 1) {
				fopen_s(&file, "files\\roomLayers\\1.txt", "r");
				if (file != NULL) {
					for (int k = 0; k < 121 ; k++) {
						car = fgetc(file);
						if (car == '\n') car = fgetc(file);
						wall_map[((k / 11) + (j * 35 + 12)) * 175 + (k % 11) + (i * 35 + 12)] = (int)(car - '0');
					} fclose(file);
				} 
				//Creation of the chest prop (not the interactible object !)
				if (room_map[(i * 5 + j) * 2 + 1] == 3) create_prop(j * 35 * 32 + 550, i * 35 * 32 + 534, 3);

			} if (room_map[(i * 5 + j) * 2] == 2) {
				magic = (char)(rand() % 7) + '0'; //Currently 7 types of size 2 rooms
				file_path = "files\\roomLayers\\2\\" + magic + ".txt";
				fopen_s(&file, file_path.c_str(), "r");
				if (file != NULL) {
					for (int k = 0; k < 289; k++) {
						car = fgetc(file);
						if (car == '\n') car = fgetc(file);
						wall_map[((k / 17) + (j * 35 + 9)) * 175 + (k % 17) + (i * 35 + 9)] = (int)(car - '0');
					} fclose(file);
				} 
				file_path = "files\\roomLayers\\2\\" + magic + "p.txt";
				fopen_s(&file, file_path.c_str(), "r");
				if (file != NULL) {
					for (int k = 0; k < 289; k++) {
						car = fgetc(file);
						if (car == '\n') car = fgetc(file);
						if (car != 'v') {
							create_prop(((k / 17) + (j * 35 + 9)) * 32 + 16, ((k % 17) + (i * 35 + 9)) * 32 + 16, (int)(car - '0'), 1);
						}
					} fclose(file);
				} 
				rooms_idx.push_back(new Room((j * 35 + 9) * 32, (i * 35 + 9) * 32, 17 * 32, 0, 6));
				rooms_nb++;
				place_props(i * 35 + 9, j * 35 + 9, 17);

			} if (room_map[(i * 5 + j) * 2] == 3) {
				magic = (char)(rand() % 4) + '0'; //Currently 4 types of size 2 rooms
				file_path = "files\\roomLayers\\3\\" + magic + ".txt";
				fopen_s(&file, file_path.c_str(), "r");
				if (file != NULL) {
					for (int k = 0; k < 529; k++) {
						car = fgetc(file);
						if (car == '\n') car = fgetc(file);
						wall_map[((k / 23) + (j * 35 + 6)) * 175 + (k % 23) + (i * 35 + 6)] = (int)(car - '0');
					} fclose(file);
				} 
				file_path = "files\\roomLayers\\3\\" + magic + "p.txt";
				fopen_s(&file, file_path.c_str(), "r");
				if (file != NULL) {
					for (int k = 0; k < 529; k++) {
						car = fgetc(file);
						if (car == '\n') car = fgetc(file);
						if (car != 'v') {
							create_prop(((k / 23) + (j * 35 + 6)) * 32 + 16, ((k % 23) + (i * 35 + 6)) * 32 + 16, (int)(car - '0'), 1);
						}
					} fclose(file);
				}
				rooms_idx.push_back(new Room((j * 35 + 6) * 32, (i * 35 + 6) * 32, 23 * 32, 0, 10));
				rooms_nb++;
				place_props(i * 35 + 6, j * 35 + 6, 23);
			}
		}
	}
}

void World::generate_hallways(int first_x, int first_y)
{
	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < 5; j++) {
			if (room_map[(i * 5 + j) * 2] != 0) {
				if (room_map[((i + 1) * 5 + j) * 2] != 0 && i + 1 < 5) {
					for (int o = i * 35 + 23; o < (i + 1) * 35 + 12; o++) {
						for (int p = j * 35 + 15; p < j * 35 + 20; p++) {
							if (wall_map[p * 175 + o] == 0) {
								if (p > j * 35 + 15 && p < j * 35 + 19) wall_map[p * 175 + o] = 3;
								else wall_map[p * 175 + o] = 1;
							}
						}
					}
				} if (room_map[(i * 5 + (j + 1)) * 2] != 0 && j + 1 < 5) {
					for (int o = i * 35 + 15; o < i * 35 + 20; o++) {
						for (int p = j * 35 + 23; p < (j + 1) * 35 + 12; p++) {
							if (wall_map[p * 175 + o] == 0) {
								if (o > i * 35 + 15 && o < i * 35 + 19) wall_map[p * 175 + o] = 3;
								else wall_map[p * 175 + o] = 1;
							}
						}
					}
				}
			}
		}
	}
}

void World::generate_walls()
{
	int* wall_map_c = (int*)malloc(sizeof(int) * (static_cast<unsigned long long>(175) * 175));
	if (wall_map_c != NULL) {
		for (int i = 0; i < 175 * 175; i++) wall_map_c[i] = wall_map[i];

		//Note : walls can't be generated at the edge of the map, this should not matter anyway
		for (int i = 1; i < 174; i++) {
			for (int j = 1; j < 174; j++) {
				if (wall_map_c[i * 175 + j] == 0 && (wall_map_c[(i - 1) * 175 + (j - 1)] != 0 || wall_map_c[i * 175 + (j - 1)] != 0 ||
					wall_map_c[(i + 1) * 175 + (j - 1)] != 0 || wall_map_c[(i - 1) * 175 + j] != 0 ||
					wall_map_c[(i + 1) * 175 + j] != 0 || wall_map_c[(i - 1) * 175 + (j + 1)] != 0 ||
					wall_map_c[i * 175 + (j + 1)] != 0 || wall_map_c[(i + 1) * 175 + (j + 1)] != 0)) {
					wall_map[i * 175 + j] = 5;
				}
			}
		} free(wall_map_c);
	}
}

void World::place_props(int top_left_x, int top_left_y, int width)
{
	int pos_x, pos_y;
	vector<string> csv;
	int position_correct;
	int type;

	for (int i = 0; i < width; i++) {
		type = rand() % 3;
		csv = CSV_read_row("files\\Ruin\\prop.csv", type);
		pos_x = (rand() % (width * 32)) + (top_left_y * 32);
		pos_y = (rand() % (width * 32)) + (top_left_x * 32);

		position_correct = 1;
		for (int x = pos_x / 32; x <= (pos_x + stoi(csv[2])) / 32; x++) {
			for (int y = pos_y / 32; y <= (pos_y + stoi(csv[1])) / 32; y++) {
				if (wall_map[x * 175 + y] != 2) position_correct = 0;
			}
		}
		if (position_correct) {
			create_prop(pos_x, pos_y, type);
		}
	}
}

void World::place_wave(int room_ref)
{
	int tokens_left = rooms_idx[room_ref]->tokens;
	int top_left_x = rooms_idx[room_ref]->top_left_x;
	int top_left_y = rooms_idx[room_ref]->top_left_y;
	int size = rooms_idx[room_ref]->size;
	int ennemy_type, position_correct;
	float pos_x, pos_y;

	while (tokens_left > 0) {
		ennemy_type = 2; //To choose randomly when more variety will be added
		pos_x = (float)(top_left_x + (rand() % size));
		pos_y = (float)(top_left_y + (rand() % size));

		NPC* new_ennemy = new NPC(sprite_lib, ennemy_type, pos_x, pos_y, 0, rooms_idx[room_ref]);

		position_correct = 1;
		for (int x = pos_x / 32; x <= (pos_x + 32) / 32; x++) {
			for (int y = pos_y / 32; y <= (pos_y + 32) / 32; y++) {
				if (wall_map[x * 175 + y] == 0 || wall_map[x * 175 + y] == 5) position_correct = 0;
			}
		}
		if (position_correct) {
			tokens_left--;
			rooms_idx[room_ref]->defender_nbr++;
			char_idx.push_back(new_ennemy);
			char_nb++;
		} else {
			delete new_ennemy;
		}
	}
}

void World::create_prop(int top_left_x, int top_letf_y, int type, int centered)
{
	vector<string> csv = CSV_read_row("files\\Ruin\\prop.csv", type);
	Prop* new_prop = (Prop*)malloc(sizeof(Prop));

	if (new_prop != NULL) {
		if (centered) {
			top_left_x -= stoi(csv[1]) / 2;
			top_letf_y -= stoi(csv[2]) / 2;
		}
		new_prop->pos_x = top_left_x;
		new_prop->pos_y = top_letf_y;
		new_prop->hbox_width = stoi(csv[1]);
		new_prop->hbox_height = stoi(csv[2]);
		new_prop->sprite_relx = stoi(csv[3]);
		new_prop->sprite_rely = stoi(csv[4]);
		new_prop->sprite_width = stoi(csv[5]);
		new_prop->sprite_height = stoi(csv[6]);
		new_prop->sheet_x = stoi(csv[7]);
		new_prop->sheet_y = stoi(csv[8]);
		new_prop->explosive = stoi(csv[9]);
		new_prop->weapon_ref = stoi(csv[10]);

		props_idx.push_back(new_prop);
		props_nb++;
	}
}

void World::hoDoor(int room_ref, int tile_type)
{
	int room_x, room_y, room_size;
	rooms_idx[room_ref]->Get_hitbox(room_y, room_x, room_size);
	room_x /= 32; room_y /= 32; room_size /= 32;

	for (int i = room_size / 2 - 2; i < room_size / 2 + 3; i++) {
		int sprite;
		if (tile_type == 5) sprite = 0;
		else sprite = 1;

		if (wall_map[(room_y - 1) * 175 + room_x + i] != 5 || tile_map[(room_y - 1) * 175 + room_x + i] == 0) {
			wall_map[(room_y - 1) * 175 + room_x + i] = tile_type;
			tile_map[(room_y - 1) * 175 + room_x + i] = sprite;
		}
		if (wall_map[(room_y + room_size) * 175 + room_x + i] != 5 || tile_map[(room_y + room_size) * 175 + room_x + i] == 0) {
			wall_map[(room_y + room_size) * 175 + room_x + i] = tile_type;
			tile_map[(room_y + room_size) * 175 + room_x + i] = sprite;
		}
		if (wall_map[(room_y + i) * 175 + room_x - 1] != 5 || tile_map[(room_y + i) * 175 + room_x - 1] == 0) {
			wall_map[(room_y + i) * 175 + room_x - 1] = tile_type;
			tile_map[(room_y + i) * 175 + room_x - 1] = sprite;
		}
		if (wall_map[(room_y + i) * 175 + room_x + room_size] != 5 || tile_map[(room_y + i) * 175 + room_x + room_size] == 0) {
			wall_map[(room_y + i) * 175 + room_x + room_size] = tile_type;
			tile_map[(room_y + i) * 175 + room_x + room_size] = sprite;
		}
	}
}

int World::get_tile(int x, int y)
{
	return tile_map[x * 175 + y];
}

int World::get_collision(int x, int y)
{
	if (wall_map[x * 175 + y] > 4) return 1;
	else return 0;
}

void World::check_collision()
{
	int pos_x, pos_y, cpos_x, cpos_y, width, height;
	int prop_x, prop_y, prop_width, prop_height;
	int collided;
	int room_x, room_y, room_size;

	for (int i = 0; i < char_nb; i++) {

		char_idx[i]->Get_pos(cpos_x, cpos_y);
		char_idx[i]->Get_ground_hitbox(pos_x, pos_y, width, height);
		pos_x += cpos_y;
		pos_y += cpos_x;

		collided = 0;
		
		//Collision with grid-based placing (ie. walls)
		for (int x = pos_x / 32; x <= (pos_x + width) / 32; x++) {
			for (int y = pos_y / 32; y <= (pos_y + height) / 32; y++) {
				if (wall_map[(y) * 175 + (x)] > 4) collided = 1;
			}
		}
		//Collision with props
		for (int j = 0; j < props_nb; j++) {
			prop_x = props_idx[j]->pos_y;
			prop_y = props_idx[j]->pos_x;
			prop_width = props_idx[j]->hbox_width;
			prop_height = props_idx[j]->hbox_height;

			if ((pos_x < prop_x + prop_width && pos_x + width > prop_x) &&
				(pos_y < prop_y + prop_height && pos_y + height > prop_y)) {
				collided = 1;
			}
		}
		if (collided) {
			char_idx[i]->revert_pos();
		}
		//Room entering
		if (char_idx[i]->Get_team()) {
			for (int j = 0; j < rooms_nb; j++) {
				if (!rooms_idx[j]->active && rooms_idx[j]->defender_nbr) {
					rooms_idx[j]->Get_hitbox(room_x, room_y, room_size);
					if ((pos_y + 25 < room_x + room_size && pos_y - 25  + width > room_x) &&
						(pos_x + 25 < room_y + room_size && pos_x - 25 + height > room_y)) {

						rooms_idx[j]->active = 1;
						hoDoor(j, 5);
					}
				} else {
					if (!rooms_idx[j]->defender_nbr) {
						rooms_idx[j]->active = 0;
						hoDoor(j, 1);
					}
				}
			}
		}
	}

	//The following code should be put in its own method for more clarity
	int nb_erased = 0;
	int n;
	int x2, y2, w2, h2, relx2, rely2;
	for (int i = 0; i < proj_nb; i++) {
		int pos_x, pos_y, width;

		proj_idx[i - nb_erased]->Get_pos(pos_x, pos_y);
		width = 4;
		pos_x -= width;
		pos_y -= width - 20;

		collided = 0;

		//Collision with grid-based placing (ie. walls)
		for (int x = pos_x / 32; x <= (pos_x + width * 2) / 32; x++) {
			for (int y = pos_y / 32; y <= (pos_y + width * 2) / 32; y++) {
				if (wall_map[(y) * 175 + (x)] > 4) collided = 1;
			}
		} pos_y += 20;
		//Collision with a character
		for (int j = 0; j < char_nb; j++) {
			if (char_idx[j]->Get_team() != proj_idx[i - nb_erased]->Get_team() && char_idx[j]->is_active()) { //If char.team = proj.team
				char_idx[j]->Get_pos(y2, x2);
				char_idx[j]->Get_damage_hitbox(relx2, rely2, w2, h2);
				x2 += relx2;
				y2 -= rely2;
				if (box_collision(pos_x, pos_y, width * 2, width * 2, x2, y2, w2, h2)) {
					collided = 1;
					char_idx[j]->raise_dmg_flag(proj_idx[i - nb_erased]->get_dmg());
				}
			}
		}
		//Collision with explosive props (explosive only)
		for (int j = 0; j < props_nb; j++) {
			if (props_idx[j]->explosive) {
				x2 = props_idx[j]->pos_y + props_idx[j]->sprite_relx;
				y2 = props_idx[j]->pos_x - props_idx[j]->sprite_rely;
				w2 = props_idx[j]->sprite_width;
				h2 = props_idx[j]->sprite_height;
				if (box_collision(pos_x, pos_y, width * 2, width * 2, x2, y2, w2, w2)) {
					collided = 1;
					if (props_idx[j]->weapon_ref >= 0) {
						for (int disp = 0; disp < 4; disp++) {
							proj_idx.push_back(new Bullet(props_idx[j]->weapon_ref, x2 + w2 / 2, y2 - h2 / 2, disp * (3.14 / 4) - (3.14 / 2), 1));
							proj_idx.push_back(new Bullet(props_idx[j]->weapon_ref, x2 + w2 / 2, y2 - h2 / 2, (disp + 1) * (3.14 / 4) - (3.14 / 2), -1));
							proj_nb += 2;
						}
					}
					props_idx.erase(props_idx.begin() + j);
					props_nb--;
					j--;			//Ohlala c'est pas bien !! je le fais quand même haha
				}
			}
		}
		if (collided) {
			proj_idx[i - nb_erased]->revert_pos();
			vector<Bullet*> res = proj_idx[i - nb_erased]->last_will(n);
			for (int j = 0; j < n; j++) {
				proj_idx.push_back(res[j]);
				proj_nb++;
			}

			proj_idx.erase(proj_idx.begin() + (i - nb_erased));
			nb_erased++;
			proj_nb--;
		}
	}
}

void World::update_anims()
{
	int nb_erased = 0;
	for (int i = 0; i < char_nb; i++) {
		if (char_idx[i - nb_erased]->update_anim()) {
			if (char_idx[i - nb_erased]->is_dead()) {
				NPC* cast = (NPC*)(char_idx[i - nb_erased]);
				cast->get_Room()->defender_nbr--;
				char_idx.erase(char_idx.begin() + (i - nb_erased));
				nb_erased++;
				char_nb--;
			}
		}
	}
	for (int i = 0; i < proj_nb; i++) {
		proj_idx[i]->update_anim();
	}
}

void World::update_targets()
{
	for (int i = 0; i < char_nb; i++) {
		Character* closest_foe = find_closest_foe(char_idx[i]);
		if (closest_foe) {
			char_idx[i]->set_target(closest_foe);
		}
	}
}

int World::box_collision(int x1, int y1, int w1, int h1, int x2, int y2, int w2, int h2)
{
	if ((((x1 > x2) && (x1 < x2 + w2)) || ((x1 + w1 > x2) && (x1 + w1 < x2 + w2))) &&
		(((y1 > y2) && (y1 < y2 + h2)) || ((y1 + h1 > y2) && (y1 + h1 < y2 + h2)))) {
		return 1;
	}
	else return 0;
};

int World::raycast(double x1, double y1, double x2, double y2)
{
	int return_value = 0;

	float deg = atan(abs(y1 - y2) / abs(x1 - x2));
	double step_x = 15 * cos(deg);
	double step_y = 15 * sin(deg);

	double tested_x = x1 + step_x;
	double tested_y = y1 + step_y;

	while (!return_value && (pow(x1 - tested_x, 2) < pow(x1 - x2, 2))) {
		if (wall_map[(int)(tested_y) / 32 * 175 + (int)(tested_x) / 32] > 4) return_value = 1;
		tested_x += step_x;
		tested_y += step_y;
	}
	return return_value;
}

Character* World::find_closest_foe(Character* origin)
{
	int origin_x, origin_y, target_x, target_y;
	int origin_team = origin->Get_team();
	origin->Get_pos(origin_x, origin_y);

	Character* best_pick = nullptr;
	int best_dist = 999999;

	for (int i = 0; i < char_nb; i++) {
		if ((char_idx[i]->Get_team() != origin_team) && char_idx[i]->is_active()) {
			char_idx[i]->Get_pos(target_x, target_y);
			//Bah ouai j'utilise pas cmath, et tu vas faire quoi hein ?
			int dist_pow2 = (origin_x - target_x) * (origin_x - target_x) + (origin_y - target_y) * (origin_y - target_y);
			if (dist_pow2 < best_dist && !raycast((double)origin_y, (double)origin_x, (double)target_y, (double)target_x)) {
				best_dist = dist_pow2;
				best_pick = char_idx[i];
			}
		}
	}
	return best_pick;
}