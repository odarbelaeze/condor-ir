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
<lom:keyword>keyword2</lom:keyword>
</lom:lom>
</record>
    '''


@pytest.fixture(scope='module')
def xml_element(request, xml_text):
    return minidom.parseString(xml_text)


def test_record_wrapper_is_instantiable(xml_element):
    record = Record(xml_element)
    assert record is not None


@pytest.fixture(scope='module')
def record(request, xml_element):
    return Record(xml_element)


@pytest.fixture(scope='module')
def empty_record(request):
    return Record(minidom.parseString('<record></record>'))


@pytest.fixture(scope='module')
def sw_record_xml(request):
    return minidom.parseString(
        '''
        <record>
        <lom:lom xmlns:lom="http://ltsc.ieee.org/xsd/LOM">
        <lom:keyword>a</lom:keyword>
        <lom:keyword>ante</lom:keyword>
        <lom:keyword>bajo</lom:keyword>
        <lom:keyword>of</lom:keyword>
        <lom:keyword>in</lom:keyword>
        </lom:lom>
        </record>
        ''')


@pytest.fixture(scope='module')
def sw_record(request, sw_record_xml):
    return Record(sw_record_xml, strip_stopwords=True)


def test_record_wrapper_yields_title(record):
    assert 'title' == record.title


def test_record_wraper_yields_description(record):
    assert 'description' == record.description


def test_record_wrapper_yields_title_in_empty_reccord(empty_record):
    assert '' == empty_record.title


def test_record_wrapper_yields_description_in_empty_reccord(empty_record):
    assert '' == empty_record.description


def test_record_wrapper_yields_list_of_keywords(record):
    assert len(record.keywords)
    for key in ['keyword1', 'keyword2']:
        assert key in record.keywords


def test_record_empty_list_of_keywords_on_empty_record(empty_record):
    assert not len(empty_record.keywords)
    assert [] == empty_record.keywords


def test_record_raw_data(record, empty_record):
    data = ['title', 'keyword1', 'keyword2', 'description']
    assert sorted(data) == sorted(record.raw)
    assert not empty_record.raw


def test_record_raw_data_with_no_stopwords(sw_record):
    assert not sw_record.raw
