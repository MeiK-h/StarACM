import json
import os

from spiders.SDUT import main as SDUT
from spiders.POJ import main as POJ
from spiders.HDU import main as HDU


def main():
    with open('account.json') as fr:
        data = json.loads(fr.read())
    if not os.path.exists('result'):
        os.mkdir('result')

    if data.get('SDUT'):
        print('开始获取 SDUT')
        sdut_data = SDUT(data['SDUT'])
        with open(os.path.join('result', 'SDUT.json'), 'w') as fw:
            fw.write(json.dumps(sdut_data, indent=4, ensure_ascii=False))
        print('SDUT 获取完成')
    if data.get("POJ"):
        print('开始获取 POJ')
        poj_data = POJ(data['POJ'])
        with open(os.path.join('result', 'POJ.json'), 'w') as fw:
            fw.write(json.dumps(poj_data, indent=4, ensure_ascii=False))
        print('POJ 获取完成')
    if data.get('HDU'):
        print('开始获取 HDU')
        hdu_data = HDU(data['HDU'])
        with open(os.path.join('result', 'HDU.json'), 'w') as fw:
            fw.write(json.dumps(hdu_data, indent=4, ensure_ascii=False))
        print('HDU 获取完成')
    # if data.get('CodeForces'):
    #     print('开始获取 CodeForces')
    #     cf_data = CodeForces(data['CodeForces'])
    #     with open(os.path.join('result', 'CodeForces.json'), 'w') as fw:
    #         fw.write(json.dumps(cf_data, indent=4, ensure_ascii=False))
    #     print('CodeForces 获取完成')
    # if data.get('Virtual Judge'):
    #     print('开始获取 Virtual Judge')
    #     vj_data = VirtualJudge(data['Virtual Judge'])
    #     with open(os.path.join('result', 'Virtual-Judge.json'), 'w') as fw:
    #         fw.write(json.dumps(vj_data, indent=4, ensure_ascii=False))
    #     print('Virtual Judge 获取完成')
    # if data.get('LeetCode-CN'):
    #     print('开始获取 LeetCode-CN')
    #     leetcode_cn_data = LeetCodeCN(data['LeetCode-CN'])
    #     with open(os.path.join('result', 'LeetCode-CN.json'), 'w') as fw:
    #         fw.write(json.dumps(leetcode_cn_data, indent=4, ensure_ascii=False))
    #     print('LeetCode-CN 获取完成')


if __name__ == '__main__':
    main()
