"""
Organize the downloaded Kaggle dataset which we assume has the following format:

    /path/to/your/dataset/
    ├── sample_submission.csv
    ├── test/
    │   ├── 1.jpg
    │   ├── 2.jpg
    │   ├── ...
    │   └── x.jpg
    └── train/
        ├── labelA.0.jpg
        ├── labelA.2.jpg
        ├── ...
        ├── labelA.x.jpg
        ├── labelB.0.jpg
        ├── labelB.2.jpg
        ├── ...
        └── labelB.x.jpg

The above will then be organized according to the structure outlined in the
**Preparing the Data** section of the lesson 2 notes:
http://wiki.fast.ai/index.php/Lesson_2_Notes
"""
import argparse
import fnmatch
import glob
import os
from shutil import copyfile, rmtree

import numpy as np

# The path of the specific dataset which you want to organize
# DATASET_PATH = '/path/to/your/dataset/directory/'
DATASET_PATH = ('/Users/chriskim/Dev/fastai-courses/datasets'
                '/dogs-vs-cats-redux-kernels-edition/')

DIR_VALID_NAME = 'valid'

DIR_SAMPLE_NAME = 'sample'

DIR_TRAIN_NAME = 'train'

DIR_TEST_NAME = 'test'

DIR_RESULTS_NAME = 'results'

FILE_PATTERN = '*.jpg'

# List of tuples which control the image classes we will be using.
# Position 0 is the label provided by Kaggle in the original train folder.
# Position 1 is the directory name we will use to group the categories.
CATEGORIES = [
    ('cat', 'cats'),
    ('dog', 'dogs'),
]

# The number of random files to move from the original training set to use as
# our validation set
VALIDATION_SIZE = 2000

# The number of random files to copy from the original training set to use as
# our sample training set
SAMPLE_SIZE = 200

# The number of random files to move from the original training set to use as
# our sample validation set
SAMPLE_VALIDATION_SIZE = 50


def _img_transfer(from_path, to_path, limit, move=False, pattern=FILE_PATTERN):
    """
    Copy or move image files. By default the action is to copy.
    In case this script is being re-run, only trasnfer up to the specified
    limit or do not transfer at all if category subdirectories exist.
    """
    do_transfer = True

    for label, dir_name in CATEGORIES:
        new_path = os.path.join(to_path, dir_name)
        if os.path.isdir(new_path):
            do_transfer = False
            break

    if do_transfer:
        files = glob.glob(os.path.join(from_path, pattern))
        shuf = np.random.permutation(files)
        count = len(fnmatch.filter(os.listdir(to_path), pattern))
        transfer_count = limit - count if count < limit else 0

        for i in range(transfer_count):
            new_file_path = os.path.join(to_path, os.path.basename(shuf[i]))
            if move:
                os.rename(shuf[i], new_file_path)
            else:
                copyfile(shuf[i], new_file_path)


def _group_categories(path, pattern=FILE_PATTERN):
    """
    Create category subdirectories within the given `path` and move existing
    image files based on labels into the proper folder.
    """
    for label, dir_name in CATEGORIES:
        new_path = os.path.join(path, dir_name)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)

        new_pattern = '{}.{}'.format(label, pattern)
        files = glob.glob(os.path.join(path, new_pattern))

        for f in files:
            new_file_path = os.path.join(new_path, os.path.basename(f))
            os.rename(f, new_file_path)


def reset():
    """
    Attempt to reset the dataset folder structure to the original Kaggle
    structure, described above. If a root result folder has been created, will
    leave that untouched in case weights have been saved.
    """
    # Delete the sample directory
    sample_dir = os.path.join(DATASET_PATH, DIR_SAMPLE_NAME)
    rmtree(sample_dir)

    # Move all training category images into the root and delete the
    # subdirectories
    train_dir = os.path.join(DATASET_PATH, DIR_TRAIN_NAME)
    cat_subdirs = [sub for sub in os.listdir(train_dir)
                   if os.path.isdir(os.path.join(train_dir, sub))]

    for cat in cat_subdirs:
        cat_path = os.path.join(train_dir, cat)
        files = glob.glob(os.path.join(cat_path, FILE_PATTERN))
        for f in files:
            move_path = os.path.join(train_dir, os.path.basename(f))
            os.rename(f, move_path)
        rmtree(cat_path)

    # Move all valid category images back into the training folder and delete
    # the valid directory
    valid_dir = os.path.join(DATASET_PATH, DIR_VALID_NAME)
    cat_subdirs = [sub for sub in os.listdir(valid_dir)
                   if os.path.isdir(os.path.join(valid_dir, sub))]

    for cat in cat_subdirs:
        cat_path = os.path.join(valid_dir, cat)
        files = glob.glob(os.path.join(cat_path, FILE_PATTERN))
        for f in files:
            move_path = os.path.join(train_dir, os.path.basename(f))
            os.rename(f, move_path)

    rmtree(valid_dir)


def main():
    # Original Kaggle directories
    train_dir = os.path.join(DATASET_PATH, DIR_TRAIN_NAME)
    test_dir = os.path.join(DATASET_PATH, DIR_TEST_NAME)

    # Create all the required directories
    valid_dir = os.path.join(DATASET_PATH, DIR_VALID_NAME)
    results_dir = os.path.join(DATASET_PATH, DIR_RESULTS_NAME)
    sample_dir = os.path.join(DATASET_PATH, DIR_SAMPLE_NAME)
    sample_valid_dir = os.path.join(DATASET_PATH, DIR_SAMPLE_NAME,
                                    DIR_VALID_NAME)
    sample_train_dir = os.path.join(DATASET_PATH, DIR_SAMPLE_NAME,
                                    DIR_TRAIN_NAME)
    sample_test_dir = os.path.join(DATASET_PATH, DIR_SAMPLE_NAME, DIR_TEST_NAME)
    sample_results_dir = os.path.join(DATASET_PATH, DIR_SAMPLE_NAME,
                                      DIR_RESULTS_NAME)

    if not os.path.isdir(valid_dir):
        os.mkdir(valid_dir)

    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)

    if not os.path.isdir(sample_dir):
        os.mkdir(sample_dir)

    if not os.path.isdir(sample_valid_dir):
        os.mkdir(sample_valid_dir)

    if not os.path.isdir(sample_train_dir):
        os.mkdir(sample_train_dir)

    if not os.path.isdir(sample_test_dir):
        os.mkdir(sample_test_dir)

    if not os.path.isdir(sample_results_dir):
        os.mkdir(sample_results_dir)

    # Move random files from the train folder into the valid folder
    _img_transfer(train_dir, valid_dir, VALIDATION_SIZE, move=True)

    # Copy random files from the train folder into the sample/train folder
    _img_transfer(train_dir, sample_train_dir, SAMPLE_SIZE)

    # Copy random files from the valid folder into the sample/valid folder
    _img_transfer(valid_dir, sample_valid_dir, SAMPLE_VALIDATION_SIZE)

    # Create category subdirectories where required
    _group_categories(sample_train_dir)
    _group_categories(sample_valid_dir)
    _group_categories(valid_dir)
    _group_categories(train_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reset', action='store_true',
                        help="Reset your data folder structure")
    args = parser.parse_args()

    if args.reset:
        reset()
    else:
        main()
