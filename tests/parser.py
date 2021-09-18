from html.parser import HTMLParser

class HTMLTestParser(HTMLParser):
    """
        Class to asset the result of BeautifulSoup
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