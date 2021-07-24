import os
import sys
import glob
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla


class CarlaInstance:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        print("Initializing CARLA client...")
        self.client = carla.Client(self.host, self.port)
        print('Listening to server %s:%d' % (self.host, self.port))

        self.world = self.client.get_world()
        self.map = self.world.get_map()
        self.blueprint_library = self.world.get_blueprint_library()
