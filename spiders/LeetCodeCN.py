import requests
import json
import time


def language_fix(language):
    language_dict = {
        "c": "C",
        "cpp": "C++",
        "java": "Java",
        "python": "Python",
        "python3": "Python",
        "csharp": "C#",
        "javascript": "JavaScript",
        "ruby": "Ruby",
        "swift": "Swift",
        "golang": "Go",
        "scala": "Scala"
    }
    if language_dict.get(language):
        return language_dict[language]
    return 'Other'


def result_fix(result):
    result = result.lower()
    result_dict = {
        "accepted": "Accepted",
        "wrong answer": "Wrong Answer",
        "internal error": "System Error",
        "runtime error": "Runtime Error",
        "compile error": "Compile Error",
        "timeout": "Time Limit Exceeded",
        "time limit exceeded": "Time Limit Exceeded",
        "memory-limit-exceeded": "Memory Limit Exceeded",
        "output-limit-exceeded": "Output Limit Exceeded",
        "pending": "Judging",
        "judging": "Judging"
    }
    if result_dict.get(result):
        return result_dict[result]
    return 'Other'


def main(username, password, last=0):
    return_data = []
    session = requests.Session()
    session.get('https://leetcode-cn.com/accounts/login/')
    post_data = {
        'csrfmiddlewaretoken': session.cookies.get('csrftoken'),
        'login': username,
        'password': password,
        'next': '/problems'
    }
    req = session.post('https://leetcode-cn.com/accounts/login/', data=post_data,
                       headers={'referer': 'https://leetcode-cn.com/accounts/login/'}, allow_redirects=False)
    if req.status_code != 302 or req.headers.get('Location') != '/problems':
        print('登陆失败')
        return []

    cnt = 0
    lastkey = ''
    offset = 0
    while cnt < 100:
        url = 'https://leetcode-cn.com/api/submissions/?offset={}&limit=20&lastkey={}'.format(
            offset, lastkey)
        req = session.get(url)
        data = json.loads(req.text)
        if data.get('detail') == '您没有执行该操作的权限。':  # 被限制
            time.sleep(1)
            continue
        lastkey = data['last_key']
        for i in data['submissions_dump']:
            runid = i['id']
            if last >= int(runid):
                data['has_next'] = False
                break
            problem = i['title']
            submit_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(i['timestamp']))
            result = result_fix(i['status_display'])
            time_used = i['runtime'][:-2]
            language = language_fix(i['lang'])
            return_data.append({
                'runid': runid,
                'pid': problem,
                'source': 'LeetCode-CN',
                'result': result,
                'time': time_used,
                'memory': 0,
                'submission_time': submit_time,
                'language': language,
                'username': username,
            })
        if not data['has_next']:
            break
        print(offset)
        offset += 20
    return return_data[::-1]


if __name__ == '__main__':
    print(json.dumps(main('MeiK', '******'), indent=4, ensure_ascii=False))
