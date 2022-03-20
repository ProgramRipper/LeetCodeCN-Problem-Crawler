from argparse import ArgumentParser, Namespace
from html import unescape
from json import dumps
from json import loads
from os.path import abspath
from re import sub

from html2text import html2text
from requests import Session

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 ' \
             'Safari / 537.36'
url = 'https://leetcode-cn.com/'

parser = ArgumentParser()

parser.add_argument('path', type=str, help='Output path')
parser.add_argument('-d', '--difficulty', type=int,
                    help='Choose the difficulty of the problems.'
                         '\nIf not specified, all problems will be grasped.'
                         '\n"1" means easy,"2" means medium and "3" means hard.',
                    choices=[1, 2, 3])
parser.add_argument('-l', '--language', type=str,
                    help='Choose the language of the descriptions.'
                         '\nIf not specified, untranslatedContent(en) will be grasped.',
                    choices=['zh-CN', 'en'], default='en')
parser.add_argument('-s', '--status', type=str,
                    help='Choose the status of the problems.'
                         '\nIf not specified, all problems will be grasped.'
                         '\nYou need to login first to get your status of all problems.'
                         '\n"ac" means the problems which you have solved.'
                         '\n"notac" means the problems which you have tried to solved.'
                         '\n"null" means the problems which you have never tried.',
                    choices=['ac', 'notac', 'null'])
parser.add_argument('-f', '--format', type=str,
                    help='Choose the format of the descriptions.'
                         '\nIf not specified, .md will be generated',
                    choices=['md', 'txt'], default='md')


class Main:
    def __init__(self, args: Namespace) -> None:
        self.path = abspath(args.path) + '\\'
        self.level = args.difficulty
        self.format = args.format
        self.lang = args.language
        self.status = args.status

        self.session = Session()
        self.session.encoding = 'utf-8'
        self.session.headers.update({
            'User-Agent': user_agent,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json'
        })

        with open('config.json', 'r', encoding='utf-8') as f:
            f = loads(f.read())
            self.account = f['account']
            self.password = f['password']
        self.login()
        for i in self.problem_list():
            if i['stat']['is_new_question']:
                continue
            if self.level is None:
                pass
            elif i['difficulty']['level'] != self.level:
                continue
            if self.status is None:
                pass
            elif i['status'] != self.status:
                continue

            info = self.download_info(i['stat']['question__title_slug'])

            if self.lang == 'en':
                title = f"{info['questionFrontendId']}.{info['title']}"
                content = info['content']
            elif self.lang == 'zh-CN':
                title = f"{info['questionFrontendId']}.{info['translatedTitle']}"
                content = info['translatedContent']
            if content is None:
                continue
            if self.format == 'md':
                self.save_markdown(title, content)
            elif self.format == 'txt':
                self.save_text(title, content)

            print(title)

    def login(self):
        while True:
            try:
                self.session.get(f'{url}accounts/login/')
                data = {'login': self.account,
                        'password': self.password
                        }
                response = self.session.post(
                    f'{url}accounts/login/',
                    data=data,
                    headers=dict(Referer=url + 'accounts/login/'),
                )


                if response.ok:
                    print('Login successfully!')
                    break
            except:
                print('Login failed! Wait till next round!')

    def problem_list(self) -> list:
        headers = {'Referer': f'{url}problems/'}
        return self.session.get(f'{url}api/problems/all/', headers=headers).json()[
            'stat_status_pairs'
        ]

    def download_info(self, slug):
        params = {'operationName': 'questionData',
                  'variables': {'titleSlug': slug},
                  'query': '''query questionData($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionId
                    questionFrontendId
                    title
                    content
                    translatedTitle
                    translatedContent
                }
            }'''
                  }
        headers = {'Referer': f'{url}problems/{slug}'}
        data = dumps(params).encode('utf-8')
        return unescape(
            self.session.post(f'{url}graphql/', data=data, headers=headers).json()[
                'data'
            ]['question']
        )

    def save_markdown(self, title, content):
        title = sub('[\/:*?"<>|]', '', title)
        with open(self.path + title + '.md', 'w', encoding='utf-8') as f:
            f.write('# {}\n{}'.format(title, html2text(content)))

    def save_text(self, title, content):
        title = sub('[\/:*?"<>|]', '', title)
        with open(self.path + title + '.txt', 'w', encoding='utf-8') as f:
            f.write('{}\n{}'.format(title, content))


if __name__ == '__main__':
    args = parser.parse_args()
    Main(args)
