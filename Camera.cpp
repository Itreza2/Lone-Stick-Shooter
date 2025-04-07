#include "Camera.h"
using namespace std;

Camera::Camera(Character* target_, World* map_, Sprite_lib* sprites_, SDL_Rect render_rect_, unsigned int width_, unsigned int height_, int& err)
{
	err = 0;

	target = target_;
	map = map_;
	sprites = sprites_;
	render_rect = render_rect_;
	width = width_;
	height = height_;
	offset_x = 0;
	offset_y = 0;
	target_offset_x = 0;
	target_offset_y = 0;

	target_->Get_pos(top_left_x, top_left_y);
	top_left_x -= (int) width_ / 2;
	top_left_y -= (int) height_ / 2;

	h_map = (unsigned int*)malloc(sizeof(unsigned int) * (static_cast<unsigned long long>(width_) * height_));
	if (h_map == NULL) {
		err = 1;
	} else {
		for (unsigned int i = 0; i < width_ * height_; i++) h_map[i] = 0;
	}

	surface = SDL_CreateRGBSurfaceWithFormat(0, width_, height_, 32, SDL_PIXELFORMAT_RGB888);
	if (surface == NULL) err = 1;

	last_render_tick = SDL_GetTicks();
}

//WIP (not fool-proof yet)
int Camera::draw_floor()
{
	Uint32* pixels = (Uint32*)surface->pixels;
	Uint32* pixels_src = (Uint32*)sprites->floor_sheet->pixels;
	Uint32* pixels_w = (Uint32*)sprites->wall_sheet->pixels;
	Uint32* pixels_void = (Uint32*)sprites->void_sheet[(int)(SDL_GetTicks() / 60) % 40]->pixels;

	//Draw the floor tiles
	int tile;
	for (unsigned int i = 0; i <  height; i++) {
		for (unsigned int j = 0; j <  width; j++) {
			if (((i + top_left_x) > 0) && ((i + top_left_x) < (175 * 32)) && ((j + top_left_y) > 0) && ((j + top_left_y) < (175 * 32))
				&& ! map->get_collision((i + top_left_x) / 32, (j + top_left_y) / 32) && map->get_tile((i + top_left_x) / 32, (j + top_left_y) / 32) > 0) {
				tile = map->get_tile((i + top_left_x) / 32, (j + top_left_y) / 32);
				
				pixels[i * width + j] = pixels_src[((int)(tile / 16) * 32 + ((i + top_left_x) % 32)) * 512 + ((int)(tile % 16) * 32 + ((j + top_left_y) % 32))];
			}
			//Void
			else pixels[i * width + j] = pixels_void[((i + top_left_x) % 128) * 128 + ((j + top_left_y) % 128)];
		}
	}
	//Draw the solid tiles
	for (int i = top_left_x / 32; i < top_left_x / 32 + height / 32 + 2; i++) {
		for (int j = top_left_y / 32; j < top_left_y / 32 + width / 32 + 1; j++) {
			if (i >= 0 && i < 175 && j >= 0 && j < 175) {
				if (map->get_collision(i, j)) {
					this->draw_wall(i, j, pixels, pixels_w);
				}
			}
		}
	}
	return 0;//Currently no exeption raised... that was useless I guess
}

void Camera::draw_wall(int x, int y, Uint32* pixels, Uint32* pixels_w)
{
	int wall_heigth;
	int total_heigth;

	if (x >= 0 && x < 175 && y >= 0 && y < 175) {
		int tile = map->get_tile(x, y);

		if (tile == 0) {
			wall_heigth = 38;
			total_heigth = 70;
		} else {
			wall_heigth = 20;
			total_heigth = 52;
		}
		for (int i = 0; i < total_heigth; i++) {
			for (int j = 0; j < 32; j++) {
				if ((i + (x * 32) - top_left_x - wall_heigth > 0) && (i + (x * 32) - top_left_x - wall_heigth < height)
					&& (j + (y * 32) - top_left_y > 0) && (j + (y * 32) - top_left_y < width) 
					&& pixels_w[i * 224 + (tile * 32 + j)] != SDL_MapRGBA(surface->format, 0, 0, 0, 0)) {

					pixels[(i + (x * 32) - top_left_x - wall_heigth) * width + (j + (y * 32) - top_left_y)] = pixels_w[i * 224 + (tile * 32 + j)];

					h_map[(i + (x * 32) - top_left_x - wall_heigth) * width + (j + (y * 32) - top_left_y)] = total_heigth - i;
				}
			}
		}
	}
}

