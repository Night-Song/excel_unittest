# coding:utf-8
"""参数转换"""

from common_util import BaseCommonUtil
import re
import hashlib


def url_split(url):
    """[summary] 拆分url函数

    Args:
        url: [description] url，字符串类型

    Returns:
        [description] 返回拆分后的结果，url和params，list类型
        [type] list
        注意：若给的url没参数部分，则返回的长度仍是2，但params=None
    """
    # 传参类型检查
    BaseCommonUtil.check_params_type(locals(), url=str)
    result = url.strip().split("?", 1)
    if len(result) < 2:
        result.append(None)
    return result


def params_to_dict(url_params):
    """[summary] 参数转换，将字符串转为dict类型（注意，只管参数转换，不管判断有没有url）

    Args:
        url_params: [description] 需要解析的url参数，string类型

    Returns:
        [description] 返回url参数字典
        [type] dict
    """
    # 传参类型检查
    BaseCommonUtil.check_params_type(locals(), url_params=str)
    # 转换
    param_dict = {}
    if "?" in url_params:
        url_params = url_params.strip().split("?", 1)[1]
    if url_params.startswith("&"):
        url_params = url_params[1:]
    for it in url_params.split("&"):
        temp = it.split("=", 1)
        param_dict[temp[0]] = temp[1]
    return param_dict


def params_to_dict_from_charles(url_params):
    """
    将url参数从字符串转字典
    """
    # 传参类型检查
    BaseCommonUtil.check_params_type(locals(), url_params=str)
    # 转换
    param_dict = {}
    for line in url_params.strip().split("\n"):
        temp = re.split(r"\s+", line.strip(), 1)
        if len(temp) < 2:
            param_dict[temp[0]] = ""
        else:
            param_dict[temp[0]] = temp[1]
    return param_dict


def dict_sort_print_to_list(params):
    """排序后打印url参数（转成list后打印）"""
    BaseCommonUtil.check_params_type(locals(), params=dict)
    url_paramss = sorted(params.items(), lambda x, y: cmp(x, y))
    for item in url_paramss:
        if item:
            k, v = item
            print k, "\t" * 3, v
    return


def url_split_all(url):
    """将url分割为 protocol/host/port/path"""
    BaseCommonUtil.check_params_type(locals(), url=basestring)

    # 参数准备
    url = url.strip()
    url_info = {}

    # 匹配协议 = > 获取Http://最后的斜杠位置，然后截取String
    fir_split = url.index("//")
    prot = url[0: fir_split - 1]
    url = url[fir_split + 2:]

    # 匹配域名 = > 从双斜杠后面开始继续匹配"/"到第1个斜杠截止
    host, path = url.split("/", 1)

    # 匹配域名和端口
    port = None
    if ":" in host:
        host, port = host.split(":")

    # 匹配路径和参数
    querys = None
    if "?" in path:
        path, querys = path.split("?")

    # 存储返回
    url_info["prot"] = prot
    url_info["host"] = host
    url_info["port"] = port
    url_info["path"] = path
    url_info["querys"] = querys
    return url_info


def encrypt_md5(orig_str):
    """
    字符串MD5加密
    """
    BaseCommonUtil.check_params_type(locals(), orig_str=str)
    mm = hashlib.md5()
    mm.update(orig_str)
    return mm.hexdigest()


if __name__ == '__main__':
    pass
