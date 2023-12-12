import re

from qianv_tool.module.logger import logger
from qianv_tool.config.exe_config  import ExecuteConfig as ButtonExt
from qianv_tool.module.base.decorator import cached_property, del_cached_property


def get_assets_from_file(file, regex):
    assets = set()
    with open(file, 'r', encoding='utf-8') as f:
        for row in f.readlines():
            result = regex.search(row)
            if result:
                assets.add(result.group(1))
    return assets


class PreservedAssets:
    @cached_property
    def ui(self):
        assets = set()
        assets |= get_assets_from_file(
            file='./module/ui/assets.py',
            regex=re.compile(r'^([A-Za-z][A-Za-z0-9_]+) = ')
        )
        assets |= get_assets_from_file(
            file='./module/ui/ui.py',
            regex=re.compile(r'\(([A-Z][A-Z0-9_]+),')
        )
        assets |= get_assets_from_file(
            file='./module/handler/info_handler.py',
            regex=re.compile(r'\(([A-Z][A-Z0-9_]+),')
        )
        # MAIN_CHECK == MAIN_GOTO_CAMPAIGN
        assets.add('MAIN_GOTO_CAMPAIGN')
        return assets


_preserved_assets = PreservedAssets()


class Resource:
    # Class property, record all button and templates
    instances = {}
    # Instance property, record cached properties of instance
    cached = []

    def resource_add(self, key):
        Resource.instances[key] = self

    def resource_release(self):
        for cache in self.cached:
            del_cached_property(self, cache)

    @classmethod
    def is_loaded(cls, obj):
        if hasattr(obj, '_image') and obj._image is None:
            return False
        elif hasattr(obj, 'image') and obj.image is None:
            return False
        return True

    @classmethod
    def resource_show(cls):
        logger.hr('Show resource')
        for key, obj in cls.instances.items():
            if cls.is_loaded(obj):
                continue
            logger.info(f'{obj}: {key}')

    @staticmethod
    def parse_property(data, s=None):
        """
        Parse properties of Button or Template object input.
        Such as `area`, `color` and `button`.

        Args:
            data: Dict or str
            s (str): Load from given a server or load from global attribute `server.server`
        """
        if s is None:
            s = ButtonExt.ASSETS_GAME_FOLDER
        if isinstance(data, dict):
            return data[s]
        else:
            return data