//BIG confusion between x and y
void Camera::draw_props()
{
	Prop* prop;
	Uint32* pixels = (Uint32*)surface->pixels;
	Uint32* pixels_src = (Uint32*)sprites->prop_sheet->pixels;
	int o, p;

	for (int i = 0; i < map->props_nb; i++) {
		prop = map->props_idx[i];

		if (prop->pos_x + prop->sprite_relx - top_left_x > 0 || prop->pos_x + prop->sprite_relx + prop->sprite_width - top_left_x < width ||
			prop->pos_y + prop->sprite_rely - top_left_y > 0 || prop->pos_y + prop->sprite_rely + prop->sprite_height - top_left_y < height) {
			
			o = 0;
			for (int x = prop->pos_y + prop->sprite_relx; x < prop->pos_y + prop->sprite_relx + prop->sprite_width; x++) {
				p = 0;
				for (int y = prop->pos_x + prop->sprite_rely; y < prop->pos_x + prop->sprite_rely + prop->sprite_height; y++) {
					if (y - top_left_x > 0 && y - top_left_x < height && x - top_left_y > 0 && x - top_left_y < width) {
						if (pixels_src[(p + prop->sheet_y) * 512 + (o + prop->sheet_x)] != SDL_MapRGBA(surface->format, 0, 0, 0, 0) && h_map[(y - top_left_x) * width + (x - top_left_y)] < prop->sprite_height - p) {
							pixels[(y - top_left_x) * width + (x - top_left_y)] = pixels_src[(p + prop->sheet_y) * 512 + (o + prop->sheet_x)];
							h_map[(y - top_left_x) * width + (x - top_left_y)] = prop->sprite_height - p;
						}
					} p++; //omg it append !!
				} o++;
			}
		}
	}
}

