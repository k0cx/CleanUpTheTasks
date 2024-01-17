import cpuinfo  # py-cpuinfo
import hashlib


def get_hardware_id():
    """
    Get an unique hardware ID, based on CPU info. All the times called, the value will be the same.
    >>> get_hardware_id()
    'f8ef57d64aae6f3c45200b39di422bd6ca625d9a79655cb3aa6e171ef6f93013aa16c2df2f2b0359dfaf1782ba6fda94300506cdd9b21fdaf1264fbd0e47abb89'
    :return: string with the hardware ID
    :rtype: str
    """
    _ci = cpuinfo.get_cpu_info()

    cpu_inf = (
        "%s%s%s%s" % (_ci["model"], _ci["family"], "".join(_ci["flags"]), _ci["arch"])
    ).replace(" ", "")

    # print(cpu_inf)
    d = hashlib.sha512()
    d.update(cpu_inf.encode("utf-8", errors="ignore"))

    return d.hexdigest()


# get_hardware_id()
# print(cpuinfo.get_cpu_info())
print(get_hardware_id())
