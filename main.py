import cv2
import time
import argparse
import numpy as np
from utils.carla import CarlaInstance
from utils.config import Config
from utils.viewer import Viewer


class PedestrianDetector:
    def __init__(self, args):
        self.config = Config(args)
        self.carla = None
        self.viewer = Viewer()

    def main(self):
        try:
            self.carla = CarlaInstance(self.config)
            self.carla.create_vehicle(
                with_rgb=True, listen_function=self.process_image)
            self.viewer.start()

            time.sleep(30)
        except Exception as e:
            print('Unexpected error:', e)
        finally:
            print('Cleaning world...')
            self.carla.clear_world()
            cv2.destroyAllWindows()

            return False

    def process_image(self, image, vehicle):
        i1 = np.array(image.raw_data)
        i2 = i1.reshape(self.config.args.height, self.config.args.width, 4)
        i3 = i2[:, :, :3]
        i4 = i3[..., ::-1].transpose((1, 0, 2))
        self.viewer.update_rgb(i4)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Pedestrian Detector')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '--width',
        metavar='W',
        default=640,
        type=int,
        help='Width of the image captured by the sensors (default: 640)')
    argparser.add_argument(
        '--height',
        metavar='H',
        default=480,
        type=int,
        help='Height of the image captured by the sensors (default: 480)')

    detector = PedestrianDetector(argparser.parse_args())
    detector.main()
