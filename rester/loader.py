import jsonpickle

from rester.struct import DictWrapper
import json
import os
import yaml
from rester.manifest import Variables


class TestSuite(object):
    def __init__(self, filename):
        self.filename = filename
        self.test_cases = []
        self.variables = Variables()
        self.load()

    def load(self):
        with open(self.filename) as fh:
            data = load(self.filename, fh)
            self._load(data)

    def _load(self, data):
        self.variables.update(data.get('globals', {}).get('variables', {}).items())
        for case in data['test_cases']:
            filename = os.path.join(os.path.dirname(self.filename), case)
            self.test_cases.append(TestCase(self, filename))

    def __getstate__(self):
        state = self.__dict__.copy()
        # del elements of state you don't want to pickle here
        return state

    def __setstate__(self, state):
        """
        behavior for unpickling. setting default values here
        :param state:
        :return:
        """
        # Manipulate state here before assigning it to our instance

        self.__dict__.update(state)


class TestCase(object):
    def __init__(self, suite):
        """
        generate a TestCase
        :param suite: none if not part of a suite.
        """
        self.variables = Variables()
        if suite:
            self.variables.update(suite.variables)

        self.testSteps = []

    @property
    def steps(self):
        return self.testSteps

    @property
    def request_opts(self):
        return self.variables.get('request_opts', {})

    def __getstate__(self):
        state = self.__dict__.copy()
        # del elements of state you don't want to pickle here
        return state

    def __setstate__(self, state):
        """
        behavior for unpickling. setting default values here
        :param state:
        :return:
        """
        # Manipulate state here before assigning it to our instance

        self.__dict__.update(state)


class TestStep(object):
    def __init__(self):
        """
        Initializing a default TestStep. Not used usually but here in case we need a default object to serialize.
        :return:
        """
        self.name = ""
        self.skip = False
        self.apiUrl = ""
        self.dumpResponse = True
        self.assertMap = {}
        self.headers = {}
        self.params = {}
        self.method = "get"

    def __getstate__(self):
        state = self.__dict__.copy()
        # del elements of state you don't want to pickle here
        return state

    def __setstate__(self, state):
        """
        behavior for unpickling. setting default values here
        :param state:
        :return:
        """
        # Manipulate state here before assigning it to our instance
        if not hasattr(state, 'skip'):
            state['skip'] = False

        self.__dict__.update(state)

