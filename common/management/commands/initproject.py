#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-03-17 13:38
# @Author  : myloe
# @File    : initproject.py
import os
import shutil
from django.core.management.base import BaseCommand
from myloe_django.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Initialize Project'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--name', help='assign project name', type=str, required=True)
        parser.add_argument('-dir', '--dir', help='assign project path', type=str)

    def handle(self, *args, **options):
        current_project_name = BASE_DIR.name
        new_project_name = options.get('name')
        new_project_dir = options.get('dir') or BASE_DIR.parent.joinpath(new_project_name)

        # 清理文件夹
        shutil.copytree(BASE_DIR, new_project_dir)
        new_project_dir.joinpath(current_project_name).rename(new_project_dir.joinpath(new_project_name))

        # 修改文件里的内容
        for root, dirs, files in os.walk(new_project_dir):
            for _dir in dirs:
                if _dir in ['.git', '.idea']:
                    shutil.rmtree(os.path.join(root, _dir))
            for file in files:
                if file[-3:] == '.py':
                    abs_file = os.path.join(root, file)
                    self.new_file(abs_file, current_project_name, new_project_name)

    @staticmethod
    def new_file(file_path, old_str, new_str):
        """
            替换文件中的字符串
        file_path：文件路径
        old_str:待修改的字符串
        new_str：修改后的字符串
        """
        with open(file_path, "r") as f1:  # 以只读方式打开文件
            data = f1.read()  # 读取文件，读取为一个字符串
            str_replace = data.replace(old_str, new_str)  # 将字符串中的某个字符进行替换
            with open(file_path, "w") as f2:  # 重新打开文件，选择写入模式
                f2.write(str_replace)  # 将修改后的字符串重新写入文件
