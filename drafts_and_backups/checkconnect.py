from pathlib import Path

# from cpuinfo import get_cpu_info  # py-cpuinfo
import hashlib
from cryptocode import encrypt, decrypt
from webdav3.client import Client  # webdavclient3
from webdav3.exceptions import WebDavException  # webdavclient3
import json
import platform


def generate_key_word():
    cpu_inf = str(
        str(platform.system())
        + str(platform.node())
        + str(platform.version())
        + str(platform.processor())
        + str(platform.architecture())
        + str(platform.machine())
    ).replace(" ", "")
    d = hashlib.sha256()
    d.update(cpu_inf.encode("utf-8", errors="ignore"))
    # with open(
    #     Path(__file__).parent.resolve() / "settings2.ini", "w", encoding="utf-8"
    # ) as file:
    #     file.write(d.hexdigest())
    return d.hexdigest()


def encrypt_word(word: str, key_word: str) -> str:
    return encrypt(key_word)


def decrypt_word(word: str, key_word: str) -> str:
    return decrypt(word, key_word)


def crypt_input():
    # sm = MDApp.get_running_app().root
    # key_word = "The best password for Clean_up_the_Tasks"
    # login = sm.ids.settings_screen.ids.login_field.text
    # password = sm.ids.settings_screen.ids.password_container.ids.password_field.text

    key_word = generate_key_word()
    login = encrypt("dvo.2103@mail.ru", key_word)
    password = encrypt(" ", key_word)

    data = {
        "webdav_hostname": "https://webdav.cloud.mail.ru",
        "webdav_login": login,
        "webdav_password": password,
    }

    settings_json = Path(__file__).parents[1] / "data/settings.json"
    with open(settings_json, "w", encoding="utf-8") as file:
        json.dump(data, file)


# crypt_input()


def check_client():
    settings_json = Path(__file__).parents[1] / "data/settings.json"
    with open(settings_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    key_word = generate_key_word()
    decrypt_data = {
        "webdav_login": decrypt(data["webdav_login"], key_word),
        "webdav_password": decrypt(data["webdav_password"], key_word),
    }
    data.update(decrypt_data)

    # login = decrypt(credentials["webdav_login"], key_word)
    # password = decrypt(credentials["webdav_password"], key_word)
    # data = {
    #     "webdav_hostname": credentials["webdav_hostname"],
    #     "webdav_login": login,
    #     "webdav_password": password,
    # }
    try:
        client = Client(data)
        my_files = client.list()
        print(my_files)
    except WebDavException as exception:
        print(exception)


check_client()


def json_dump():
    data = {
        "webdav_hostname": "https://webdav.cloud.mail.ru",
        "webdav_login": "super_login",
        "webdav_password": "super_password",
    }
    settings_json = Path(__file__).parents[1] / "data/settings.json"

    with open(settings_json, "w", encoding="utf-8") as file:
        json.dump(data, file)


# json_dump()


def json_load():
    settings_json = Path(__file__).parents[1] / "data/settings.json"
    with open(settings_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(data["webdav_login"], "\n:::\n", data["webdav_password"])


# json_load()


def cpu_information():
    cpu_inf = (
        "%s%s%s%s"
        % (
            get_cpu_info()["model"],
            get_cpu_info()["family"],
            "".join(get_cpu_info()["flags"]),
            get_cpu_info()["arch"],
        )
    ).replace(" ", "")

    print(cpu_inf)
