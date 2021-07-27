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
    def __init__(self, config):
        self.host = config.args.host
        self.port = config.args.port
        self.width = config.args.width
        self.height = config.args.height

        self.sensors = {}
        self.vehicle = None

        print("Initializing CARLA client...")
        self.client = carla.Client(self.host, self.port)
        print('Listening to server %s:%d' % (self.host, self.port))

        self.world = self.client.get_world()
        self.map = self.world.get_map()
        self.blueprint_library = self.world.get_blueprint_library()

    def create_vehicle(self, with_rgb=False, listen_function=None):
        blueprint = self.blueprint_library.find('vehicle.lincoln.mkz2017')
        spawn_point = self.world.get_map().get_spawn_points()[0]
        self.vehicle = self.world.try_spawn_actor(blueprint, spawn_point)

        if with_rgb:
            camera_transform = carla.Transform(carla.Location(x=0.5, z=1.8))
            camera = self.blueprint_library.find('sensor.camera.rgb')
            camera.set_attribute('image_size_x', str(self.width))
            camera.set_attribute('image_size_y', str(self.height))
            camera.set_attribute('sensor_tick', '1.0')

            self.sensors['camera_rgb'] = self.world.spawn_actor(
                camera, camera_transform, attach_to=self.vehicle)

            if listen_function:
                self.sensors['camera_rgb'].listen(
                    lambda image: listen_function(image, self.vehicle))

        return self.vehicle

    def clear_world(self):
        for _, sensor in self.sensors.items():
            sensor.destroy()

        self.vehicle.destroy()
