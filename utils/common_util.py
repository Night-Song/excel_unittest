# coding:utf-8
u"""工具类的基础类"""


class BaseCommonUtil(object):
    """docstring for BaseCommonUtil"""

    @staticmethod
    def check_param_type(local_params, check_param_name, expected_param_type):
        """[summary] 验证传参类型是否正确的方法，静态方法

        Args:
            local_params: [description] 传入locals()
            check_param_name: [description] 传入参数名
            expected_param_type: [description] 传入预期的类型

        Raises:
            TypeError: [description] 返回“is_return”的布尔值
        """
        if not isinstance(local_params[check_param_name], expected_param_type):
            print "%s参数类型有误,请排查: input:%s, expect:%s" % (check_param_name, type(local_params[check_param_name]), expected_param_type)
            return True
        return False

    @staticmethod
    def check_params_type(local_params, **expected_param_types):
        """[summary] 遍历验证函数传参类型是否正确，静态方法

        Args:
            local_params: [description] 传入locals()
            **expected_params_type: [description] 按key1=type1...逐个传入参数预期类型

        Returns:
            [description] 返回“是否需要return”的布尔值
            bool
        """
        for key, expected_type in expected_param_types.items():
            # 传参中如果某个key对应的值是None，则跳过、判断下一个key：
            input_param_value = local_params[key]
            if input_param_value:
                # 如果不符合预期类型，则报错
                if not isinstance(local_params[key], expected_type):
                    # print "%s参数类型有误,请排查: input:%s, expect:%s" % (key, type(input_param_value), expected_type)
                    # return True
                    # error_text = (u"%s参数类型有误,请排查: input:%s, expect:%s" % (key, type(input_param_value), expected_type)).encode("utf-8")
                    error_text = "%s参数类型有误,请排查: input:%s, expect:%s" % (key, type(input_param_value), expected_type)
                    raise TypeError(error_text)
        return False
