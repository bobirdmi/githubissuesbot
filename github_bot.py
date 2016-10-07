import requests
import json
import configparser
import re


class GitHubBot:
    def __init__(self, auth_file, label_file):
        self._read_config(auth_file, label_file)

        self._session = requests.Session()
        self._session.headers = {'Authorization': 'token ' + self._token, 'User-Agent': 'Python'}

    def _read_config(self, auth_file, label_file):
        conf = configparser.ConfigParser()
        conf.read([auth_file, label_file])

        self._token = conf['github']['token']

        self._label_list = list(map(str.strip, conf['list']['labels'].split(',')))
        print("List of labels: ", self._label_list)

        self._label_rules = []
        for label in self._label_list:
            self._label_rules.append(conf['rules'][label])

    def label_issues(self):
        url = 'https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/issues'
        r = self._session.get(url)
        issues_num = len(r.json())
        print(issues_num)

        for issue_id in range(issues_num):
            issue_info = r.json()[issue_id]
            if issue_info['labels']:
                continue

            self._set_labels(url, issue_info['number'], issue_info['title'], issue_info['body'])

    def _set_labels(self, url, issue_num, title, body):
        text = title + " " + body
        labels = []

        index = 0
        for rule in self._label_rules:
            if re.search(rule, text):
                labels.append(self._label_list[index])

            index += 1

        print("Found labels: ", labels)

        r = self._session.post(url + '/' + str(issue_num) + '/labels', data=json.dumps(labels))
        print('Status code: ', r.status_code)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('./config/auth.cfg')
    token = config['github']['token']

    session = requests.Session()
    session.headers = {'Authorization': 'token ' + token, 'User-Agent': 'Python'}
    # r = session.get('https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/issues/3/labels')
    r = session.get('https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/issues')
    # r = session.get('https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/labels')
    print(r.status_code)
    print(len(r.json()))
    print(r.json()[1])
    print(r.json()[1]['url'])
    print(r.json()[1]['labels_url'])
    # print(r.json()['title'])
    # print(r.json()['body'])

    # json_obj = json.loads(r.json())
    # print(json_obj.labels)

    # print(r.json()[0]['labels'])
    # # print(r.json()[1]['labels'][0]['name'])
    # print(r.json()[1]['labels'])
    # print(r.json()[2]['labels'])

    # r = session.post('https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/issues/3/labels',
    #                  data=json.dumps(['bug']))
    # print(r.status_code)
    # print(r.json())
