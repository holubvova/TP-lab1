import logging

import requests

from .DATA import ALL_FIELDS
import requests as r
import json
from requests.structures import CaseInsensitiveDict
import datetime

DIGITS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
query = ''
lst_query = []


def input_str(query: str):
    tmp = query.replace('(', ' ( ')
    tmp = tmp.replace(')', ' ) ')
    lst_query = tmp.split()
    print(lst_query)
    return lst_query


class Elastic4:

    # type : 0 - match_phrase, ( 1- range, contine in future )

    def __init__(self):
        self.response_api = None
        self.URL = b'http://10.10.1.94:9200/_search?track_total_hits=true&rest_total_hits_as_int=true'
        self.result = ''
        self.timeout = False
        self.count_aggs = 2
        self.aggs = {}
        self.no_change_param = '''"size": 0,"stored_fields": ["*"],"script_fields": {},"docvalue_fields":[{"field": "@timestamp","format": "date_time"},{"field": "submission_timestamp","format": "date_time"}],"_source": {"excludes": []},'''
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
        self.final_json_query = []
        self.first_list = []
        self.flag_not = False
        self.results = {}
        self.filter_items = []
        self.dict_result_parse = {}
        self.aggs_dict = {}
        self.result_for_last_day = {}

    def add_item_filds(self, fields: str, value: str, type=0):
        tmp = self.add_match_phrase(fields, value)
        self.filter_items.append(tmp)

    def add_aggss(self, field):

        param = {"field": field, "order": {"_count": "desc"}, "size": 50000}
        body_aggs = {"terms": param}
        if not bool(self.aggs):
            self.aggs = {str(self.count_aggs): body_aggs}
        else:
            self.recurse_add(self.aggs, {str(self.count_aggs): body_aggs})
        self.aggs_dict[f'{self.count_aggs}'] = field
        self.count_aggs = self.count_aggs + 1

    def add_aggs(self, *args):
        for aggs_field in args:
            self.add_aggss(aggs_field)
        print(self.aggs)

    def recurse_add(self, arggs, param_add):
        list_keys = list(arggs.keys())
        if len(list_keys) == 1:
            rest = arggs[list_keys[0]]
            rest_2 = list(rest.keys())
            if rest_2[0] == "terms":
                if len(rest_2) == 2:
                    self.recurse_add(rest[rest_2[1]], param_add)
                else:
                    rest["aggs"] = param_add

    def recurse_add_filter(self, arrgs, param_add: dict):
        tmp = arrgs["bool"]["should"]
        if len(tmp) == 1:
            tmp.append(param_add)
        elif len(tmp) == 2:
            self.recurse_add_filter(tmp["bool"]["should"], param_add)

    def fiter_add(self, fields: str, value: str):  # ??????????????????????

        tmp = self.item_bool(self.add_match_phrase(fields, value))
        if self.filter[0] == {"match_all": {}}:
            self.filter[0] = tmp
        else:
            pass
            # self.recurse_add_filter(self.filter[0], tmp)

    def add_match_phrase(self, fields: str, value: str):
        arguments = {"match_phrase": {fields: value}}
        return arguments

    # type-0 normal, 1- add as filter

    def add_range(self, fields: str, start_value, end_value, type=0):
        arguments = {}
        if fields == 'submission_timestamp':
            arguments = {"submission_timestamp": {"gte": start_value, "lte": end_value}}
        range = {"range": arguments}
        if type == 1:
            self.filter_items.append(range)
            return
        return range

    def item_bool(self, arguments: dict):  # if Match_phrase flag = 0, else flag = 1

        self.item = {"should": [arguments], "minimum_should_match": 1}
        return {"bool": self.item}

    def filter_query(self, query):
        tmp = query.replace('(', ' ( ')
        tmp = tmp.replace(')', ' ) ')
        self.lst_query = tmp.split()
        self.start()
        self.second_look()
        print(self.filter)

    def start(self):
        i = 0
        while i < len(self.lst_query):
            if self.lst_query[i] in ALL_FIELDS:
                fields = self.lst_query[i]
                separator = self.lst_query[i + 1]
                data = self.lst_query[i + 2]
                if separator == ":":
                    self.item = self.create_item(fields, data)
                elif separator == "is":
                    pass
                else:
                    print("Error")
                    break
                self.first_list.append(self.item)
                i = i + 3
            else:
                self.first_list.append(self.lst_query[i])
                i = i + 1

    def second_look(self):
        i = 0
        length_ = len(self.first_list)
        if length_ != 0:
            self.steck_item = []
            self.steck_operand = []
            self.second_list = []
            while i < length_:
                if self.first_list[i] == 'not':
                    if i + 1 < length_:
                        if self.first_list[i + 1] != '(':
                            self.second_list.append(self.not_operand(self.first_list[i + 1]))
                            i = i + 1
                        else:
                            self.second_list.append(self.first_list[i])
                else:
                    self.second_list.append(self.first_list[i])

                i = i + 1
            i = 0
            length_ = len(self.second_list)
            while i < length_:
                tmp = self.second_list[i]
                if tmp == 'not' or tmp == 'and' or tmp == 'or' or tmp == '(':
                    self.steck_operand.insert(0, tmp)
                elif tmp == ')':
                    self.add()
                    if self.steck_operand[0] == 'not':
                        self.steck_operand.pop(0)
                        self.steck_item.insert(0, self.not_operand(self.steck_item.pop(0)))
                else:
                    self.steck_item.insert(0, tmp)
                i = i + 1

            if len(self.steck_operand) != 0 and len(self.steck_item) != 0:
                self.add()
            else:
                self.filter[0] = self.steck_item.pop(0)
                self.result = self.filter
                print(self.filter[0])

    def add(self):
        result = {}
        item2 = self.steck_item.pop(0)
        operand = self.steck_operand.pop(0)
        item1 = self.steck_item.pop(0)
        while 1:
            item2 = self.operand_work(item1, item2, operand)
            if not self.steck_item and not self.steck_operand:
                break
            operand = self.steck_operand.pop(0)
            if operand == '(':
                break
            else:
                item1 = self.steck_item.pop(0)

        result = item2
        print(result)
        self.result = item2
        self.steck_item.insert(0, result)

    def operand_work(self, item1, item2, operand):
        result = {}
        if operand == 'or':
            result = {"bool": {"should": [item1, item2], "minimum_should_match": 1}}
        elif operand == 'and':
            result = {"bool": {"filter": [item1, item2]}}
        return result

    def not_operand(self, item):
        result = {"bool": {"must_not": item}}
        return result

    def create_item(self, fields: str, data):

        match_phrase = self.create_field(fields, data)
        should = {"should": [match_phrase], "minimum_should_match": 1}
        item = {"bool": should}
        return item

    def create_field(self, fields: str, data):
        if data[0] == '"' and data[-1] == '"':
            match_phrase = {"match_phrase": {fields: data}}
        else:
            if data[0] == '*' or data[-1] == '*':
                new_data = self.new_data_m(data)
                match_phrase = {"query_string": {"fields": [fields], "query": new_data}}
            else:
                match_phrase = {"match": {fields: data}}
        return match_phrase

    def new_data_m(self, data):
        tmp = list(data)
        result = ''
        for i in tmp:
            if i in DIGITS:
                result = result + '\\' + i
            else:
                result = result + i
        return result

    def date_range(self, interval, lte=None, gte=None,type=None):

        # type 1 : when GTE time  start form 00:00:00 .

        gte_tmp = datetime.datetime.utcnow()
        curently_time = datetime.datetime.utcnow()

        if lte != None:
            curently_time = self.str_to_datetime(lte)
        else:
            lte = self.corect_date_range(curently_time.year, curently_time.month, curently_time.day, curently_time.hour,
                                         curently_time.minute)
        range_delta = interval[-1]
        count_delta = int(interval[:-1])

        if type == 1:
            self.timestamp = {"@timestamp": {
                "gte": self.corect_date_range(curently_time.year, curently_time.month, curently_time.day, 0,0),
                "lte": lte,
                "format": "strict_date_optional_time"
            }}
            return

        if range_delta == 'm':
            gte_tmp = curently_time - datetime.timedelta(minutes=count_delta)
        elif range_delta == 'h':
            gte_tmp = curently_time - datetime.timedelta(hours=count_delta)
        elif range_delta == 'd':
            gte_tmp = curently_time - datetime.timedelta(days=count_delta)
        self.timestamp = {"@timestamp": {
            "gte": self.corect_date_range(gte_tmp.year, gte_tmp.month, gte_tmp.day, gte_tmp.hour,
                                          gte_tmp.minute),
            "lte": lte,
            "format": "strict_date_optional_time"
        }}
        print(self.timestamp)



    def str_to_datetime(self, time: str):
        day = int(time[8:10])
        month = int(time[5:7])
        year = int(time[:4])
        hour = int(time[11:13])
        minute = int(time[14:16])
        temporary_time = datetime.datetime(day=day, month=month, year=year, hour=hour, minute=minute)
        return temporary_time

    def corect_date_range(self, year, month, day, hour, minute):
        if day < 10:
            day = f'0{day}'
        if month < 10:
            month = f'0{month}'
        if hour < 10:
            hour = f'0{hour}'
        if minute < 10:
            minute = f'0{minute}'
        result = f'{year}-{month}-{day}T{hour}:{minute}:00.000Z'
        return result

    def send_to_Api(self):
        self.make_query()
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        try:
            resp = r.get(
                b'http://10.10.1.94:9200/_search?track_total_hits=true&rest_total_hits_as_int=true',

                data=self.Query,
                headers=headers,
            )
            print(resp.status_code)
            self.result_json = resp.json()
            self.resp = resp
            self.timeout = False
        except requests.ConnectionError as e:
            print(e)
            print("TIME out error")
            self.timeout = True

    def make_query(self):

        tmp = self.query["bool"]['filter']
        buffer = self.make_filter()
        for i in buffer:
            tmp.append(i)
        print(tmp)
        aggs = f'"aggs": {self.aggs}'
        query = f'"query" : {self.query}'
        tmp_str_query = '{' + f'{aggs},{self.no_change_param}{query}' + '}'

        JSON = tmp_str_query.replace("'", '"')
        JSON = JSON.replace('""', '"')
        print(JSON)
        self.Query = JSON

    def make_filter(self):
        result = []
        if type(self.result) == dict:
            result.append(self.result)
        elif type(self.result) == list:
            result.append(self.result[0])
        else:
            result.append(self.filter)

        if self.filter_items != []:
            for x in self.filter_items:
                result.append(x)

        result.append({"range": self.timestamp})

        return result

    def response(self):
        if not self.timeout:
            if self.resp.status_code == 200:
                self.response_api = json.loads(self.resp.content)
                self.parse_response_api()
                return self.resp.status_code
            else:
                print(f'{self.resp.status_code}, \n  {self.resp.json()}')
                return self.resp.status_code

    def parse_response_api(self):
        print(self.response_api)
        response = self.response_api
        if "hits" in response:
            tmp = response["hits"]
            if tmp["total"] == 0:
                self.dict_result_parse["total"] = 0
            elif "aggregations" in response:
                tmp = response["aggregations"]
                for k, v in self.aggs_dict.items():
                    self.dict_result_parse[v] = None
                self.parse(tmp)
                tmp = response["hits"]
                self.dict_result_parse["total"] = tmp["total"]
            else:
                tmp = response["hits"]
                self.dict_result_parse["total"] = tmp["total"]

    def parse(self, aggregations):
        end = self.count_aggs
        list_keys = self.aggs_dict.keys()
        tmp = aggregations.copy()
        for i in list_keys:
            tmp = tmp[i]
            tmp = tmp['buckets']
            if tmp:
                if len(tmp) == 1:
                    tmp = tmp[0]
                if type(tmp) == dict:
                    dict_items = {}
                    dict_items[tmp['key']] = tmp['doc_count']
                    self.dict_result_parse[f'{self.aggs_dict[i]}'] = dict_items
                elif 'key' not in tmp:
                    dict_items = {}
                    for j in tmp:
                        dict_items[j['key']] = j['doc_count']
                    self.dict_result_parse[f'{self.aggs_dict[i]}'] = dict_items
                    tmp = tmp[0]
                else:
                    self.dict_result_parse[f'{self.aggs_dict[i]}'] = tmp['key']