void Camera::draw_character(int char_idx, Uint32* pixels)
{
	int idx, anim, frame, dir, pos_x, pos_y, sheet_size, sprite_width, sprite_height;
	int wsprite_x, wsprite_y, wield_offset;
	int dmg_flag = map->char_idx[char_idx]->is_damaged();
	float deg;
	map->char_idx[char_idx]->Get_anim(idx, anim, frame, dir, deg);
	map->char_idx[char_idx]->Get_pos(pos_y, pos_x);
	sheet_size = stoi(sprites->character_anim[idx][3]);
	sprite_width = stoi(sprites->character_anim[idx][4]);
	sprite_height = stoi(sprites->character_anim[idx][4]);
	pos_y -= sprite_width / 2 + top_left_x;
	pos_x -= sprite_height / 2 + top_left_y;

	Uint32* pixels_src = (Uint32*)sprites->character_sheet[idx]->pixels;
	Uint32* pixels_wsrc = (Uint32*)sprites->weapons_sheet->pixels;
	Uint32* pixels_msrc = (Uint32*)sprites->muzzle_sheet->pixels;
	int current_pixel = 0;

	if ((pos_x + sprite_width / 2 > 0 || pos_x - sprite_width / 2 < width) &&
		(pos_y + sprite_height / 2 > 0 || pos_y - sprite_height / 2 < height)) {
		
		//Character's own sprite
		for (int i = 0; i < sprite_width; i++) {
			for (int j = 0; j < sprite_height; j++) {

				if (pos_x + i >= 0 && pos_x + i < width && pos_y + j >= 0 && pos_y + j < height) {

					if (dir == 1) {
						current_pixel = (j + sprite_height * anim) * sheet_size + (i + sprite_width * frame);
					}
					else {
						current_pixel = (j + sprite_height * anim) * sheet_size + ((sprite_width - i) + sprite_width * frame);
					}
					if (pixels_src[current_pixel] != SDL_MapRGBA(sprites->character_sheet[idx]->format, 0, 0, 0, 0) && h_map[(pos_y + j) * width + (pos_x + i)] < 62 - j) {

						if (dmg_flag)
							pixels[(pos_y + j) * width + (pos_x + i)] = SDL_MapRGBA(surface->format, 255, 255, 255, 255);
						else
							pixels[(pos_y + j) * width + (pos_x + i)] = pixels_src[current_pixel];
						h_map[(pos_y + j) * width + (pos_x + i)] = 62 - j;
					}
				}
			}
		}
		//Character's weapon sprite
		if (map->char_idx[char_idx]->weapon != NULL) {
			pos_x += sprite_width / 2;
			pos_y += sprite_height / 2 + sprite_height / 10;
			//We re-use sprite_width and sprite_height for conveniance
			map->char_idx[char_idx]->weapon->Get_sprite(wsprite_x, wsprite_y, sprite_width, sprite_height, wield_offset);
			//pos_x and pos_y will be the origin of our rotation

			int src_x, src_y, length;
			if (sprite_width > sprite_height) length = sprite_width;
			else length = sprite_height;

			for (int i = pos_x - length; i < pos_x + length; i++) {
				for (int j = pos_y - length; j < pos_y + length; j++) {

					//Calculation of the corresponding pixel on the source image
					if (dir == 1) {
						src_x = (int)((i - pos_x) * cos(deg) + (j - pos_y) * sin(deg)) + sprite_width / 2 - wield_offset;
						src_y = (int)(-(i - pos_x) * sin(deg) + (j - pos_y) * cos(deg)) + sprite_height / 2;
					} else {
						src_x = (int)((i - pos_x) * cos(deg) - (j - pos_y) * sin(deg)) + sprite_width / 2 + wield_offset;
						src_y = (int)((i - pos_x) * sin(deg) + (j - pos_y) * cos(deg)) + sprite_height / 2;
					}
					//cout << (62 - ((62 - length) / 2)) - (j - pos_y + length) << endl;
					if (src_x > 0 && src_x < sprite_width && src_y > 0 && src_y < sprite_height &&
						i > 0 && i < width && j >=0  && j < height) {
						if (dir == 1) {
							if (pixels_wsrc[(wsprite_y + src_y) * 420 + (wsprite_x + src_x)] != 16752479 &&  //16752479 correspond to some kind of orange
								h_map[j * width + i] < (62 - ((62 - length) / 2)) - (j - pos_y + length) + 31) {
								if (!dmg_flag)
									pixels[j * width + i] = pixels_wsrc[(wsprite_y + src_y) * 420 + (wsprite_x + src_x)];
								else
									pixels[j * width + i] = SDL_MapRGBA(surface->format, 255, 255, 255, 255);
							}
						} else {
							if (pixels_wsrc[(wsprite_y + src_y) * 420 + ((sprite_width - src_x) + wsprite_x)] != 16752479 &&
								h_map[j * width + i] < (62 - ((62 - length) / 2)) - (j - pos_y + length) + 31) {
								if (!dmg_flag)
									pixels[j * width + i] = pixels_wsrc[(wsprite_y + src_y) * 420 + ((sprite_width - src_x) + wsprite_x)];
								else
									pixels[j * width + i] = SDL_MapRGBA(surface->format, 255, 255, 255, 255);
							}
						}
					}
				}
			}
			//Draw the muzzle flash when the weapon has been fired
			if (map->char_idx[char_idx]->weapon->muzzle_flag) {
				map->char_idx[char_idx]->weapon->muzzle_flag--;

				int src_x, src_y, length, radius;
				int muzzle_type = map->char_idx[char_idx]->weapon->Get_muzzle(radius);
				wsprite_x = stoi(sprites->muzzle_data[muzzle_type][1]);
				wsprite_y = stoi(sprites->muzzle_data[muzzle_type][2]);
				sprite_width = stoi(sprites->muzzle_data[muzzle_type][3]);
				sprite_height = stoi(sprites->muzzle_data[muzzle_type][4]);

				if (sprite_width > sprite_height) length = sprite_width;
				else length = sprite_height;

				pos_x += cos(deg) * (radius) * dir;
				pos_y += sin(deg) * (radius);

				for (int i = pos_x - length; i < pos_x + length; i++) {
					for (int j = pos_y - length; j < pos_y + length; j++) {

						//Calculation of the corresponding pixel on the source image
						if (dir == 1) {
							src_x = (int)((i - pos_x) * cos(deg) + (j - pos_y) * sin(deg)) + sprite_width / 2;
							src_y = (int)(-(i - pos_x) * sin(deg) + (j - pos_y) * cos(deg)) + sprite_height / 2;
						}
						else {
							src_x = (int)((i - pos_x) * cos(deg) - (j - pos_y) * sin(deg)) + sprite_width / 2;
							src_y = (int)((i - pos_x) * sin(deg) + (j - pos_y) * cos(deg)) + sprite_height / 2;
						}
						if (src_x > 0 && src_x < sprite_width && src_y > 0 && src_y < sprite_height &&
							i > 0 && i < width && j >= 0 && j < height) {
							if (dir == 1) {
								if (pixels_msrc[(wsprite_y + src_y) * 376 + (wsprite_x + src_x)] != SDL_MapRGBA(surface->format, 0, 0, 0, 0) &&
									h_map[j * width + i] < 32) {
									pixels[j * width + i] = pixels_msrc[(wsprite_y + src_y) * 376 + (wsprite_x + src_x)];
									h_map[j * width + i] = 32;
								}
							}
							else {
								if (pixels_msrc[(wsprite_y + src_y) * 376 + ((sprite_width - src_x) + wsprite_x)] != SDL_MapRGBA(surface->format, 0, 0, 0, 0) &&
									h_map[j * width + i] < 32) {
									pixels[j * width + i] = pixels_msrc[(wsprite_y + src_y) * 376 + ((sprite_width - src_x) + wsprite_x)];
									h_map[j * width + i] = 32;
								}
							}
						}
					}
				}
			}
		}
	}
}

