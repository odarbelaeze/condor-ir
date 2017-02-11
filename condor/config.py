import os


CONDOR_PATH = os.path.expanduser('~/.condor')
TERM_LIST_PATH = os.path.join(CONDOR_PATH, 'term_lists')
MATRIX_PATH = os.path.join(CONDOR_PATH, 'matrices')
MODEL_PATH = os.path.join(CONDOR_PATH, 'models')
DEFAULT_DB_PATH = CONDOR_PATH

ALL_CONDOR_PATHS = [
    CONDOR_PATH,
    TERM_LIST_PATH,
    MATRIX_PATH,
    MODEL_PATH,
    DEFAULT_DB_PATH,
]


for path in ALL_CONDOR_PATHS:
    if not os.path.exists(path):
        os.mkdir(path)
