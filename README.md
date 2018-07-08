## 更新：
2018年07月08日，重构脚本程序，上传excel_unittes2.py文件。  
变更说明：  
1）程序改为使用unittest+openpyxl+requests+ddt+HTMLTestRunner，从而去掉exec()函数，减少调试的麻烦。  
2）增加run_script()断言函数，增加断言的便利性。



-----
## 项目说明：
接口测试程序，使用python2.7编写。

## 具体说明：
主程序文件为excel_unittest.py。使用unittest+openpyxl+requests+exec函数+HTMLTestRunner编写，利用excel维护测试数据。

#### 运行方式：
命令行输入“python2 excel_unittest.py”运行，运行后会在同级目录生成名为HTMLTestRunner.Html的测试报告文件，可供参考。不过暂时没写发送邮件功能。

#### Excel中字段说明：
· testcase：测试case名称指定字段。  
· request_method：接口http请求方式指定字段，GET或POST。  
· url：接口URL指定字段。  
· url_params：接口参数指定字段。  
· check_point_type：断言函数指定字段。  
· node_path/script：json路径指定字段或自定义断言脚本存放字段。  
· expected_result：预期结果指定字段。  

#### 接口参数格式说明：  
· 若是GET接口-->将接口URL整体存入Excel文档中url字段，然后url_params字段空着，即可使用。  
· 若是POST接口-->将接口URL存入Excel文档中url字段，再将body存入url_params字段，即可使用。  
#### 断言说明：  
因为公司项目返回都是json，因此写的2个断言函数都是对json数据的断言，因此若接口返回html、xml，此脚本暂不支持，请自己写断言函数。  

#### 断言类型说明（check_point_type字段的值）：  
目前有2种断言方法: check_single_node()和run_script()。  
· check_single_node()：json数据的单节点，判断该节点的值是否等于expected_result的值。  
· run_script()：自己写脚本断言，脚本中可使用参数：resp_obj-->json解析后的数据；expected_result-->预期结果字段。  

-----
## 其他说明：
该程序为练手用，可以用来做测试接口，但仍需完善。
欢迎建议，不喜勿喷，谢谢。  