#  recipient :  1 or  ( recipient : "2"   or recipient : "3" ) or recipient : "4" '
class check_conditions:
    flag_is = False
    error = ''
    i = 0
    last_value = 0
    count_backets = 0
    check_list = []

    def __init__(self, query):
        tmp = query.replace('(', ' ( ')
        tmp = tmp.replace(')', ' ) ')
        self.check_list = tmp.split()
        self.lenght = len(self.check_list)

    def checkin(self):

        for x in self.check_list:
            if x == '(':
                self.count_backets = self.count_backets + 1
            elif x == ')':
                self.count_backets = self.count_backets - 1
            else:
                continue

        if self.count_backets != 0:
            error = ' Condition is not correct , not closed parentheses '
            return error
        tmp = self.check_list[-1]
        type_last_element = self.check_type_element(tmp)
        if type_last_element != 3 and type_last_element != 6:
            return ' Condition is not correct'

        tmp = self.check_list[0]
        type_last_element = self.check_type_element(tmp)
        if type_last_element != 5 and type_last_element != 1:
            return ' Condition is not correct'

        if self.lenght >= 3:
            for element in self.check_list:
                type_element = self.check_type_element(element)
                if self.last_value == 0:
                    self.last_value = type_element
                    continue
                elif type_element == self.last_value:
                    return 'Condition is not correct'
                elif type_element == 2 and self.last_value == 1:
                    self.last_value = type_element
                    continue
                elif type_element == 3 and self.last_value == 2 and self.flag_is is False:
                    self.last_value = type_element
                    continue
                elif type_element == 3 and (self.last_value == 4 or self.last_value == 2) and self.flag_is is True:
                    self.last_value = type_element
                    continue
                elif type_element == 4 and (self.last_value == 6 or self.last_value == 3):
                    # if self.flag_is is True:
                    #     self.flag_is = False
                    self.last_value = type_element
                    continue
                elif type_element == 1 and (self.last_value == 4 or self.last_value == 5):
                    self.last_value = type_element
                    continue
                elif type_element == 5 and self.last_value == 4:
                    if self.flag_is is True:
                        self.flag_is = False
                    self.last_value = type_element
                    continue
                elif type_element == 6 and self.last_value == 3:
                    self.last_value = type_element
                    continue

                else:
                    return ' Condition is not correct'
        else:
            return ' Condition is not correct'

        return "ok"

    def check_type_element(self, element):
        # 1 - fields, 2- :  ':' / 'is' , 3 - value, 4- or / and , 5 - '(' , 6 - ')' 7 - if use 'is'
        if element in ALL_FIELDS:
            return 1
        elif element == ':':
            return 2
        elif element == 'is':
            self.flag_is = True
            return 2
        elif element == 'and' or element == 'or':
            return 4
        elif element == '(':
            return 5
        elif element == ')':
            return 6
        else:
            return 3

    def check(self):
        result = self.checkin()
        return result


