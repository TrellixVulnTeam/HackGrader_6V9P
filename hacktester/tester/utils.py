from urllib.parse import urlsplit
import tarfile


def get_base_url(uri):
    return "{0.scheme}://{0.netloc}".format(urlsplit(uri))


class ArchiveFileHandler:
    @staticmethod
    def extract_tar_gz(path_to_archive, path_to_extract):
        with tarfile.open(name=path_to_archive, mode="r:gz") as tar:
            tar.extractall(path=path_to_extract)

    @classmethod
    def extract(cls, archive_type, path_to_archive, path_to_extract="."):
        extract_method_name = "extract_{}".format(archive_type.value)
        extract_method = getattr(cls, extract_method_name, None)
        if extract_method and hasattr(extract_method, "__call__"):
            return extract_method(path_to_archive, path_to_extract)
