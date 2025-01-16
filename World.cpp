#include "World.h"

//TODO : actual world generation
World::World(Character* player1)
{
	int first_x, first_y;

	props_idx = {};
	props_nb = 0;

	char_idx = { player1 };
	char_nb = 1;

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
	}
}

void World::generate_tiles()
{
	for (int i = 0; i < 175 * 175; i++) {
		
		switch (wall_map[i]) {

		case 1://Grass tile
			tile_map[i] = (rand() % 8) * 16 + (rand() % 8);
			if (tile_map[i] == 0) tile_map[i] = 1;//No idea why this is necessary ¯\_(ツ)_/¯
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
			tile_map[i] = 0;
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
		player1->set_pos(pos_y * (35) * 32 + 736, pos_x * (35) * 32 + 384);
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
			} if (room_map[(i * 5 + j) * 2] == 2) {
				magic = (char)(rand() % 6) + '0'; //Currently 6 types of size 2 rooms
				file_path = "files\\roomLayers\\2\\";
				file_path = file_path + magic;
				file_path = file_path + ".txt";
				fopen_s(&file, file_path.c_str(), "r");
				if (file != NULL) {
					for (int k = 0; k < 289; k++) {
						car = fgetc(file);
						if (car == '\n') car = fgetc(file);
						wall_map[((k / 17) + (j * 35 + 9)) * 175 + (k % 17) + (i * 35 + 9)] = (int)(car - '0');
					} fclose(file);
				} this->place_props(i * 35 + 9, j * 35 + 9, 17);
			} if (room_map[(i * 5 + j) * 2] == 3) {
				magic = (char)(rand() % 4) + '0'; //Currently 4 types of size 2 rooms
				file_path = "files\\roomLayers\\3\\";
				file_path = file_path + magic;
				file_path = file_path + ".txt";
				fopen_s(&file, file_path.c_str(), "r");
				if (file != NULL) {
					for (int k = 0; k < 529; k++) {
						car = fgetc(file);
						if (car == '\n') car = fgetc(file);
						wall_map[((k / 23) + (j * 35 + 6)) * 175 + (k % 23) + (i * 35 + 6)] = (int)(car - '0');
					} fclose(file);
				} this->place_props(i * 35 + 6, j * 35 + 6, 23);
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
	Prop* new_prop;
	vector<string> csv;
	int position_correct;

	cout << "gen" << endl;

	for (int i = 0; i < width; i++) {
		csv = CSV_read_row("files\\Ruin\\prop.csv", rand() % 3);
		pos_x = (rand() % (width * 32)) + (top_left_y * 32);
		pos_y = (rand() % (width * 32)) + (top_left_x * 32);

		position_correct = 1;
		for (int x = pos_x / 32; x <= (pos_x + stoi(csv[2])) / 32; x++) {
			for (int y = pos_y / 32; y <= (pos_y + stoi(csv[1])) / 32; y++) {
				if (wall_map[x * 175 + y] != 2) position_correct = 0;
			}
		}
		if (position_correct) {
			new_prop = (Prop*)malloc(sizeof(Prop));
			if (new_prop != NULL) {
				new_prop->pos_x = pos_x;
				new_prop->pos_y = pos_y;
				new_prop->hbox_width = stoi(csv[1]);
				new_prop->hbox_height = stoi(csv[2]);
				new_prop->sprite_relx = stoi(csv[3]);
				new_prop->sprite_rely = stoi(csv[4]);
				new_prop->sprite_width = stoi(csv[5]);
				new_prop->sprite_height = stoi(csv[6]);
				new_prop->sheet_x = stoi(csv[7]);
				new_prop->sheet_y = stoi(csv[8]);

				props_idx.push_back(new_prop);
				props_nb++;
			}
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

	for (int i = 0; i < char_nb; i++) {
		char_idx[i]->Get_pos(cpos_x, cpos_y);
		char_idx[i]->Get_ground_hitbox(pos_x, pos_y, width, height);
		pos_x += cpos_y + 168;                                             //I don't know why this 168px offset is a thing...
		pos_y += cpos_x - 168;

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
	}
}