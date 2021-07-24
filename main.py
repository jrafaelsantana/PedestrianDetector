from src.carla import CarlaInstance
import argparse


def main():
    argparser = argparse.ArgumentParser(
        description='Pedestrian Detector')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    args = argparser.parse_args()

    carla = CarlaInstance(args.host, args.port)


if __name__ == '__main__':
    main()
