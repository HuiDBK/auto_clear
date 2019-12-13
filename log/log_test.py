# -*- coding:utf-8 -*-
"""
日志测试模块
author: Mr Liu
version: 1.0
"""
import logging

# %(levelno)s：打印日志级别的数值
# %(levelname)s：打印日志级别的名称
# %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s：打印当前执行程序名
# %(funcName)s：打印日志的当前函数
# %(lineno)d：打印日志的当前行号
# %(asctime)s：打印日志的时间
# %(thread)d：打印线程ID
# %(threadName)s：打印线程名称
# %(process)d：打印进程ID
# %(message)s：打印日志信息

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt='%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Start print log")
logger.debug("Do something")
logger.warning("Something maybe fail.")
logger.info("Finish")

# python中时间日期格式化符号：
#
# % y
# 两位数的年份表示（00 - 99）
#
# % Y
# 四位数的年份表示（000 - 9999）
#
# % m
# 月份（01 - 12）
#
# % d
# 月内中的一天（0 - 31）
#
# % H
# 24
# 小时制小时数（0 - 23）
#
# % I
# 12
# 小时制小时数（01 - 12）
#
# % M
# 分钟数（00 = 59）
#
# % S
# 秒（00 - 59）
#
# % a
# 本地简化星期名称
#
# % A
# 本地完整星期名称
#
# % b
# 本地简化的月份名称
#
# % B
# 本地完整的月份名称
#
# % c
# 本地相应的日期表示和时间表示
#
# % j
# 年内的一天（001 - 366）
#
# % p
# 本地A.M.或P.M.的等价符
#
# % U
# 一年中的星期数（00 - 53）星期天为星期的开始
#
# % w
# 星期（0 - 6），星期天为星期的开始
#
# % W
# 一年中的星期数（00 - 53）星期一为星期的开始
#
# % x
# 本地相应的日期表示
#
# % X
# 本地相应的时间表示
#
# % Z
# 当前时区的名称
#
# % % % 号本身