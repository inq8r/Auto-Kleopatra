import couchdb


class DataBaseAPI:
    database: couchdb.client.Database

    def __init__(self, server_addr: str = 'http://127.0.0.1:5984', database_name: str = 'your_db'):
        self.database = couchdb.Server(server_addr)[database_name]

    def get_keys(self, id_document: str = 'your_id') -> dict.values:
        response = self.database.get(id_document)
        del response['_id']
        del response['_rev']
        return response.values()


def __tests():
    db_api = DataBaseAPI()
    keys = db_api.get_keys()
    for k in keys:
        print(k)


if __name__ == '__main__':
    __tests()
