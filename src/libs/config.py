import pytoml as toml


class Config(dict):

    def __init__(self):
        self['aws'] = {
            'credentials': {
                'aws_access_key_id': '',
                'aws_secret_access_key': ''
            },
            'bucket': {
                'name': '',
                'path': '/'
            }
        }
        self['sync'] = {
            'root': {
                'path': '.'
            }
        }

    def load(self, path):
        self.clear()
        with open(path) as fp:
            self.update(toml.load(fp))

    def save(self, path):
        with open(path, 'w') as fp:
            toml.dump(fp, self)
