from pathlib import Path

import platform
from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path

    request_permissions(
        [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
    )

    primary_ext_storage = Path(primary_external_storage_path())
    cutt_data_dir = Path(primary_ext_storage / "Clean up the tasks")
else:
    cutt_data_dir = Path.home() / "Clean up the tasks"

print(cutt_data_dir)

start_path = Path.home() / "cutt"


class sample:
    def path_append():
        return str(start_path) + "/dir"


# start_path.mkdir()
# start_file = start_path / "tseting1.json"
# start_file.touch()
# print(sample.path_append())
# print(start_path)
print(platform)  # kivy.utils
print(platform.system())  # platform

# n_path = Path("/home/dvo")
# Path(n_path / "cutt").mkdir()
