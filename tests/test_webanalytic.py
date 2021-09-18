import sys
import pytest
sys.path.append("src/")
from analytic import WebPageAnalyticTool
from parser import HTMLTestParser
from pandas import DataFrame


def test_url_is_string():
    url = 'justastring'
    assert isinstance(url, str)

def test_error_for_non_string_url():
    url = 10
    with pytest.raises(Exception):
        WebPageAnalyticTool(url)

def test_return_base_url_method():
    assert WebPageAnalyticTool().url == 'http://www.google.com'

def test_return_users_input_url():
    url = 'file:///home/oyindolapo/Documents/PythonProjects/monetha/segmentation-model/segmentation-models/results/10/LTVcohorts_by_segments_relative.html'
    assert WebPageAnalyticTool(url).url == 'file:///home/oyindolapo/Documents/PythonProjects/monetha/segmentation-model/segmentation-models/results/10/LTVcohorts_by_segments_relative.html'

def test_header_property():
    header_info = {'referer': 'https://www.justatestsite.com/',
              'accept-language': 'en-US,en;q=0.9',
                            }
    wat = WebPageAnalyticTool()
    wat.header = header_info
    assert wat.header == header_info

def test_get_all_tags():
    url = 'https://skeptric.com/python-html-parser/'
    wat = WebPageAnalyticTool(url)
    parser = HTMLTestParser()
    parser.feed(wat.get_content.decode("utf-8"))

    assert len(wat.get_all_tags) == len(parser.start_tags) + len(parser.start_end_tag)
    
def test_get_unique_tags():
    url = 'https://skeptric.com/python-html-parser/'
    wat = WebPageAnalyticTool(url)
    parser = HTMLTestParser()
    parser.feed(wat.get_content.decode("utf-8"))
    parser.start_tags.extend(parser.start_end_tag)
    assert wat.get_unique_tags == set(parser.start_tags)


def test_most_common_tags():
    url = 'https://skeptric.com/python-html-parser/'
    wat = WebPageAnalyticTool(url)
    parser = HTMLTestParser()
    parser.feed(wat.get_content.decode("utf-8"))
    parser.start_tags.extend(parser.start_end_tag)
    all_tags = DataFrame(parser.start_tags, columns=['tags'])
    assert wat.get_most_common_tags == all_tags.value_counts().index[0][0]