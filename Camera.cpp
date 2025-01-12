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
}

//WIP (not fool-proof yet)
int Camera::draw_floor()
{
	Uint32* pixels = (Uint32*)surface->pixels;
	Uint32* pixels_src = (Uint32*)sprites->floor_sheet->pixels;
	Uint32* pixels_w = (Uint32*)sprites->wall_sheet->pixels;
	Uint32* pixels_void = (Uint32*)sprites->void_sheet->pixels;

	//Draw the floor tiles
	int tile;
	for (unsigned int i = 0; i <  height; i++) {
		for (unsigned int j = 0; j <  width; j++) {
			if (((i + top_left_x) > 0) && ((i + top_left_x) < (175 * 32)) && ((j + top_left_y) > 0) && ((j + top_left_y) < (175 * 32))
				&& ! map->get_collision((i + top_left_x) / 32, (j + top_left_y) / 32) && map->get_tile((i + top_left_x) / 32, (j + top_left_y) / 32) > 0) {
				tile = map->get_tile((i + top_left_x) / 32, (j + top_left_y) / 32);
				pixels[i * width + j] = pixels_src[((int)(tile / 16) * 32 + ((i + top_left_x) % 32)) * 512 + ((int)(tile % 16) * 32 + ((j + top_left_y) % 32))];
			}
			else pixels[i * width + j] = pixels_void[((i + top_left_x / 2) % 512) * 512 + ((j + top_left_y / 2 + (int)SDL_GetTicks() / 50) % 512)];
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
	if (x >= 0 && x < 175 && y >= 0 && y < 175) {
		int tile = map->get_tile(x, y);
		for (int i = 0; i < 52; i++) {
			for (int j = 0; j < 32; j++) {
				if ((i + (x * 32) - top_left_x - 20 > 0) && (i + (x * 32) - top_left_x - 20 < height)
					&& (j + (y * 32) - top_left_y > 0) && (j + (y * 32) - top_left_y < width)) {

					pixels[(i + (x * 32) - top_left_x - 20) * width + (j + (y * 32) - top_left_y)] = pixels_w[i * 224 + (tile * 32 + j)];

					h_map[(i + (x * 32) - top_left_x - 20) * width + (j + (y * 32) - top_left_y)] = 54 - i;
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
	map->char_idx[char_idx]->Get_anim(idx, anim, frame, dir);
	map->char_idx[char_idx]->Get_pos(pos_x, pos_y);
	sheet_size = stoi(sprites->character_anim[idx][3]);
	sprite_width = stoi(sprites->character_anim[idx][4]);
	sprite_height = stoi(sprites->character_anim[idx][4]);
	pos_x -= sprite_width / 2 + top_left_x;
	pos_y -= sprite_height / 2 + top_left_y;

	Uint32* pixels_src = (Uint32*)sprites->character_sheet[idx]->pixels;
	int current_pixel = 0;

	if ((pos_x + sprite_width / 2 > top_left_x || pos_x - sprite_width / 2 < top_left_x + width) &&
		(pos_y + sprite_height / 2 > top_left_y || pos_y - sprite_height / 2 < top_left_y + height)) {
		for (int i = 0; i < sprite_width; i++) {
			for (int j = 0; j < sprite_height; j++) {

				if (pos_x + i >= 0 && pos_x + i < width && pos_y + j >= 0 && pos_y + j < height) {

					if (dir == 1) {
						current_pixel = (j + sprite_height * anim) * sheet_size + (i + sprite_width * frame);
					}
					else {
						current_pixel = (j + sprite_height * anim) * sheet_size + ((sprite_width - i) + sprite_width * frame);
					}
					if (pixels_src[current_pixel] != SDL_MapRGBA(surface->format, 0, 0, 0, 0) && h_map[(pos_y + j) * width + (pos_x + i)] < 62 - j) {
						pixels[(pos_y + j) * width + (pos_x + i)] = pixels_src[current_pixel];
						h_map[(pos_y + j) * width + (pos_x + i)] = 62 - j;
					}
				}

			}
		}
	}
}

//Placeholder
void Camera::draw_frame(SDL_Renderer* render)
{
	for (unsigned int i = 0; i < width * height; i++) h_map[i] = 0;

	target->Get_pos(top_left_x, top_left_y);
	top_left_x -= (int)width / 2;
	top_left_y -= (int)height / 2;

	SDL_LockSurface(surface);
	Uint32* pixels = (Uint32*)surface->pixels;
	SDL_LockSurface(sprites->floor_sheet);
	SDL_LockSurface(sprites->prop_sheet);
	SDL_LockSurface(sprites->void_sheet);

	this->draw_floor();
	this->draw_props();
	for (int i = 0; i < map->char_nb; i++) {
		this->draw_character(i, pixels);
	}

	SDL_UnlockSurface(surface);
	SDL_UnlockSurface(sprites->floor_sheet);
	SDL_UnlockSurface(sprites->prop_sheet);
	SDL_UnlockSurface(sprites->void_sheet);

	SDL_Texture* text = SDL_CreateTextureFromSurface(render, surface);
	SDL_RenderClear(render);
	SDL_RenderCopy(render, text, &render_rect, NULL);
	SDL_RenderPresent(render);
	SDL_DestroyTexture(text);
}