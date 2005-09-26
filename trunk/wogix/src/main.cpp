#include <stdlib.h>
#include <X11/Xlib.h>
#include <unistd.h>
#include <assert.h>
#include <iostream>

using namespace std;

#define ZERO (0)

// ok, the actual code

int main()
{
	Display *dpy = XOpenDisplay(ZERO);
	assert(dpy);
	cout<<"Wogix 0.1alpha - Tab manager for Exigo\n";
};
