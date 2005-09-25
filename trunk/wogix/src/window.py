import cfilter

class Window:
    "A container for all window objects on a screen."

    full_screen_windows = cfilter.none
    
    def __init__(self, screen, window):
	"Create a window object managing WINDOW."

	self.screen = screen
	self.window = window
        self.wm = screen.wm	# So we can pass Windows to KeyHandlers.

	self.withdrawn = 0
	self.delayed_moveresize = 0

	self.current = 0
	self.focused = 0
	
	self.force_iconified = 0
	
	self.dispatch = event.WindowDispatcher(self.window)

	# Initial mapped state and geometry
	a = window.get_attributes()
	self.mapped = a.map_state != X.IsUnmapped

	r = self.window.get_geometry()
	self.x = r.x
	self.y = r.y
	self.width = r.width
	self.height = r.height
	self.border_width = r.border_width

    #
    # Internal methods
    #
    
    def withdraw(self, destroyed = 0):
	"""Window has been withdrawn.
	If DESTROYED is true the window doesn't exist anymore."""

	if self.withdrawn:
	    return

	self.mapped = 0
	self.withdrawn = 1

	# Clear the dispatcher to avoid cirkular references
	self.dispatch = event.SlaveDispatcher([])
	

    def handle_event(self, event, grabbed = 0):
	"""Handle EVENT for this client by calling its dispatch table. 
	"""
	self.dispatch.handle_event(event, grabbed)


    def get_focus(self, time):
	debug('focus', 'client gets focus: %s', self)
	self.focused = 1
        self.window.set_input_focus(X.RevertToPointerRoot, time)

    def lose_focus(self):
	debug('focus', 'client loses focus: %s', self)
	self.focused = 0

    #
    # External methods
    #
    
    def configure(self, **keys):
	if self.withdrawn:
	    return

	for i in ['x', 'y', 'width', 'height', 'border_width']:
	    setattr(self, i, keys.get(i, getattr(self, i)))

	apply(self.window.configure, (), keys)


    def is_mapped(self):
	return self.mapped

    def valid_window(self):
	"""Return true if the window still exists.
	"""
	if self.withdrawn:
	    return 0

	# Check for an invalid window by trigging BadDrawable
	# on a simple request
	try:
	    r = self.window.get_geometry()
	except error.BadDrawable:
	    return 0
	else:
	    return 1

    def resize(self, width, height):
	if self.withdrawn:
	    return
	self.window.configure(width = width, height = height)
	self.width = width
	self.height = height


    def move(self, x, y):
	if self.withdrawn:
	    return
	self.window.configure(x = x, y = y)
	self.x = x
	self.y = y


    def moveresize(self, x, y, width, height, delayed = 0):
	if self.withdrawn:
	    return

	# If client is iconified and delayed is true, don't actually
	# resize the window now but postpone it until deiconifying
	if self.mapped or not delayed:
	    self.window.configure(x = x, y = y, width = width, height = height)
	    self.delayed_moveresize = 0
	else:
	    self.delayed_moveresize = 1

	self.x = x
	self.y = y
	self.width = width
	self.height = height


    def setborderwidth(self, width):
	if self.withdrawn:
	    return
	self.window.configure(border_width = width)
	self.border_width = width


    def keep_on_screen(self, x, y, width, height):
	"""Return X, Y, WIDTH, HEIGHT after adjusting so the entire window
	is visible on the screen, including the border.
	"""

	if self.full_screen_windows(self):
	    root_x = 0
	    root_y = 0
	    root_width = self.screen.root_full_width
	    root_height = self.screen.root_full_height
	else:
	    root_x = self.screen.root_x
	    root_y = self.screen.root_y
	    root_width = self.screen.root_width
	    root_height = self.screen.root_height
	    
	# negative sizes is impossible
	if width < 0:
	    width = 0
	if height < 0:
	    height = 0

	# width and height must not be larger than the screen area
	if width + 2 * self.border_width > root_width:
	    width = root_width - 2 * self.border_width
	if height + 2 * self.border_width > root_height:
	    height = root_height - 2 * self.border_width

	# Move window if right/bottom edge is outside screen
	if (x + width + 2 * self.border_width 
	    > root_x + root_width):
	    x = (root_x + root_width
		 - width - 2 * self.border_width)
	    
	if (y + height + 2 * self.border_width
	    > root_y + root_height):
	    y = (root_y + root_height
		 - height - 2 * self.border_width)

	# Move window if left/top edge is outside screen
	if x < root_x:
	    x = root_x
	if y < root_y:
	    y = root_y

	return x, y, width, height

    def geometry(self):
	return self.x, self.y, self.width, self.height, self.border_width

    def get_top_edge(self):
	"""Return the y coordinate of the top edge of the client."""
	return self.y

    def get_bottom_edge(self):
	"""Return the y coordinate of the bottom edge of the client."""
	return self.y + self.height + 2 * self.border_width

    def get_left_edge(self):
	"""Return the x coordinate of the left edge of the client."""
	return self.x

    def get_right_edge(self):
	"""Return the x coordinate of the right edge of the client."""
	return self.x + self.width + 2 * self.border_width

    def pointer_position(self):
	"""Return the pointer x and y position relative to the window
	origin.  Return None if the pointer is on another screen.
	"""
	if self.withdrawn:
	    return None
	r = self.window.query_pointer()
	if r.same_screen:
	    return r.win_x, r.win_y
	else:
	    return None

    #
    # Window ops
    #

    def map(self):
        if self.withdrawn: return None
        self.window.map()

    def unmap(self):
        if self.withdrawn: return None
        self.window.unmap()

    def clear_area(self, *args, **keys):
        if self.withdrawn: return None
        apply(self.window.clear_area, args, keys)

    def fill_rectangle(self, gc, x, y, width, height, onerror = None):
        if self.withdrawn: return None
        self.window.fill_rectangle(gc, x, y, width, height, onerror)

    def image_text(self, gc, x, y, string, onerror = None):
        if self.withdrawn: return None
        self.window.image_text(gc, x, y, string, onerror)

    def draw_text(self, gc, x, y, text, onerror = None):
        if self.withdrawn: return None
        self.window.draw_text(gc, x, y, text, onerror)

    def convert_selection(self, selection, target, property, time, onerror = None):
        if self.withdrawn: return None
        self.window.convert_selection(selection, target, property, time, onerror)

    def destroy(self):
	if self.withdrawn:
	    return
        self.screen.remove_window(self.window)
	self.window.destroy()

    def raisewindow(self):
	if self.withdrawn:
	    return
	self.window.configure(stack_mode = X.Above)

    def lowerwindow(self):
	if self.withdrawn:
	    return
	self.window.configure(stack_mode = X.Below)

    def raiselower(self):
	if self.withdrawn:
	    return
	self.window.configure(stack_mode = X.Opposite)
