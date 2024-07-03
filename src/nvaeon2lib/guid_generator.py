"""Provide a GUID generator class for Aeon Timeline 2.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2nv
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import uuid


class GuidGenerator:
    """Generator for non-random GUIDs to be used with Aeon Timeline 2."""

    def __init__(self, filePath):
        self._url = f'file:///{filePath}'

    def get_guid(self, fragment):
        """Return a version-3 GUID according to RFC 4122.
        
        Positional arguments:
            fragment: str -- fragment to be appended to the URL for individual GUID generation.
        """
        return str(uuid.uuid3(uuid.NAMESPACE_URL, f'{self._url}#{fragment}'))
