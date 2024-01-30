"""This module is used for application dynamic mapping.
Determine model from a specific key
"""

from abc import ABC, abstractmethod


class Mapper(ABC):
    @property
    @abstractmethod
    def apps_name_to_model_name(self):
        pass

    def get_model_name_from_apps_name(self, app_name):
        return self.apps_name_to_model_name[app_name]
