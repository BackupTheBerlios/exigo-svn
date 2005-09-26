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
	cout << "Wogix 0.1alpha - Tab manager for Exigo\n";

	int blackColor = BlackPixel(dpy, DefaultScreen(dpy));
	int whiteColor = WhitePixel(dpy, DefaultScreen(dpy));

	Window w = XCreateSimpleWindow(dpy, DefaultRootWindow(dpy), 0, 0, 200, 100, 0, blackColor, blackColor);

	XSelectInput(dpy, w, StructureNotifyMask);

	XMapWindow(dpy, w);

	XFlush(dpy);

	sleep(10);
};
