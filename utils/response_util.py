# coding:utf-8
"""
设计一个接口处理response的工具类
"""

import json


def json_decrypt(resp_text):
    try:
        resp_json_obj = json.loads(resp_text)
        return resp_json_obj
    except ValueError:
        error_text = "JSON解析错误，疑似非Json格式，请排查：response=%s" % (resp_text)
        raise JsonDecryptException(error_text)


def pretty_format(resp):
    """
    json格式化函数

    1.如果是str或unicode，则先尝试json解析，然后：
        1.1 若能解析则进行json格式化再返回，
        1.2 若不能解析则直接返回；
    2.如果是dict和list，则直接进行json格式化再返回；
    3.若是数字，则直接返回；
    其他类型均报错
    """
    if isinstance(resp, basestring):
        try:
            return json.dumps(json.loads(resp), ensure_ascii=False, indent=4)
        except Exception:
            return resp
    elif isinstance(resp, (dict, list)):
        return json.dumps(resp, ensure_ascii=False, indent=4)
    elif isinstance(resp, (int, float, long)):
        return str(resp)
    else:
        print "参数类型有误：%s" % (type(resp))
        return    # 不写返回值，等于 return None


def get_json_node(resp_json_obj, node_path):
    """工具方法：按json节点逐层取值。如果节点不存在，则先提示，然后返回None。"""
    node_path_list = node_path.split(".")
    if len(node_path.split(".")) < 2:
        print "json节点输入有误！获取不到该节点"
        return None
    del node_path_list[0]  # 删除第1个“$”符号
    try:
        for i in node_path_list:
            resp_json_obj = resp_json_obj[i]
        return resp_json_obj
    except KeyError as e:
        error_text = "Json节点输入有误！%s节点不存在，请检查输入" % (e.message)
        raise JsonNodeNonExistentException(error_text)


class JsonDecryptException(Exception):
    """自定义异常，json解析异常时使用"""

    pass


class JsonNodeNonExistentException(Exception):
    """自定义异常，Json节点不存在异常"""

    pass


if __name__ == '__main__':
    resp_dict = {"returncode": 2049005, "message": "登录已过期，请重新登录"}
    resp_json = pretty_format(resp_dict)
    print resp_json
