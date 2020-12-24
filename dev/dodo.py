import os
import shutil
import glob
import pathlib
import json
import nbdime

DOIT_CONFIG = {'default_tasks': ['execute']}

DEV_NB_DIR = 'notebooks'
DOC_NB_DIR = '../docs/notebooks'
SRC_NB_DIR = '../notebooks'
GIT_NB_DIR = SRC_NB_DIR

def load_json(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

def are_same_notebooks(filename1, filename2):
    nbdime.diffing.notebooks.set_notebook_diff_targets(sources=True, outputs=False, attachments=False, metadata=False, details=False) 
    try:
        diff = nbdime.diff_notebooks(load_json(filename1),load_json(filename2))
    except:
        return False
    return len(diff) == 0

def nb_uptodate(source, target):
    if not target.exists():
        return False
    return are_same_notebooks(source, target)

def timestamp_uptodate(target, source):
    if not target.exists():
        return False
    return os.path.getatime(source) <= os.path.getatime(target)

def task_init():
    '''
    Copy files to initialize the development
    '''
    def copy_to_dev(targets):
        for target in targets:
            shutil.copy2(pathlib.Path(SRC_NB_DIR) / pathlib.Path(target).name, DEV_NB_DIR)

    sources = list(pathlib.Path(SRC_NB_DIR).glob('*.ipynb'))
    sources = sources + list(pathlib.Path(SRC_NB_DIR).glob('*.py'))
    sources = sources + list(pathlib.Path(SRC_NB_DIR).glob('requirements.txt')) # needed for test_environment
    dst = pathlib.Path(DEV_NB_DIR)
    targets = [dst / src.name for src in sources]
    for source, target in zip(sources, targets):
        yield {
            'name': target.name,
            'actions': [copy_to_dev],
            # 'file_dep': [source], # no file_dep to avoid cyclic dependencies
            'targets': [target],
            'uptodate': [nb_uptodate(target, source) or timestamp_uptodate(target, source)],
        }

def task_execute():
    '''
    Execute all notebooks
    '''
    dst = pathlib.Path(DOC_NB_DIR)
    sources = sorted(pathlib.Path(DEV_NB_DIR).glob('*.ipynb'))
    for i, fn in enumerate(sources):
        if 'img2img_comparison' in str(fn): # move img2img_comparison to the last
            del sources[i]
            sources.append(fn)
            break
    targets = [dst / src.name for src in sources]
    
    for source, target in zip(sources, targets):
        yield {
            'name': target.name,
            'actions': ['jupyter nbconvert --ExecutePreprocessor.timeout=-1 --to notebook --output-dir=. --output=%(targets)s --execute %(dependencies)s'],
            'file_dep': [source],
            'targets': [target],
            'uptodate': [timestamp_uptodate(target, source)],
        }

def task_clear():
    '''
    Clear all notebooks
    '''
    dst = pathlib.Path(GIT_NB_DIR)
    sources = list(pathlib.Path(DEV_NB_DIR).glob('*.ipynb'))
    targets = [dst / src.name for src in sources]
    
    for source, target in zip(sources, targets):
        yield {
            'name': target.name,
            'actions': ['jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to notebook --output-dir=. --output=%(targets)s %(dependencies)s'],
            'file_dep': [source],
            'targets': [target],
            'uptodate': [nb_uptodate(target, source)],
        }
def task_precommit():
    '''
    Run this before git commit.
    '''
    def copy_to_git(targets):
        for target in targets:
            shutil.copy2(pathlib.Path(DEV_NB_DIR) / pathlib.Path(target).name, GIT_NB_DIR)

    sources = list(pathlib.Path(DEV_NB_DIR).glob('*.py'))
    dst = pathlib.Path(GIT_NB_DIR)
    targets = [dst / src.name for src in sources]
    for source, target in zip(sources, targets):
        yield {
            'name': target.name,
            'actions': [copy_to_git],
            'targets': [target],
            'task_dep':['clear'],
            'uptodate': [timestamp_uptodate(target, source)],
        }

def task_html():
    '''
    Run make html
    '''
    return {
        'actions':[r'..\docs\make html'],
        'task_dep':['execute'],
    }

def task_latex():
    '''
    Run make latex
    '''
    return {
        'actions':[r'..\docs\make latex'],
        'task_dep':['execute'],
    }
