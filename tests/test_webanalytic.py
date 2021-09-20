import pytest
from analytic import WebPageAnalyticTool
from wat_helper import HTMLTestParser, HTMLInsightHelper


URL = 'https://edition.cnn.com/'


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
    URL = 'https://www.bbc.com/sport/football'
    assert WebPageAnalyticTool(URL).url == 'https://www.bbc.com/sport/football'


def test_header_property():
    header_info = {'referer': 'https://www.justatestsite.com/',
              'accept-language': 'en-US,en;q=0.9',
                            }
    wat = WebPageAnalyticTool()
    wat.header = header_info
    assert wat.header == header_info


def test_get_all_tags():
    wat = WebPageAnalyticTool(URL)
    parser = HTMLTestParser()
    parser.feed(wat.get_content.decode("utf-8"))
    assert len(wat.get_all_tags) == len(parser.start_tags) + len(parser.start_end_tag)


def test_get_unique_tags():
    wat = WebPageAnalyticTool(URL)
    HTMLTestParser().reset()
    parser = HTMLTestParser()
    parser.feed(wat.get_content.decode("utf-8"))
    parser.start_tags.extend(parser.start_end_tag)
    assert wat.get_unique_tags == set(parser.start_tags)


def test_most_common_tags():
    wat = WebPageAnalyticTool(URL)
    wat_helper_common_tag = HTMLInsightHelper().get_most_common_tag(content=wat.get_content)
    assert wat.get_most_common_tags == wat_helper_common_tag


def test_longest_path():
    wat = WebPageAnalyticTool(URL)
    content = wat.get_content
    wat_helper_longest_path = HTMLInsightHelper().get_longest_path(content)

    assert wat.get_longest_path == wat_helper_longest_path


def test_longest_path_with_most_common_tag():
    wat = WebPageAnalyticTool(URL)
    content = wat.get_content
    wat_helper_path = HTMLInsightHelper().get_longest_path_with_most_common_tag(content)

    assert wat.get_longest_path_with_most_common_tag == wat_helper_path
