#pragma once
#include <SDL.h>
#include <SDL_image.h>
#include <SDL_ttf.h>
#include <unordered_map>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <iostream>

#include "SuperSurface.h"

/*
TODO :
-> Font loader (and ttf files by the way)
-> Failsafes when trying to access an asset that isn't loaded
*/

/**
* @brief a singleton that load SLD assets and make them accessible in a convenient way
*/
class AssetsManager
{
private:

	static AssetsManager* instance;

	std::unordered_map<std::string, SuperSurface*> sheets;

	std::unordered_map<std::string, SDL_Texture*> textures;

	std::unordered_map<std::string, TTF_Font*> fonts;

	AssetsManager();

public:

	static AssetsManager* getManager(); //The Karen method, I guess...

	SuperSurface* getSheet(std::string name) { return sheets[name]; }
	
	SDL_Texture* getTexture(std::string name) { return textures[name]; }

	TTF_Font* getFont(std::string name) { return fonts[name]; }

	/**
	* @brief load a group of assets listed in a text file
	* @param path the adress of the reference file
	* @param renderer the SDL renderer on which textures will be rendered
	*/
	void loadGroup(std::string path, SDL_Renderer* renderer);
};

AssetsManager* AssetsManager::instance = nullptr;