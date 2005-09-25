#include <stdlib.h>
#include <X11/Xlib.h>
#include <stdio.h>
#include <unistd.h>
#include <assert.h>

#define ZERO (0)

// ok, the actual code

int main()
{
	Display *dpy = XOpenDisplay(ZERO);
	assert(dpy);
	printf("Wogix 0.1alpha - Tab manager for Exigo\n");
};
