# coding:utf-8
"""http请求工具类"""
from common_util import BaseCommonUtil
import requests
import url_param_convert_util as upc_util


class RequestUtil(object):
    """docstring for RequestUtil"""

    def __init__(self, timeout=10, encoding="utf-8"):
        """构造函数"""
        self._timeout = timeout
        self._encoding = encoding
        self._headers = None
        self._redirects = False
        self._verify = True

    # ------------------------------ headers ------------------------------
    @property
    def headers(self):
        """设置header-bean get()方法"""
        return self._headers

    @headers.setter
    def headers(self, new_headers):
        """设置header-bean set()方法"""
        BaseCommonUtil.check_param_type(locals(), "new_headers", dict)
        self._headers = new_headers

    # ------------------------------ redirects ------------------------------
    @property
    def redirects(self):
        """设置redirects-bean get()方法"""
        return self._redirects

    @redirects.setter
    def redirects(self, new_redirects):
        """设置redirects-bean set()方法"""
        BaseCommonUtil.check_param_type(locals(), "new_redirects", basestring)
        self._redirects = new_redirects

    # ------------------------------ verify ------------------------------
    @property
    def verify(self):
        """设置verify-bean get()方法"""
        return self._verify

    @verify.setter
    def verify(self, new_verify):
        """设置verify-bean set()方法"""
        BaseCommonUtil.check_param_type(locals(), "new_verify", bool)
        self._verify = new_verify

    # ------------------------------ http method ------------------------------
    def get(self, url, url_params=None, modify_params=None):
        """[summary] http协议，接口测试工具类，get函数

        [description]
            兼容的类型：
            1.直接传url
            2.url + url_params
            3.url + charles_url_params： 从charles复制过来的key&value的参数字符串

        Args:
            url: [description] url，可以是带参数的url，也可以不带参数，string类型。
            url_params: [description] url参数，可以是dict，也可以是string。
            modify_params: [description] url参数中要修改的参数，dict类型。

        Returns:
            [description] 返回请求得到的request对象。
        """
        # 传参类型检查
        BaseCommonUtil.check_params_type(locals(), url=str, url_params=(str, dict), modify_params=dict)
        # 转换url和params
        url, url_params = self.convert_url_and_params(url, url_params)
        # 更新参数
        self.update_params(url_params, modify_params)
        # 请求接口
        try:
            resp = requests.get(url, params=url_params, headers=self._headers, timeout=self._timeout, allow_redirects=self._redirects, verify=self._verify)
        except requests.exceptions.ConnectTimeout as e:
            raise ConnectTimeoutException(e.message.url, e.message.reason[1])
            return
        # 设置显示内容编码
        resp.encoding = self._encoding
        # 异常判断
        self.check_status_code(resp)
        # 关闭连接、返回内容
        resp_text = resp.text
        resp.close()
        return resp_text

    def post(self, url, url_params, modify_params=None):
        """Content-Type = application/x-www-form-urlencoded"""
        # 传参类型检查
        BaseCommonUtil.check_params_type(locals(), url=str, url_params=(str, dict), modify_params=dict)
        # 转换url和params
        url, url_params = self.convert_url_and_params(url, url_params)
        # 更新参数
        self.update_params(url_params, modify_params)
        # 请求接口
        try:
            resp = requests.post(url, data=url_params, headers=self._headers, timeout=self._timeout, allow_redirects=self._redirects, verify=self._verify)
        except requests.exceptions.ConnectTimeout as e:
            raise ConnectTimeoutException(e.message.url, self._timeout)
            return
        # 设置显示内容编码
        resp.encoding = self._encoding
        # 异常判断
        self.check_status_code(resp)
        # 关闭连接、返回内容
        resp_text = resp.text
        resp.close()
        return resp_text

    def post_multipart_form_data(self, url, url_params=None, files=None):
        """Content-Type = multipart/form-data，注意：暂不提供modify_params"""
        # 传参类型检查
        BaseCommonUtil.check_params_type(locals(), url=str, url_params=(str, dict), files=dict)
        # 更新参数
        self.update_params(url_params)
        # 请求接口
        try:
            resp = requests.post(url, data=url_params, files=files, headers=self._headers, timeout=self._timeout, allow_redirects=self._redirects, verify=self._verify)
        except requests.exceptions.ConnectTimeout as e:
            raise ConnectTimeoutException(e.message.url, self._timeout)
            return
        # 设置显示内容编码
        resp.encoding = self._encoding
        # 异常判断
        self.check_status_code(resp)
        # 关闭连接、返回内容
        resp_text = resp.text
        resp.close()
        return resp_text

    def file_download(self, url, url_params, file_save_path):
        """从接口下载文件"""
        # jpg_url = 'http://img2.niutuku.com/1312/0804/0804-niutuku.com-27840.jpg'
        content = requests.get(url, data=url_params).content
        with open(file_save_path, 'wb') as fp:
            fp.write(content)

    # ------------------------------ assert ------------------------------
    def check_status_code(self, response):
        """判断接口请求是否正常：status_code是否等于200"""
        try:
            response.raise_for_status()
        except requests.RequestException:
            error_text = "接口:%s 请求异常！请排查：status_code=%s" % (response.url, response.status_code)
            raise requests.RequestException(error_text)

    # ------------------------------ util ------------------------------
    def convert_url_and_params(self, url, url_params):
        """url和params解析函数（参数类型转换）"""
        url = url.strip()
        # 若没url_params，但给的url字符串里带url参数字符串，则拆分url字符串
        if (url_params is None) and ("?" in url):
            return url, url_params
        # 若有url参数，则再判断是不是字符串类型，是则将其解析为dict（不是则跳过）
        if url_params and isinstance(url_params, str):
            # 处理 params_string 或 charles_params_string
            if "&" in url_params:
                url_params = upc_util.params_to_dict(url_params)
            if "\n" in url_params:
                url_params = upc_util.params_to_dict_from_charles(url_params)
        return url, url_params

    def update_params(self, url_params, modify_params=None):
        """更新参数"""
        if url_params:
            if modify_params:
                url_params.update(modify_params)


class ConnectTimeoutException(Exception):
    """自定义，接口请求超时异常"""

    def __init__(self, url, value):
        """初始化函数"""
        self._url = url
        self._value = value

    def __str__(self):
        """返回对象字符串表达式"""
        if isinstance(self._value, int):
            return (u"接口%s %ss超时，请重试……" % (self._url, self._value)).encode("utf-8")
        else:
            return self._value
