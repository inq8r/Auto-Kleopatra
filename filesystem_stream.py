from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer
import time
import re
import verification_data
import validate


class Handler(RegexMatchingEventHandler):
    """
    The file system event handler.
    It waits for the file and its signature (.sig) to appear, then runs verification.
    """
    
    def __init__(self, validation_service: validate.ValidateService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation_service = validation_service
        self.vd_obj = verification_data.VerificationData()

    def check_vd_obj(self):
        if hasattr(self.vd_obj, 'file') and hasattr(self.vd_obj, 'signature_file'):
            self.validation_service.do_validate(checked_data_obj=self.vd_obj)
            # Resetting an object to wait for a new pair
            self.vd_obj = verification_data.VerificationData()

    def on_created(self, event):
        if re.search(pattern=r'.*\.sig', string=event.src_path):
            self.vd_obj.signature_file = event.src_path
        else:
            self.vd_obj.file = event.src_path

        self.check_vd_obj()


class FileSystemMonitor:

    @staticmethod
    def create_handler(validator: validate.ValidateService) -> Handler:
        handler = Handler(
            validation_service=validator,
            regexes=[r'.*\.(txt|pdf|docx|odt|sig)'],
            ignore_directories=True,
            case_sensitive=False
        )
        return handler

    def start_observer(self, validator: validate.ValidateService, path_to_dir: str):
        event_handler = self.create_handler(validator=validator)
        observer = Observer()
        observer.schedule(event_handler=event_handler, path=path_to_dir)
        print(f'[ The observer is running, the monitored directory -- [{path_to_dir}] ]')
        observer.start()

        # An infinite loop for continuous operation of the observer
        try:
            while observer.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


def __tests():
    fs_monitor = FileSystemMonitor()
    validator = validate.ValidateService()
    fs_monitor.start_observer(validator=validator, path_to_dir='ver_data_folder')


if __name__ == '__main__':
    __tests()
