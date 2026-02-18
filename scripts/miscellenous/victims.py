import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.utils import create_victims_df
from utils.victims import create_separate_victims_tuple


def main():
    data = create_victims_df()
    data = create_separate_victims_tuple(data)

    print('finish')

main()