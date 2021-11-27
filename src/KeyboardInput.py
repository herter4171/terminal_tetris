from pynput import keyboard
from shapely.geometry import Point
from shapely.affinity import translate


class KeyBoardInput(object):

    __move_vecs = {
        'Key.right': Point(1, 0),
        'Key.left': Point(-1, 0),
        'Key.down': Point(0, 1)
    }

    __rotate_map = {
        'q': -90,
        'e': 90
    }

    @property
    def translate_vec(self):
        """Returns translation vector based on pressed arrow keys."""
        final_vec = Point(0, 0)

        for curr_key, curr_vec in KeyBoardInput.__move_vecs.items():
            if curr_key in self._pressed_keys:
                final_vec = translate(final_vec, curr_vec.x, curr_vec.y)

        return final_vec

    @property
    def rotate_angle(self):
        """Returns angle to rotate active block by."""
        final_angle = 0.0

        for curr_key, curr_angle in KeyBoardInput.__rotate_map.items():
            if curr_key in self._pressed_keys:
                final_angle += curr_angle

        return final_angle

    def __init__(self):
        """Instantiate by creating keyboard listener and pressed key set."""
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release = self._on_release
        )

        self._listener.start()
        self._pressed_keys = set()

    def __str__(self):
        return "Pressed keys: " + str(self._pressed_keys) + '\n'

    def _get_key_name(self, key):
        return str(key).replace("'", "")

    def _on_press(self, key):
        """Add key to pressed key set if not present."""
        key_name = self._get_key_name(key)

        if key_name not in self._pressed_keys:
            self._pressed_keys.add(key_name)

    def _on_release(self, key):
        """Remove key from pressed keys if present."""
        key_name = self._get_key_name(key)

        if key_name in self._pressed_keys:
            self._pressed_keys.remove(key_name)
