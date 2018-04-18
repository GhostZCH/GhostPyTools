import os
import argparse


def count(path, type_list):
    print path, type_list

    line_count = 0
    for base, _, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[-1][1:] not in type_list:
                continue

            file_name = os.path.join(base, f)

            with open(file_name) as fd:
                file_count = len(fd.readlines())
                line_count += file_count
                print "%-50s: %10d" % (f, file_count)

    return line_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default='./')
    parser.add_argument("--type", default='c,h')
    args = parser.parse_args()

    total = count(args.path, args.type.split(','))
    print "%-50s: %10d" % ("total", total)
