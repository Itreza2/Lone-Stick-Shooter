#include "AssetsManager.h"

AssetsManager* AssetsManager::getManager()
{
	if (instance == nullptr) {
		instance = new AssetsManager();
	}
	return instance;
}

AssetsManager::AssetsManager()
{
	sheets = {};
	fonts = {};
}

void AssetsManager::loadGroup(std::string path, SDL_Renderer* renderer)
{
	std::ifstream loader;
	loader.open(path);

	std::string line, word;
	std::stringstream stream;
	std::vector<std::string> row;
	SDL_Surface* surface;
	SDL_Surface* surfaceRGBA;
	TTF_Font* font;

	while (std::getline(loader, line)) {
		stream = std::stringstream(line);
		row.clear();

		while (std::getline(stream, word, ','))
			row.push_back(word);

		if (!row[0].compare("SHEET")) {
			surface = IMG_Load(row[2].c_str());
			if (surface == NULL) {
				std::cout << "ERROR : Failed to load " << row[2] << std::endl;
			}
			else {
				//A simple conversion of the surface does not work, but SDL_Blit handle the conversion well
				surfaceRGBA = SDL_CreateRGBSurfaceWithFormat(0, surface->w, surface->h, 32, SDL_PIXELFORMAT_RGBA8888);
				SDL_BlitSurface(surface, NULL, surfaceRGBA, NULL);
				sheets.insert({ row[1], new SuperSurface(std::move(*surfaceRGBA)) });
				SDL_FreeSurface(surface);
			}
		}
		else if (!row[0].compare("TEXTURE")) {
			surface = IMG_Load(row[2].c_str());
			if (surface == NULL) {
				std::cout << "ERROR : Failed to load " << row[2] << std::endl;
			}
			else {
				SDL_ConvertSurfaceFormat(surface, SDL_PIXELFORMAT_RGBA8888, 0);
				textures.insert({ row[1], SDL_CreateTextureFromSurface(renderer, surface)});
				SDL_FreeSurface(surface);

				if (row.size() == 4) {
					SDL_SetTextureAlphaMod(textures[row[1]], stoi(row[3]));
				}
			}
		}
		else if (!row[0].compare("FONT")) {
			font = TTF_OpenFont(row[2].c_str(), stoi(row[3]));
			if (font == NULL) {
				std::cout << "OUH ! OUH ! Assassin de la police " << row[3] << std::endl;
			}
			else {
				fonts.insert({ row[1], font });
			}
		}
	}
}