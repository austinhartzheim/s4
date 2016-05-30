import json
import os

import libs.errors


class S4Project():
    '''
    An abstraction of the hidden .s4 data directory.
    '''

    def __init__(self, path):
        '''
        :param str path: a path to a .s4 directory.
        '''
        self.s4path = path
        self.path = os.path.split(path)[0]

    @classmethod
    def create_by_search(cls, path):
        '''
        Search all parent directories of `path` until a .s4 directory
        is found. Return's an S4Project instance using that path.
        :param str path: the path to begin searching in. For example,
          this might be the current working directory.
        :returns S4Project: when a .s4 directory is found.
        :raises libs.errors.NotInS4Project: when a .s4 directory cannot
          be found in any parent directories.
        '''
        while path != '/':
            test_path = os.path.join(path, '.s4')
            if os.path.exists(test_path):
                return cls(test_path)
            else:
                path = os.path.split(path)[0]

        raise libs.errors.NotInS4Project('You are not in an S4 project.')


class ModificationFinder():
    FILE_NAME = 'modification-state.json'

    def __init__(self, s4project):
        self.s4project = s4project
        self.data = {}

    def find_modifications(self):
        '''
        Find modified files.
        '''
        pass

    def load(self):
        path = os.path.join(self.s4project.s4path, self.FILE_NAME)
        try:
            fp = open(path)
            self.data = json.load(fp)
            self.data_loaded = True
        except OSError as err:
            # TODO: better error message to cover traceback
            print('Could not read modification state.')
            # TODO: try to recover
            raise err
        finally:
            fp.close()

    def save(self):
        path = os.path.join(self.s4project.s4path, self.FILE_NAME)
        try:
            fp = open(path, 'w')
            json.dump(self.data, fp)
        except OSError as err:
            # TODO: better error message to cover traceback
            print('Could not write file modification state.')
            print('This might cause additional synchronization to occur.')
            # TODO: try to recover
            raise err
        finally:
            fp.close()
