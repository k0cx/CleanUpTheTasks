from pathlib import Path

from kivy.utils import platform


class data_dir_init:
    def dir_init(self):
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

        if cutt_data_dir.exists() == False:
            cutt_data_dir.mkdir()
        if Path(cutt_data_dir / "attachments").exists() == False:
            Path(cutt_data_dir / "attachments").mkdir()
        return cutt_data_dir


# cutt_data_dir = data_dir_init().dir_init()

# print(globals().get("cutt_data_dir"))
# print(cutt_data_dir)
