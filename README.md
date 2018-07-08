## 更新：
2018年07月08日，重构脚本程序，上传excel_unittest2.py文件。
变更说明：    
1）框架改为使用unittest+openpyxl+requests+ddt+HTMLTestRunner，从而去掉exec()函数，减少调试的麻烦。
2）增加run_script()断言函数，增加断言的便利性。



-----
## 项目说明：
接口测试程序，使用python2编写。

## 具体说明：
主程序文件为excel_unittest.py。使用unittest+openpyxl+requests+exec函数+HTMLTestRunner编写，利用excel维护测试数据。

## 运行方式：
命令行输入“python2 excel_unittest.py”运行，运行后会在同级目录生成名为HTMLTestRunner.Html的测试报告文件，可供参考。不过暂时没写发送邮件。

## 补充说明：
1）接口参数格式说明：
· 若是GET接口-->将接口URL整体存入Excel文档中url字段，然后url_params字段空着，即可使用。
· 若是POST接口-->将接口URL存入Excel文档中url字段，再将body存入url_params字段，即可使用。
2）断言说明：
因为公司项目返回都是json，因此写的断言函数都对json数据的断言，因此若接口返回html、xml，此脚本暂不支持。
3）断言类型说明（check_point_type字段的值）：
目前有2种断言方法: check_single_node()和run_script()。
· check_single_node()：json数据的单节点，判断该节点的值是否等于expected_result的值。
· run_script()：自己写脚本断言，脚本中可使用参数：
        resp_obj-->json解析后的数据，python数据类型。
        expected_result-->预期结果、Excel中expected_result字段的值。

## 其他说明：
该程序为练手用，可以用来测试接口，但并不完善。因此欢迎建议，但不喜勿喷，谢谢。
