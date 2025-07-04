#pragma once
#define RYML_SINGLE_HDR_DEFINE_NOW

#include <vector>
#include <string>
#include <fstream>
#include <SDL.h>

#include "rapidyaml-0.9.0.hpp"

/**
* @brief an animated (or not) isometric object that can be freely moved
* This class is abstract, a simple BasicObject will not move
*/
class BasicObject
{
private:

	//[Object's position]//

	int x, y;	   //Coordinates of the center

	int vX, vY;	   //Velocity (useless here, made for inheritance)

	int w, h, e;   //width, height and elevation (distance from the ground)

	Uint32 lastUpdate;

	//[Object's Sprite]//

	std::string sheet;			   //Sprite Sheet

	int sX, sY;					   //coordinates od the first frame on the sheet

	int sW, sH;					   //Width and Height of the sprite

	int currentFrame, currentAnim; //Animation Control

	std::vector<unsigned int> animLengths;

	Uint32 lastFrame;

	//[Methods]//

	virtual void animate();

public:

	/**
	* @brief unserialize the specified object model
	* @return a Tree object from the rapid-yaml librairy
	*/
	static ryml::Tree loadModel(std::string model);

	/**
	* @brief BasicObject standard constructor
	* @param x the coordinate in the abciss axis where the object will be spawned
	* @param y the coordinate in the ordonates axis where the object will be spawned
	* @param model the unserialized object model (use the static "loadModel" method)
	*/
	BasicObject(int x, int y, ryml::Tree model);

	//BasicObject(const BasicObject& obj); //TODO

	/**
	* @brief update the object position and animation frame
	* @return true if the object is willing to die (average Health enjoyer)
	*/
	virtual bool update();

	const char* getSheet() { return sheet.c_str(); }

	SDL_Rect getFrame() { return {sX + currentFrame * sW, sY + currentAnim * sH, sW, sH}; }

	SDL_Rect getHitbox() { return { x - w / 2, y - h / 2, w, h }; }

	/**
	* @brief perform a box-shape collision check with an other object
	* @obj the object to check collision with
	*/
	bool collision(const BasicObject& obj);
};