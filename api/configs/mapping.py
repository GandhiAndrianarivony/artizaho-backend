from .base import Mapper


class MapConfiguration(Mapper):
    apps_name_to_model_name = dict(users="User", artisans="Artisan")
