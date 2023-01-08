from django.db import models
from typing import List


class CURDManager:
    """CURD通用管理器"""

    def __int__(self):
        self._models = list()

    def register(self, model):
        self._models.append(model)
        return self

    def register_batch(self, model_list):
        [self.register(model) for model in model_list]


curd_manager = CURDManager()
curd_manager.register_batch([])
