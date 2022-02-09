#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
from OnlineShop.settings.dev import CONFIG_PATH


class MyDict(dict):
    # 支持用.获取属性值，如d.a=1
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        if not self.get(key):
            raise ValueError(f"{str(key)} is not exist")
        self[key] = value


class InitConfigFile:

    def __init__(self):
        self.result = self.read_config(CONFIG_PATH)

    @staticmethod
    def read_config(file_name):
        result = {}
        config = configparser.ConfigParser()
        config.read(file_name, encoding="utf-8")
        for x in config.sections():
            items = {}
            for y in config.items(x):
                items[y[0]] = y[1]
            result[x] = items
        return result

    def __getattr__(self, item):
        return self.result[item]


global_config = InitConfigFile()