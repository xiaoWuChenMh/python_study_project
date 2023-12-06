#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

class DevidesInfo:

    def __init__(self):
       pass

    def get_info(self):
        devices = [
            {"name": "Devices00AL1"},
            {"name": "Devices00AL2"},
            {"name": "Devices00AL3"},
            {"name": "Devices00AL6"},
            {"name": "Devices00AL7"},
            {"name": "Devices00AL4"}
        ]
        return copy.deepcopy(devices)