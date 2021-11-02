#!/usr/bin/env python3


import sys
from xm_file import XmFile


def main():
    file_in_1 = sys.argv[1]
    file_in_2 = sys.argv[2]
    file_out = sys.argv[3]

    xm_file_1 = XmFile()
    xm_file_1.from_file(file_in_1)
    xm_file_2 = XmFile()
    xm_file_2.from_file(file_in_2)

    xm_file_1.remove_empty_instruments()
    xm_file_1.rename_instruments_by_index()
    xm_file_2.remove_empty_instruments()
    xm_file_2.rename_instruments_by_index()
    xm_file_1.append(xm_file_2)

    xm_file_1.to_file(file_out)


if __name__ == "__main__":
    main()
