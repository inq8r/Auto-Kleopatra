import filesystem_stream
import validate
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '--path', type=str, required=True, help='Path to the monitored directory')

args = parser.parse_args()


if __name__ == '__main__':
    fs_monitor = filesystem_stream.FileSystemMonitor()
    validator = validate.ValidateService()
    fs_monitor.start_observer(validator=validator, path_to_dir=args.path)
