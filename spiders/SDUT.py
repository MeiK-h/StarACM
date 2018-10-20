import json

import requests


def result_to_string(result):
    return {
        0: 'Waiting',
        1: 'Accepted',
        2: 'Time Limit Exceeded',
        3: 'Memory Limit Exceeded',
        4: 'Wrong Answer',
        5: 'Runtime Error',
        6: 'Output Limit Exceeded',
        7: 'Compile Error',
        8: 'Presentation Error',
        11: 'System Error',
        12: 'Judging'
    }[result]


def language_fix(language):
    language_dict = {
        "gcc": "C",
        "g++": "C++",
        "java": "Java",
        "python2": "Python",
        "python3": "Python",
        "c#": "C#",
        "ruby": "Ruby",
        "go": "Go",
        "pascal": "Pascal",
        "lua": "Lua",
        "haskell": "Haskell",
        "perl": "Perl",
    }
    if language_dict.get(language):
        return language_dict[language]
    return 'Other'


def main(username, last=0):
    return_data = []
    cnt = 0
    while cnt < 10:  # 最多尝试 10 次，防止因各种因素导致无限请求
        url = 'https://acm.sdut.edu.cn/onlinejudge2/index.php/API/Solution?user_name={}&limit=1000&order=ASC&runid={}&cmp=g'.format(
            username, last)
        cnt += 1
        req = requests.get(url)
        data = json.loads(req.text)
        if not data:
            break
        for i in data:
            return_data.append({
                'runid': i['runid'],
                'pid': i['pid'],
                'source': 'SDUT',
                'result': result_to_string(i['result']),
                'time': i.get('time'),
                'memory': i.get('memory'),
                'submission_time': i.get('submission_time'),
                'language': language_fix(i.get('language')),
                'uid': i.get('uid'),
                'code_length': i.get('code_length'),
            })
            last = i['runid']
    return return_data


if __name__ == '__main__':
    print(json.dumps(main('MeiK'), indent=4, ensure_ascii=False))
