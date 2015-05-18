import functools


def xml_to_text(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return ''
        return result.firstChild.nodeValue
    return inner


class Record(object):
    def __init__(self, xml):
        self.xml = xml

    @property
    @xml_to_text
    def title(self):
        return self.xml.getElementsByTagName('lom:title').item(0)

    @property
    @xml_to_text
    def description(self):
        return self.xml.getElementsByTagName('lom:description').item(0)
