import requests
import json
import configparser
import re


class GitHubBot:
    def __init__(self, auth_file, label_file, url, period, default_label):
        self._read_config(auth_file, label_file)

        self.url = url
        self.period = period
        self.default_label = default_label

        self._session = requests.Session()
        self._session.headers = {'Authorization': 'token ' + self._token, 'User-Agent': 'Python'}

    def _read_config(self, auth_file, label_file):
        conf = configparser.ConfigParser()
        conf.read([auth_file, label_file])

        self._token = conf['github']['token']

        self._label_list = list(map(str.strip, conf['list']['labels'].split(',')))
        print("List of defined labels:", self._label_list)

        self._label_rules = []
        for label in self._label_list:
            self._label_rules.append(conf['rules'][label])

    def label_issues(self, label_comments):
        r = self._session.get(self.url)
        r.raise_for_status()

        issues_num = len(r.json())
        for issue_id in range(issues_num):
            issue_info = r.json()[issue_id]
            if issue_info['labels']:
                continue

            self._set_labels(issue_info['number'], issue_info['title'], issue_info['body'], label_comments)

    def _set_labels(self, issue_num, title, body, label_comments):
        issue_url = self.url + '/' + str(issue_num)
        text = title + " " + body

        if label_comments:
            # add comments' body to issue's text
            r = self._session.get(issue_url + '/comments')
            for comm in r.json():
                text += ' ' + comm['body']

        labels = []
        index = 0
        for rule in self._label_rules:
            if re.search(rule, text):
                labels.append(self._label_list[index])

            index += 1

        print(10 * '-')
        print('Issue number:', issue_num)
        print('Issue title:', title)
        print('Issue url:', issue_url)

        if not labels:
            labels.append(self.default_label)

        print("Labeled as:", labels)

        r = self._session.post(issue_url + '/labels', data=json.dumps(labels))
        print('Status code:', r.status_code)

if __name__ == '__main__':
    # the following code is only for testing purposes (as functionality and new ideas)
    config = configparser.ConfigParser()
    config.read('./config/auth.cfg')
    token = config['github']['token']

    session = requests.Session()
    session.headers = {'Authorization': 'token ' + token, 'User-Agent': 'Python'}

    # r = session.get('https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/issues/3/labels')
    # r = session.get('https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/labels')
    # r = session.get('https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/issues')
    r = session.get('https://api.github.com/repos/bobirdmi/MIPYTGitHubBot/issues/11/comments')
    print(r.status_code)
    print(len(r.json()))
    print(r.json())
    print(r.json()[1])
    print(r.json()[1]['url'])
    # print(r.json()[1]['labels_url'])
    # print(r.json()[1]['comments_url'])
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
