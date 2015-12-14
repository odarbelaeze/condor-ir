import pytest
from xml.dom import minidom
from lsa.record import FroacRecordSet as RecordSet


@pytest.fixture(scope='module')
def reccords_text(request):
    return '''
<records>
<record>
<lom:lom xmlns:lom="http://ltsc.ieee.org/xsd/LOM">
<lom:title>title1</lom:title>
<lom:description>description1</lom:description>
<lom:keyword>keyword11</lom:keyword>
<lom:keyword>keywird12</lom:keyword>
</lom:lom>
</record><record>
<lom:lom xmlns:lom="http://ltsc.ieee.org/xsd/LOM">
<lom:title>title2</lom:title>
<lom:description>description2</lom:description>
<lom:keyword>keyword21</lom:keyword>
<lom:keyword>keywird22</lom:keyword>
</lom:lom>
</record>
</records>
'''


@pytest.fixture(scope='module')
def reccords_xml(request, reccords_text):
    return minidom.parseString(reccords_text)


@pytest.fixture(scope='module')
def record_set(reccords_xml):
    return RecordSet(reccords_xml)


def test_record_set_is_instantiable(record_set):
    assert record_set is not None


def test_record_set_is_iterable_container(record_set):
    assert iter(record_set) is not iter(record_set)


@pytest.skip
def test_record_set_yields_a_record_for_each_Record_in_xml(record_set,
                                                           reccords_xml):
    num_records = len(reccords_xml.getElementsByTagName('record'))
    assert num_records == len(list(record_set))


@pytest.skip
def test_assert_all_titles_in_record_set(record_set):
    titles = [record.title for record in record_set]
    for title in ['title1', 'title2']:
        assert title in titles
