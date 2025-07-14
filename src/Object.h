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
protected:

	//[Object's status]//

	int maxHp;

	int hp;

	//[Object's position]//

	float x, y;			//Coordinates of the center

	int prevX, prevY;   //Backup coordinates in case of invalid placement

	int maxVx, maxVy;   //Maximum velocity

	int vX, vY;			//Velocity (useless here, made for inheritance)

	int w, h, e;		//width, height and elevation (distance from the ground)

	bool flip;

	Uint32 lastUpdate;

	//[Object's Sprite]//

	std::string sheet;			   //Sprite Sheet

	int sX, sY;					   //coordinates of the first frame on the sheet

	int sOffsetX, sOffsetY;		   //Position on the top-left corner of the sprite rel. to the top-left corner of the hitbox

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

	SDL_Rect getHitbox() { return { (int)x - w / 2, (int)y - h / 2, w, h }; }

	int getElevation() { return e; }

	bool fliped() { return flip; }

	int getOffsetX() { return sOffsetX; }

	int getOffsetY() { return sOffsetY; }

	/**
	* @brief put back the object at his previous location (in case of an invalid placement for ex.)
	* @param obj the object that was collided (null_ptr if it isn't an object of course)
	* @return true if the object must be destroyed
	*/
	void revert() { x = prevX; y = prevY; }

	/**
	* @brief perform a box-shape collision check with an other object
	* @obj the object to check collision with
	*/
	virtual bool collision(BasicObject& obj);

	/**
	* @brief perform a box-shape collision check with a rectangle area
	* @obj the area where to check collision as an SDL_Rect
	*/
	virtual bool collision(const SDL_Rect& rect);
};