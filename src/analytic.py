from requests_testadapter import Resp
from collections import Counter
from bs4 import BeautifulSoup
import re
import requests
import os


class WebPageAnalyticTool:
    """
        A class used to analyse the tags of a webpage
        ...

        Attributes
        ----------
        
        
        Methods
        -------
        
    """

    def __init__(self, url: str = 'www.google.com') -> None:
        self.__url = self.__formaturl(url)
        self.__unique_tags = None
        self.__most_common_tag = []
        self.__longest_path = None
        self.__content = None
        self.__headers = {
                            'upgrade-insecure-requests': '1',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
                            'accept': 't	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'sec-fetch-site': 'cross-site',
                            'sec-fetch-mode': 'navigate',
                            'sec-fetch-user': '?1',
                            'sec-fetch-dest': 'document',
                            'referer': 'https://www.google.com/',
                            'accept-language': 'en-US,en;q=0.9',
                            }

        self.__validate_input(self.__url)
        self.__validate_webpage_exist(self.__url, self.__headers)


    @staticmethod
    def __validate_input(url: str) -> None:

        """
            Check if the url passed is a valid string

            Parameters
            ----------
                url: string
                    The url of the webpage

            returns
            --------
                bool

        """

        if not isinstance(url, str):
            raise TypeError('accepted type is string for url')


    def __validate_webpage_exist(self, url:str, headers) -> tuple:
        if not re.match('(?:http|ftp|https|file)://', url):
            content = requests.get(url, headers=headers)
            if content.status_code != 200:
                raise ValueError(f"supplied {url} returned status code {content.status_code}")
            else:
                self.__content = content.content
        else:
            requests_session = requests.session()
            requests_session.mount('file://', LocalFileAdapter())
            r = requests_session.get(url)
            
            self.__content = r.content

    def __formaturl(self,url):
        if not re.match('(?:http|ftp|https|file)://', url):
            return 'http://{}'.format(url)
        return url

    @property
    def url(self) -> str:
        '''
            returns the url
        '''
        return self.__url

    @property
    def header(self) -> str:
        return self.__headers

    @header.setter
    def header(self, header_info:str) -> None:
        self.__headers = header_info

    @property
    def get_content(self):
        return self.__content

    def __get_all_tags(self):
        soup = BeautifulSoup(self.__content, "html.parser")
        return [tag.name for tag in soup.find_all()]

    @property
    def get_all_tags(self):
        return self.__get_all_tags()

    # def get_all_tags(self):
    #     tags = re.findall(rb'<(.*)>.*?|<(.*) /><(\S*?)[^>]*>.*?</\1>|<.*?/>', self.__content)
    #     return tags

    def get_all_insights(self):
        tags = self.get_all_tags()
        
    
    def __get_unique_tags(self):
        return set(self.__get_all_tags())

    @property
    def get_unique_tags(self):
        return self.__get_unique_tags()

    def __get_most_common_tag(self):
       return sorted(Counter(self.__get_all_tags()).most_common(1))[0][0]

    @property
    def get_most_common_tags(self):
        return self.__get_most_common_tag()

class LocalFileAdapter(requests.adapters.HTTPAdapter):
    """
        Helper class to read local files
    """
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)