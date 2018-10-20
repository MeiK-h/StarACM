import json

import requests
from bs4 import BeautifulSoup


def result_fix(result):
    result_dict = {
        "Accepted": "Accepted",
        "Wrong Answer": "Wrong Answer",
        "Presentation Error": "Presentation Error",
        "Compile Error": "Compile Error",
        "Time Limit Exceeded": "Time Limit Exceeded",
        "Memory Limit Exceeded": "Memory Limit Exceeded",
        "Output Limit Exceeded": "Output Limit Exceeded",
        "Runtime Error": "Runtime Error",
        "Compiling": "Judging",
        "Waiting": "Judging",
        "Running & Judging": "Judging"
    }
    if result_dict.get(result):
        return result_dict[result]
    return 'Other'


def language_fix(language):
    language_dict = {
        "GCC": "C",
        "G++": "C++",
        "Java": "Java",
        "C++": "C++",
        "C": "C",
        "Fortran": "Fortran",
    }
    if language_dict.get(language):
        return language_dict[language]
    return 'Other'


def main(username, bottom=0):
    return_data = []
    cnt = 0

    while cnt < 200:  # 每页 20 条，排行榜第一名现在不到 4000 条
        url = 'http://poj.org/status?user_id={}&bottom={}'.format(
            username, bottom)
        cnt += 1
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        tables = soup.find_all('table')
        trs = tables[-1].find_all('tr')
        for tr in trs[::-1][:-1]:  # 去掉头部并反转各行
            tds = tr.find_all('td')
            run_id = tds[0].string
            user_id = tds[1].string
            problem = tds[2].string
            result = tds[3].string
            if result == 'Accepted':  # POJ 只有 AC 的提交才会显示时间和内存
                memory = tds[4].string[:-1]
                time = tds[5].string[:-2]
            else:
                memory = 0
                time = 0
            language = language_fix(tds[6].string)
            code_length = tds[7].string[:-1]
            submit_time = tds[8].string
            return_data.append({
                'runid': run_id,
                'pid': problem,
                'source': 'POJ',
                'result': result,
                'time': time,
                'memory': memory,
                'submission_time': submit_time,
                'language': language,
                'username': user_id,
                'code_length': code_length,
            })
            bottom = run_id
        print(bottom)
        if len(trs) != 21:  # 如果某页数据不足 20 条，则说明已经读完
            break

    return return_data


if __name__ == '__main__':
    print(json.dumps(main('MeiK'), indent=4, ensure_ascii=False))
