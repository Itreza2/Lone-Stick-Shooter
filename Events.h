#pragma once
#include <SDL.h>
#include <iostream>

class Events
{
private:
	//Contain the key mapping
	unsigned int* mapping;

	//The queue of pending SDL events
	SDL_Event event;

public:
	//A list of booleans representing the state of each key mapped
	//1 is pressed and 0 is released
	unsigned char* is_pressed;

public:
	/*
	This constructor is supposed to read the user options file when it will be implemented
	*/
	Events();

	/*
	@Brief handle the pending SDL events
	@return 1 if the quit event has been called, otherwise 0;
	*/
	int catch_events();
};

