import unicodedata
import sys


try:
    from setuptools._vendor import six
except ImportError:
    # fallback to naturally-installed version; allows system packagers to
    #  omit vendored packages.
    import six

# HFS Plus uses decomposed UTF-8
def decompose(path):
    if isinstance(path, six.text_type):
        return unicodedata.normalize('NFD', path)
    try:
        path = path.decode('utf-8')
        path = unicodedata.normalize('NFD', path)
        path = path.encode('utf-8')
    except UnicodeError:
        pass  # Not UTF-8
    return path


def filesys_decode(path):
    """
    Ensure that the given path is decoded,
    NONE when no expected encoding works
    """

    fs_enc = sys.getfilesystemencoding()
    if isinstance(path, six.text_type):
        return path

    for enc in (fs_enc, "utf-8"):
        try:
            return path.decode(enc)
        except UnicodeDecodeError:
            continue


def try_encode(string, enc):
    "turn unicode encoding into a functional routine"
    try:
        return string.encode(enc)
    except UnicodeEncodeError:
        return None
