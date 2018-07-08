# coding:utf-8
"""接口测试程序

数据源：Excel
测试框架：unittest
测试报告：HTMLTestRunner
"""

import os
import HTMLTestRunner
import ddt
import unittest
from utils.request_util import RequestUtil
import utils.response_util as resp_util
from utils.ExcelUtil import ParseExcel
# import traceback
# import json
import logging
import jsonpath


# 初始化日志对象
logging.basicConfig(
    # 日志级别
    level=logging.INFO,
    # 日志格式
    # 时间、代码所在文件名、代码行号、日志级别名字、日志信息
    format='%(asctime)s %(filename)s [line:%(lineno)d]: %(levelname)s %(message)s',
    # 打印日志的时间
    datefmt='%a, %Y-%m-%d %H:%M:%S',
    # 日志文件存放的目录（目录必须存在）及日志文件名
    filename='./test_log.log',
    # 打开日志文件的方式
    filemode='w'
)


# 从Excel获取数据
excel_file = u'./unit_excel.xlsx'
pe = ParseExcel(excel_file)


@ddt.ddt
class ExcelUnitTest(unittest.TestCase):
    """存接口的excel文件"""

    @classmethod
    def setUpClass(cls):
        """suite的执行前方法：创建断言的值，创建工具类实例"""
        cls.PASS = "Pass"
        cls.FAIL = "Fail"
        cls.req_util = RequestUtil(5)
        # cls.req_util = RequestUtil(5, "utf-8", allow_redirects=False)

    def setUp(self):
        """每个testcase的执行前方法：pass"""
        pass

    def tearDown(self):
        """每个testcase的执行后方法：pass"""
        pass

    @classmethod
    def tearDownClass(cls):
        """suite的执行后方法：pass"""
        pass

    # --------------------------------------------------------------------------------
    def convert_params(self, row_value_list):
        """转换入參类型"""
        def convert(row_value):
            if isinstance(row_value, unicode):
                return row_value.encode("utf-8")
            if isinstance(row_value, long):
                return int(row_value)
        return map(convert, row_value_list)

    def http_request(self, request_method, url, url_params):
        """请求接口"""
        request_method_dict = {
            "GET": self.req_util.get(url, url_params),
            "POST": self.req_util.post(url, url_params),
        }
        try:
            return request_method_dict[request_method.upper()]
        except KeyError:
            error_text = "request_method输入类型有误！无此http请求方法。"
            raise TypeError(error_text)

    @ddt.data(*pe.get_data_from_sheet(0))
    def test_data_driven(self, row_data_list):
        """ddt测试函数"""
        row_data = self.convert_params(row_data_list)    # 行数据整备
        try:
            # 请求http协议接口 -> method／url／url_params
            resp = self.http_request(row_data[2], row_data[3], row_data[4])
            # json解析
            resp_json_obj = resp_util.json_decrypt(resp)
            # 断言结果 -> check_point_type／check_node_path／expected_result
            print(type(row_data[7]), row_data[7])
            self.check_resp(resp_json_obj, row_data[5], row_data[6], row_data[7])
        except Exception as e:
            raise e

    # --------------------------------------------------------------------------------
    def check_resp(self, resp_json_obj,
                   check_point_type, node_path_or_script, expected_result):
        """断言调度函数"""
        check_type_dict = {
            "check_single_node": self.check_single_node,
            "run_script": self.run_script,
        }
        try:
            return check_type_dict[check_point_type](
                resp_json_obj, node_path_or_script, expected_result,
            )
        except KeyError:
            error_text = "check_point_type输入类型有误！无此check方法"
            raise TypeError(error_text)

    def check_single_node(self, resp_json_obj, node_path, expected_result):
        """断言函数之一：检查json节点的值是不是等于预期结果"""
        json_node_value = jsonpath.jsonpath(resp_json_obj, node_path)
        if json_node_value is False:    # 如果返回False，则证明node_path错误
            raise ValueError(u"%s路径有误，取不到值" % node_path)
        if len(json_node_value) == 1:    # 因为jsonpath获取单节点为list，所以只能这么判断
            json_node_value = json_node_value[0]
        else:
            raise ValueError(u"%s节点非单节点", node_path)
        self.assertEqual(json_node_value, expected_result)  # 断言是否相等

    def run_script(self, resp_json_obj, script_content, expected_result):
        """代码断言函数"""
        exec(script_content,
             {
                 'resp_obj': resp_json_obj,
                 'expected_result': expected_result
             })
        # self.assertEqual(result, expected_result)


if __name__ == '__main__':
    # 无报告运行unittest，测试脚本用
    # unittest.main(verbosity=2)

    # 指定报告名称
    report_save_path = './HTMLTestRunner.html'
    # 指定运行的测试类
    test_cases = unittest.TestLoader().loadTestsFromTestCase(ExcelUnitTest)
    # 设定excel文件名
    excel_file_name = os.path.basename(excel_file)
    # 给定报告里的case名称
    testcase_cn_name_list = pe.get_cell_values_by_cell_index(0, 1)
    # 运行unittest并声称报告
    with open(report_save_path, 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(
            # verbosity=2,
            stream=fp,
            title='自动化测试报告',  # 配置报告信息
            description='详细测试用例结果',
            tester="RenYi",
            testclass_name=excel_file_name,
            testcass_list=testcase_cn_name_list
        )
        runner.run(test_cases)
