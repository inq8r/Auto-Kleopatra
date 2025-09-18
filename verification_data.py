class VerificationData:
    file: str
    signature_file: str


def __tests():
    verification_data = VerificationData()
    verification_data.file = 'tracked_dir/file'
    verification_data.signature_file = 'tracked_dir/file.sig'
    print(vars(verification_data))


if __name__ == '__main__':
    __tests()
