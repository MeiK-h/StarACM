import time
import json

import requests


def language_fix(language):
    language_dict = {
        "D": "D",
        "Go": "Go",
        "PHP": "PHP",
        "GNU C11": "C",
        "Perl": "Perl",
        "Ruby": "Ruby",
        "Rust": "Rust",
        "Java": "Java",
        "Mono C#": "C#",
        "MS C++": "C++",
        "FPC": "Pascal",
        "Java 8": "Java",
        "Scala": "Scala",
        "PyPy 2": "Python",
        "PyPy 3": "Python",
        "Kotlin": "Kotlin",
        "Delphi": "Delphi",
        "GNU C++11": "C++",
        "GNU C++14": "C++",
        "GNU C++17": "C++",
        "Python 2": "Python",
        "Python 3": "Python",
        "Haskell": "Haskell",
        "Node.js": "JavaScript",
        "PascalABC.NET": "Pascal",
        "JavaScript": "JavaScript",
        "Clang++17 Diagnostics": "C++",
    }
    if language_dict.get(language):
        return language_dict[language]
    return 'Other'


def result_fix(result):
    result_dict = {
        "FAILED": "System Error",
        "OK": "Accepted",
        "PARTIAL": "Judging",
        "COMPILATION_ERROR": "Compile Error",
        "RUNTIME_ERROR": "Runtime Error",
        "WRONG_ANSWER": "Wrong Answer",
        "PRESENTATION_ERROR": "Presentation Error",
        "TIME_LIMIT_EXCEEDED": "Time Limit Exceeded",
        "MEMORY_LIMIT_EXCEEDED": "Memory Limit Exceeded",
        "TESTING": "Judging",
        "REJECTED": "Judging"
    }
    if result_dict.get(result):
        return result_dict[result]
    return 'Other'


def main(username):
    # CodeForces 提供 API
    url = 'http://codeforces.com/api/user.status?handle={}&from=1'.format(
        username)
    req = requests.get(url)
    data = json.loads(req.text)
    return_data = []
    for i in data['result'][::-1]:
        run_id = str(i['id'])
        pid = '{} - {}'.format(i['problem']['contestId'],
                               i['problem']['index'])
        creation_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(i['creationTimeSeconds']))
        language = language_fix(i['programmingLanguage'])
        time_used = str(i['timeConsumedMillis'])
        memory = str(i['memoryConsumedBytes'] // 1024)
        result = result_fix(i['verdict'])
        return_data.append({
            'runid': run_id,
            'pid': pid,
            'source': 'CodeForces',
            'result': result,
            'time': time_used,
            'memory': memory,
            'submission_time': creation_time,
            'language': language,
            'username': username,
        })
    return return_data


if __name__ == '__main__':
    print(json.dumps(main('MeiK'), indent=4, ensure_ascii=False))
