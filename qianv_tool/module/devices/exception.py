

class ImageTruncated(Exception):
    pass

class RequestHumanTakeover(Exception):
    # Request human takeover
    # Alas is unable to handle such error, probably because of wrong settings.
    pass

class PackageNotInstalled(Exception):
    pass