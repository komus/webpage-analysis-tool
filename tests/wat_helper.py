from html.parser import HTMLParser
from bs4 import BeautifulSoup, NavigableString
from pandas import DataFrame


class HTMLTestParser(HTMLParser):
    """
        Helper class to extract tags
    """
   
    start_tags = list()
    end_tag = list()
    start_end_tag = list()


    def handle_starttag(self, startTag, attrs):
        self.start_tags.append(startTag)

    def handle_endtag(self, endTag):
        self.end_tag.append(endTag)

    def handle_startendtag(self,startendTag, attrs):
        self.start_end_tag.append(startendTag)


class HTMLInsightHelper:
    """
        Helper class to generate insight from WebPages
    """
    def __get_node_path(self, d, p = [], c = 0):
        if not (k:=[i for i in getattr(d, 'contents', []) if not isinstance(i, NavigableString)]):
            yield (c, ' > '.join(p+[d.name]))
        else:
            for i in k:
                yield from self.__get_node_path(i, p=p+[d.name],c = c+1)

    def get_longest_path(self, content:bytes):
        _, path = max(self.__get_node_path(BeautifulSoup(content, 'html.parser').html), key=lambda x:x[0])
        return path

    def get_most_common_tag(self, content: bytes) -> str:
        all_tags = self.__all_tags(content)
        return all_tags.value_counts().index[0][0]

    def __all_tags(self, content:bytes) -> DataFrame:
        parse  = HTMLTestParser()
        parse.feed(content.decode("utf-8"))
        parse.start_tags.extend(parse.start_end_tag)
        all_tags = DataFrame(parse.start_tags, columns=['tags'])
        return all_tags

    def get_longest_path_with_most_common_tag(self, content: bytes):
        common_tag = self.get_most_common_tag(content)

        results= self.__get_node_path(BeautifulSoup(content, 'html.parser').html)
        data = [list(r) for r in results]
        df_result = DataFrame(data, columns=['discard', 'tags']).drop(columns=['discard'])
        df_result['most_common_count'] = df_result['tags'].str.findall(common_tag).str.len()
        return df_result.sort_values(by=['most_common_count', 'tags'], ascending=False)['tags'].values[0]

