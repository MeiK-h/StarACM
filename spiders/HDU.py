import json

import requests
from bs4 import BeautifulSoup


def result_fix(result):
    result_dict = {
        "Accepted": "Accepted",
        "Wrong Answer": "Wrong Answer",
        "Presentation Error": "Presentation Error",
        "Compilation Error": "Compile Error",
        "Time Limit Exceeded": "Time Limit Exceeded",
        "Memory Limit Exceeded": "Memory Limit Exceeded",
        "Output Limit Exceeded": "Output Limit Exceeded",
        "Runtime Error": "Runtime Error",
        "Queuing": "Judging",
        "Running": "Judging",
        "Compiling": "Judging"
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
        "Pascal": "Pascal",
        "C#": "C#"
    }
    if language_dict.get(language):
        return language_dict[language]
    return 'Other'


def main(username):
    return_data = []
    last = 0
    cnt = 0

    while cnt < 300:  # VJ 的那几个账号不考虑
        url = 'http://acm.hdu.edu.cn/status.php?last={}&user={}&status=#status'.format(
            last, username)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        trs = soup.find_all('tr', attrs={'align': 'center'})
        for tr in trs[2:-1][::-1]:
            tds = tr.find_all('td')
            run_id = tds[0].string
            submit_time = tds[1].string
            result = result_fix(tds[2].string)
            problem = tds[3].string
            time = tds[4].string[:-2]
            memory = tds[5].string[:-1]
            code_len = tds[6].string
            language = language_fix(tds[7].string)
            user = tds[8].string
            return_data.append({
                'runid': run_id,
                'pid': problem,
                'source': 'POJ',
                'result': result,
                'time': time,
                'memory': memory,
                'submission_time': submit_time,
                'language': language,
                'username': user,
                'code_length': code_len,
            })
            last = str(int(run_id) + 1)
        print(last)
        if len(trs) != 18:
            break

    return return_data


if __name__ == '__main__':
    print(json.dumps(main('MeiK'), indent=4, ensure_ascii=False))
