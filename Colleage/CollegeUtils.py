# -*- coding: utf-8 -*-

import urllib.request, urllib.error
import re

class CollegeUtils:
    def __init__(self):
        self.college_minban = set()
        with open("college_minban.txt", "r", encoding='utf-8') as f1:
            line = f1.read()
        line = line.split(',')
        self.college_minban = set(line)
        self.college_other = set()
        with open("college_other.txt", "r", encoding='utf-8') as f2:
            line = f2.read()
        line = line.split(',')
        self.college_other = set(line)

    def getCollege_nature(self, college):
        if college in self.college_minban:
            return "民办"
        if college in self.college_other:
            return ""
        college_nature = self.getCollege_nature_online(college)
        if college_nature.find("民办") >= 0 or college_nature == "error":
            self.college_minban.add(college)
            return "民办"
        self.college_other.add(college)
        return ""

    def getCollege_nature_online(self, college):
        sb = bytes(college, encoding="utf8")
        college = urllib.request.quote(sb)
        url = "https://baike.baidu.com/item/" + college
        try:
            file = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.reason)
            return "error"

        data = file.read()
        data = str(data, encoding="utf8")
        pattern = r"类.*?别</dt>.*?</dd>"

        college_nature = re.search(pattern, data, re.S)
        if college_nature is None:
            return "error";
        college_nature = college_nature.group()
        return college_nature

    def close(self):
        with open("college_minban.txt", "wb") as f1:
            line = ",".join(self.college_minban)
            f1.write(line.encode('utf8'))
            print("save college_minban.txt")
        with open("college_other.txt", "wb") as f2:
            line = ",".join(self.college_other)
            f2.write(line.encode('utf8'))
            print("save college_other.txt")

