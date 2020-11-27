# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, HttpResponse
from aweme.mongo import mydb
# from .models import StudentModel
from django.views.generic import View
import json, traceback


# class Student(View):
#     def get(self, request):
#         StudentModel.objects.create(name='水痕', age=20)
#         return HttpResponse('hello word')
sranks = ['PLAY', 'LIFE', 'FOOD', 'ROOM']

def return_poi_info(result, city_name, city_code, rank_code, is_poi):
    if city_name and rank_code:
        myquery = {"city_name": city_name}
        mydoc = mydb['provinces'].find(myquery, {"_id": 0})
        if mydoc.count() > 0:
            province_pinyin = mydoc[0]['province_pinyin']
            city_code = mydoc[0]['city_code']
            poi_query = {"city_code": city_code, "rank_code": rank_code}
            poi_doc = mydb['poi_{}'.format(province_pinyin)].find(poi_query, {"_id": 0})
            if poi_doc.count() > 0:
                if is_poi:
                    result['poi'] = poi_doc[0]
                else:
                    result['data'] = poi_doc[0]
            else:
                result['msg'] = '未找到该分类数据'
        else:
            result['msg'] = '未找到该城市'
    elif city_code and rank_code:
        myquery = {"city_code": city_code}
        mydoc = mydb['provinces'].find(myquery, {"_id": 0})
        if mydoc.count() > 0:
            province_pinyin = mydoc[0]['province_pinyin']
            poi_query = {"city_code": city_code, "rank_code": rank_code}
            poi_doc = mydb['poi_{}'.format(province_pinyin)].find(poi_query, {"_id": 0})
            if poi_doc.count() > 0:
                if is_poi:
                    result['poi'] = poi_doc[0]
                else:
                    result['data'] = poi_doc[0]
            else:
                result['msg'] = '未找到该分类数据'
        else:
            result['msg'] = '未找到该城市代码'
    else:
        result['code'] = -1
        result['msg'] = '查询失败'
    return result


class RankInfo(View):
    def get(self, request):
        result = {"code": 0, "data": None, "poi": None, "msg": "查询成功"}
        try:
            city_name = request.GET.get("city_name")
            city_code = request.GET.get("city_code")
            srank_code = request.GET.get("srank_code")
            if srank_code in sranks:
                if city_name and srank_code:
                    myquery = {"city_name": city_name}
                    mydoc = mydb['rank_info'].find(myquery, {"_id": 0})
                    if mydoc.count() > 0:
                        result['data'] = mydoc[0]
                        switch_options = mydoc[0]['switch_options']
                        if switch_options:
                            for s in switch_options:
                                if srank_code == s['rank_code']:
                                    result = return_poi_info(result, city_name, city_code, s['ranks'][0]['rank_code'], True)
                    else:
                        result['msg'] = '未找到该城市'
                elif city_code and srank_code:
                    myquery = {"city_code": city_code}
                    mydoc = mydb['rank_info'].find(myquery, {"_id": 0})
                    if mydoc.count() > 0:
                        result['data'] = mydoc[0]
                        switch_options = mydoc[0]['switch_options']
                        if switch_options:
                            for s in switch_options:
                                if srank_code == s['rank_code']:
                                    result = return_poi_info(result, city_name, city_code, s['ranks'][0]['rank_code'], True)
                    else:
                        result['msg'] = '未找到该城市代码'
                else:
                    result['code'] = -1
                    result['msg'] = '查询失败'
            else:
                result['msg'] = '无效的分类代码'
        except:
            print(traceback.format_exc())
            # write_log(3, format(traceback.format_exc()))
            result['code'] = -1
            result['msg'] = '查询异常'
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")

class PoiList(View):
    def get(self, request):
        result = {"code": 0, "data": None, "msg": "查询成功"}
        try:
            city_name = request.GET.get("city_name")
            city_code = request.GET.get("city_code")
            rank_code = request.GET.get("rank_code")
            result = return_poi_info(result, city_name, city_code, rank_code, False)
        except:
            print(traceback.format_exc())
            # write_log(3, format(traceback.format_exc()))
            result['code'] = -1
            result['msg'] = '查询异常'
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")

def save_recomm_info(poi_doc, city_code):
    recomms = []
    for poi in poi_doc:
        recomms += poi['rank_poi_list']
    recomm_list = sorted(recomms, key=lambda i: i['rank_score'], reverse=True)[:30]
    recomm_dict = {
        "_id": "RECOMM_{}".format(city_code),
        "city_code": "{}".format(city_code),
        "recomm_list": recomm_list,
    }
    mydb["recomm"].save(recomm_dict)
    return recomm_list

class ReComm(View):
    def get(self, request):
        result = {"code": 0, "data": None, "msg": "查询成功"}
        try:
            city_name = request.GET.get("city_name")
            city_code = request.GET.get("city_code")
            if city_name:
                myquery = {"city_name": city_name}
                mydoc = mydb['provinces'].find(myquery, {"_id": 0})
                if mydoc.count() > 0:
                    city_code = mydoc[0]['city_code']
                    recomm_query = {"city_code": city_code}
                    recomm_doc = mydb['recomm'].find(recomm_query, {"_id": 0})
                    if recomm_doc.count() > 0:
                        result['data'] = recomm_doc[0]['recomm_list']
                    else:
                        province_pinyin = mydoc[0]['province_pinyin']
                        poi_query = {"city_code": city_code}
                        poi_doc = mydb['poi_{}'.format(province_pinyin)].find(poi_query, {"_id": 0})
                        if poi_doc.count() > 0:
                            result['data'] = save_recomm_info(poi_doc, city_code)
                        else:
                            result['msg'] = '未找到该城市代码'
                else:
                    result['msg'] = '未找到该城市'
            elif city_code:
                myquery = {"city_code": city_code}
                mydoc = mydb['provinces'].find(myquery, {"_id": 0})
                if mydoc.count() > 0:
                    recomm_query = {"city_code": city_code}
                    recomm_doc = mydb['recomm'].find(recomm_query, {"_id": 0})
                    if recomm_doc.count() > 0:
                        result['data'] = recomm_doc[0]['recomm_list']
                    else:
                        province_pinyin = mydoc[0]['province_pinyin']
                        poi_query = {"city_code": city_code}
                        poi_doc = mydb['poi_{}'.format(province_pinyin)].find(poi_query, {"_id": 0})
                        if poi_doc.count() > 0:
                            result['data'] = save_recomm_info(poi_doc, city_code)
                        else:
                            result['msg'] = '未找到该城市代码'
                else:
                    result['msg'] = '未找到该城市代码'
            else:
                result['code'] = -1
                result['msg'] = '查询失败'
        except:
            print(traceback.format_exc())
            # write_log(3, format(traceback.format_exc()))
            result['code'] = -1
            result['msg'] = '查询异常'
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")