def main():
    obj = Elastic4()
    obj.add_aggs("receipt_error_state", "recipient_operator_tag")
    obj.filter_query('sender_esme :  995995*')
    # obj.add_item_filds("o_error", "0:0")
    obj.add_item_filds("is_receipt", "false")
    obj.date_range(interval='10m', gte='2022-11-29T11:50:00.000Z',
                   lte='2022-11-29T12:00:00.000Z')  # "2022-07-12T15:37:54.299Z"
    # obj.add_range("submission_timestamp", "now-2h", "now",type=1)
    obj.send_to_Api()
    obj.response()
    print(obj.dict_result_parse)

    last_obj = Elastic4()
    last_obj.add_aggs("receipt_error_state", "recipient_operator_tag")
    last_obj.filter_query('sender_esme :  995995*')
    last_obj.add_item_filds("is_receipt", "false")
    last_obj.date_range(interval='10m', gte='2022-11-28T11:50:00.000Z', lte='2022-11-28T12:00:00.000Z')
    last_obj.send_to_Api()
    last_obj.response()
    print(last_obj.dict_result_parse, obj.dict_result_parse)
    now_result = last_obj.dict_result_parse['recipient_operator_tag']
    last_result = obj.dict_result_parse['recipient_operator_tag']
    print(now_result)
    print(last_result)

    table = list(last_result.keys())
    for keys in now_result.keys():
        if keys not in table:
            table.append(keys)

    full_table = {}
    for operator in table:
        if operator in last_result and operator in now_result:
            full_table[operator] = {"last_value": last_result[operator], "now_value": now_result[operator]}
        elif operator in last_result and operator not in now_result:
            full_table[operator] = {"last_value": last_result[operator], "now_value": 0}
        elif operator not in last_result and operator in now_result:
            full_table[operator] = {"last_value": 0, "now_value": now_result[operator]}

    print(full_table)

    #persent = (((now - last) * 100) / last)
    message_text = ''
    persent = 0
    for keys in list(full_table.keys()):
        values = full_table[keys]
        now = values['now_value']
        last = values['last_value']
        persent = int(((now - last) * 100) / last)
        if persent >=20:
            message_text = message_text + f'We observe increase traffic on PERSENT from  GEOCELL to OPERATOR.\n'

if __name__ == '__main__':
    main()


