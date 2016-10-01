import os


CONDOR_PATH = os.path.expanduser('~/.condor')
TERM_LIST_PATH = os.path.join(CONDOR_PATH, 'term_lists')
MATRIX_PATH = os.path.join(CONDOR_PATH, 'matrices')
MODEL_PATH = os.path.join(CONDOR_PATH, 'models')

for path in [CONDOR_PATH, TERM_LIST_PATH, MATRIX_PATH, MODEL_PATH]:
    if not os.path.exists(path):
        os.mkdir(path)