void Camera::draw_bullet(int proj_idx, Uint32* pixels)
{
	int idx, frame, dir, pos_x, pos_y, sprite_width, sheet, anim_x, anim_y;
	float deg;
	map->proj_idx[proj_idx]->Get_anim(idx, sheet, frame, dir, deg);
	map->proj_idx[proj_idx]->Get_pos(pos_x, pos_y);
	sprite_width = stoi(sprites->bullet_anim[idx][4]);
	anim_x = stoi(sprites->bullet_anim[idx][2]);
	anim_y = stoi(sprites->bullet_anim[idx][3]);
	pos_y -= top_left_x;
	pos_x -= top_left_y;

	Uint32* pixels_src = (Uint32*)sprites->bullet_sheet[sheet]->pixels;
	int current_pixel = 0;
	int src_x, src_y;

	if ((pos_x + sprite_width / 2 > 0 || pos_x - sprite_width / 2 < width) &&
		(pos_y + sprite_width / 2 > 0 || pos_y - sprite_width / 2 < height)) {

		//Bullet's sprite
		for (int i = -sprite_width; i < sprite_width; i++) {
			for (int j = -sprite_width; j < sprite_width; j++) {

				//Calculation of the corresponding pixel on the source image
				if (dir == 1) {
					src_x = (int)((i) * cos(deg) + (j) * sin(deg)) + sprite_width / 2;
					src_y = (int)(-(i) * sin(deg) + (j) * cos(deg)) + sprite_width / 2;
				}
				else {
					src_x = (int)((i) * cos(deg) - (j) * sin(deg)) + sprite_width / 2;
					src_y = (int)((i) * sin(deg) + (j) * cos(deg)) + sprite_width / 2;
				}

				if (pos_x + i >= 0 && pos_x + i < width && pos_y + j >= 0 && pos_y + j < height) {
					if (src_x > 0 && src_x < sprite_width && src_y > 0 && src_y < sprite_width) {
						if (dir == 1) {
							current_pixel = (src_y + anim_y) * 640 + (src_x + anim_x + sprite_width * frame);
						}
						else {
							current_pixel = (src_y + anim_y) * 640 + ((sprite_width - src_x) + anim_x + sprite_width * frame);
						}
						if (pixels_src[current_pixel] != SDL_MapRGBA(surface->format, 0, 0, 0, 0) && h_map[(pos_y + j) * width + (pos_x + i)] < 30) {
							pixels[(pos_y + j) * width + (pos_x + i)] = pixels_src[current_pixel];
							h_map[(pos_y + j) * width + (pos_x + i)] = 30;
						}
					}
				}
			}
		}
	}
}

