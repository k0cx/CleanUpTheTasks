from pathlib import Path

# import platform
from kivy.utils import platform

from data.data_init import data_dir_init

data_dir_init()

print(cutt_data_dir)

start_path = Path.home() / "cutt"


class sample:
    def path_append():
        return str(start_path) + "/dir"


# n_path = Path("/home/dvo")
# Path(n_path / "cutt").mkdir()

# start_path.mkdir()
# start_file = start_path / "tseting1.json"
# start_file.touch()
# print(sample.path_append())
# print(start_path)

print(platform)  # kivy.utils
# print(platform.system())  # platform
