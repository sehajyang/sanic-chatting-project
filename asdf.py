from collections import Counter
import re


def solution1(input_str):
    result = ""
    for i in range(len(input_str)):
        if int(input_str[i]) % 2 is 0 and int(input_str[i - 1]) % 2 is 0:
            result += '*'
        elif int(input_str[i]) % 2 is 1 and int(input_str[i - 1]) % 2 is 1:
            result += '-'

        result += input_str[i]
    return result


def solution2():
    input_str = "Line 394 : [21:44:07 Oct 12 Fri] @0x3924004E|JVM| Free Memory: Heap [ 2368340/ 6291456], Native[ 7299824/32505856]"
    rex = re.compile(r'((?:\d{2})(?:\:\d{2}){2}).*?\[\s(\d+).*?\[\s(\d+)', re.DOTALL)
    rlist = rex.search(input_str)
    rlist.group(0)
    print(rlist.group(1))


if __name__ == '__main__':
    assert solution1('4546793') == '454*67-9-3'
    solution2()
