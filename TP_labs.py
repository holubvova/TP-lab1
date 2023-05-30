import logging

import requests

from .DATA import ALL_FIELDS
import requests as r
import json
from requests.structures import CaseInsensitiveDict
import datetime

_DIGITS_ = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
query = ''
lst_query = []


def inputStr(query: str):
    tmp = query.replace('(', ' ( ')
    tmp = tmp.replace(')', ' ) ')
    lstQuery = tmp.split()
    print(lst_query)
    return lst_query


class Elastic4:

    # type : 0 - match_phrase, ( 1- range, contine in future )

    def __init__(self):
        self.responseApi = None
        self.URL = b'http://10.10.1.94:9200/_search?track_total_hits=true&rest_total_hits_as_int=true'
        self.result = ''
        self.timeout = False
        self.countAggs = 2
        self.aggs = {}
        self.noChangeParam = '''"size": 0,"stored_fields": ["*"],"script_fields": {},"docvalue_fields":[{"field": "@timestamp","format": "date_time"},{"field": "submission_timestamp","format": "date_time"}],"_source": {"excludes": []},'''
        self.must = {}
        self.filter = []
        self.range = {}
        self.filter.append({"match_all": {}})
        self.timestamp = {}
        self.query = {"bool":
                          {"must": [],
                           "filter": [],
                           "should": [],
                           "must_not": []}
                      }
        self.lst_query = []
        self.finalJsonQuery = []
        self.firstList = []
        self.flagNot = False
        self.results = {}
        self.filterItems = []
        self.dictResultParse = {}
        self.aggsDict = {}
        self.resultForLastDay = {}

    def addItemFilds(self, fields: str, value: str, type=0):
        tmp = self.add_match_phrase(fields, value)
        self.filter_items.append(tmp)

    def addAggss(self, field):

        param = {"field": field, "order": {"_count": "desc"}, "size": 50000}
        body_aggs = {"terms": param}
        if not bool(self.aggs):
            self.aggs = {str(self.count_aggs): body_aggs}
        else:
            self.recurse_add(self.aggs, {str(self.count_aggs): body_aggs})
        self.aggs_dict[f'{self.count_aggs}'] = field
        self.count_aggs = self.count_aggs + 1

    def adAggs(self, *args):
        for aggs_field in args:
            self.add_aggss(aggs_field)
        print(self.aggs)

    def recurseAdd(self, arggs, param_add):
    '''
    Проходимо  рекурсивно по списку аргуменів та рахуємо їх кількість
    '''
    
        list_keys = list(arggs.keys())
        if len(list_keys) == 1:
            rest = arggs[list_keys[0]]
            rest_2 = list(rest.keys())
            if rest_2[0] == "terms":
                if len(rest_2) == 2:
                    self.recurse_add(rest[rest_2[1]], param_add)
                else:
                    rest["aggs"] = param_add

    def recurseAddFilter(self , arrgs , param_add: dict):
    '''
    Запам'ятовуємо у фільтр аргументи 
    '''
    
        tmp = arrgs["bool"]["should"]
        if len(tmp) == 1:
            tmp.append(param_add)
        elif len(tmp) == 2:
            self.recurse_add_filter(tmp["bool"]["should"], param_add)

    def fiterAdd(self, fields: str, value: str):  # ??????????????????????

        tmp = self.item_bool(self.add_match_phrase(fields, value))
        if self.filter[0] == {"match_all": {}}:
            self.filter[0] = tmp
        else:
            pass
            # self.recurse_add_filter(self.filter[0], tmp)

    def addMatchPhrase(self, fields: str, value: str):
        arguments = {"match_phrase": {fields: value}}
        return arguments

    # type-0 normal, 1- add as filter

    def addRange(self, fields: str, start_value, end_value, type=0):
        '''
        додаємо час в окремий аргумет для  подальшого додавання в JSON запит 
        '''
        arguments = {}
        if fields == 'submission_timestamp':
            arguments = {"submission_timestamp": {"gte": start_value, "lte": end_value}}
        range = {"range": arguments}
        if type == 1:
            self.filter_items.append(range)
            return
        return range

    