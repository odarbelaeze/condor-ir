from .bib import BibtexRecordParser, BibtexRecordIterator
from .froac import FroacRecordParser, FroacRecordIterator
from .isi import IsiRecordParser, IsiRecordIterator


def record_iterator_class(record_type):
    """
    Gets the record iterator for a given type
    
    A way to abstract the construction of a record iterator class.

    :param record_type: the type of file as string
    :return: the appropriate record iterator class
    """
    if record_type == 'bib':
        return BibtexRecordIterator
    elif record_type == 'froac' or record_type == 'xml':
        return FroacRecordIterator
    elif record_type == 'isi':
        return IsiRecordIterator
    else:
        raise ValueError("This type {} has not been implemented yet".format(
            record_type
        ))