void Camera::draw_text(int text_idx)
{
	SDL_BlitSurface(map->text_idx[text_idx]->surface, NULL, surface, map->text_idx[text_idx]->get_rect(top_left_x, top_left_y));
}

void Camera::set_offset()
{
	int useless_var;
	float target_aim_deg;
	target->Get_anim(useless_var, useless_var, useless_var, useless_var, target_aim_deg);

	if (useless_var > 0) target_aim_deg += 3.14;

	target_offset_x = -((Player*)target)->get_target_distance() * 0.3 * sin(target_aim_deg * useless_var);
	target_offset_y = -((Player*)target)->get_target_distance() * 0.3 * cos(target_aim_deg);

	if (target_offset_x > 0) target_offset_x = min(target_offset_x, MAX_X_OFFSET);
	else target_offset_x = max(target_offset_x, -MAX_X_OFFSET);
	if (target_offset_y > 0) target_offset_y = min(target_offset_y, MAX_Y_OFFSET);
	else target_offset_y = max(target_offset_y, -MAX_Y_OFFSET);

	if (abs(offset_x - target_offset_x) < 4) offset_x = target_offset_x;
	else {
		if (offset_x > target_offset_x) offset_x -= (last_render_tick / 8000);
		if (offset_x < target_offset_x) offset_x += (last_render_tick / 8000);
	}
	if (abs(offset_y - target_offset_y) < 4) offset_y = target_offset_y;
	else {
		if (offset_y > target_offset_y) offset_y -= (last_render_tick / 8000);
		if (offset_y < target_offset_y) offset_y += (last_render_tick / 8000);
	}
}

//Placeholder
void Camera::draw_frame(SDL_Renderer* render)
{
	for (unsigned int i = 0; i < width * height; i++) h_map[i] = 0;

	target->Get_pos(top_left_x, top_left_y);

	set_offset();
	top_left_x -= (int)height / 2 - offset_x;
	top_left_y -= (int)width / 2 - offset_y;

	SDL_LockSurface(surface);
	Uint32* pixels = (Uint32*)surface->pixels;
	SDL_LockSurface(sprites->floor_sheet);
	SDL_LockSurface(sprites->prop_sheet);

	draw_floor();
	draw_props();
	for (int i = 0; i < map->char_nb; i++) {
		draw_character(i, pixels);
	}
	for (int i = 0; i < map->proj_nb; i++) {
		draw_bullet(i, pixels);
	}
	last_render_tick = SDL_GetTicks();

	SDL_UnlockSurface(surface);
	SDL_UnlockSurface(sprites->floor_sheet);
	SDL_UnlockSurface(sprites->prop_sheet);
	
	for (int i = 0; i < map->text_idx.size(); i++) {
		draw_text(i);
	}

	SDL_Texture* text = SDL_CreateTextureFromSurface(render, surface);
	SDL_RenderCopy(render, text, NULL, &render_rect);
	SDL_DestroyTexture(text);
}