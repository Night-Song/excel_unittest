# excel_unittest
一个用excel+HTMLTestRunner测接口的小程序。

## 说明：
用requests+exec+unittest+HTMLTestRunner实现，仅做了数据分离。
从excel里读数据，用requests请求接口、用exec生成case代码，最后通过HTMLTestRunner生成报告。

## 用法：    
python运行excel_unittest.py”开始测试。</br>
在Excel文件中维护接口测试数据。</br>

## 接口参数存放格式说明：
可存放2种格式:    

1.url参数字符串：a=1&b=2&c=3&...&n=xxx </br>

2.多行+空格存放： </br>
aaa 111    
bbb 222   
ccc 333    

## 备注：
练手用，虽然拿来测试接口，但感觉不少问题。仅供看看思路。
