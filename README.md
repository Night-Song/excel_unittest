# excel_unittest
一个用excel+requests+uniitest+HTMLTestRunner的接口测试小程序。

## 用法：    
1.在Excel文件中维护接口测试数据，如接口地址、接口参数、判断方法、预期结果等。    
2.“python excel_unittest.py”运行程序，会调用uniitest测试、生成HTMLTestRunner报告。

## 接口参数存放格式说明：
可存放2种格式:    

1.url参数字符串：a=1&b=2&c=3&...&n=xxx    

2.多行+空格存放：    
a 111    
b 222   
c 333   
n xxx    

## 备注：
该程序纯属练手（虽然能用来测试接口，但还是发现不少问题），仍需后续调整，有兴趣的看看就好。
