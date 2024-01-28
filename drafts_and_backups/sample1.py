from pathlib import Path
import platform


start_path = Path.home() / "cutt"


class sample:
    def path_append():
        return str(start_path) + "/dir"


# start_path.mkdir()
# start_file=start_path / "tseting1.json"
# start_file.touch()
# print(sample.path_append())
# print(start_path.exists())
# print(platform.system())
