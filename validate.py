import database
import verification_data
import pgpy
import warnings

warnings.filterwarnings(action='ignore')


class VerificationInterface:
    data_to_validate: verification_data.VerificationData

    def _reading_file(self) -> str:
        raise NotImplementedError

    def validation(self, keys: list):
        raise NotImplementedError


class VerificationDisconnectedData(VerificationInterface):

    def __init__(self, data_to_validate: verification_data.VerificationData):
        self.data_to_validate = data_to_validate

    def _reading_file(self):
        with open(file=self.data_to_validate.file, mode='rb') as file:
            file_bytes = file.read()
            return file_bytes

    def validation(self, keys: list):

        file = self._reading_file()

        sig = pgpy.PGPSignature.from_file(filename=self.data_to_validate.signature_file)

        for k in keys:
            pub, _ = pgpy.PGPKey.from_blob(blob=k)
            try:
                if pub.verify(subject=file, signature=sig):
                    print(f'Подпись для файла {self.data_to_validate.file} действительна.')
                    return
            except pgpy.errors.PGPError:
                continue
        print(f'Подпись для файла {self.data_to_validate.file} недействительна.')


class ValidateService:

    @staticmethod
    def do_validate(checked_data_obj: verification_data.VerificationData):
        verify = VerificationDisconnectedData(data_to_validate=checked_data_obj)
        keys_list = database.DataBaseAPI().get_keys()
        verify.validation(keys=keys_list)


def __tests():
    data_to_check = verification_data.VerificationData()
    data_to_check.file = 'tracked_dir/file'
    data_to_check.signature_file = 'tracked_dir/file.sig'
    verify = ValidateService()
    verify.do_validate(checked_data_obj=data_to_check)


if __name__ == '__main__':
    __tests()
