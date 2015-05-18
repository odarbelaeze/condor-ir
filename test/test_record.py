import pytest
from xml.dom import minidom
from lsa import Record


@pytest.fixture(scope='module')
def xml_text(request):
    return '''
<record>
<lom:lom xmlns:lom="http://ltsc.ieee.org/xsd/LOM">
<lom:title>title</lom:title>
<lom:description>description</lom:description>
<lom:keyword>keyword1</lom:keyword>
<lom:keyword>keywird2</lom:keyword>
</lom:lom>
</record>
    '''


@pytest.fixture(scope='module')
def xml_element(request, xml_text):
    return minidom.parseString(xml_text)


def test_record_wrapper_is_instantiable(xml_element):
    record = Record(xml_element)
    assert record is not None


@pytest.fixture
def record(request, xml_element):
    return Record(xml_element)


@pytest.fixture
def empty_record(request):
    return Record(minidom.parseString('<record></record>'))


def test_record_wrapper_yields_title(record):
    assert 'title' == record.title


def test_record_wraper_yields_description(record):
    assert 'description' == record.description


def test_record_wrapper_yields_title_in_empty_reccord(empty_record):
    assert '' == empty_record.title


def test_record_wrapper_yields_description_in_empty_reccord(empty_record):
    assert '' == empty_record.description
