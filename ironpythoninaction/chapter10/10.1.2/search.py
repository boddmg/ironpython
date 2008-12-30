from argparse import ArgumentParser
from configobj import ConfigObj
import fnmatch
import os

def walk(directory, exclude_dirs):
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            if entry in exclude_dirs:
                continue
            
            for member in walk(path, exclude_dirs):
                yield member
                

def search(exclude_dirs, paths, inc_pattern, exc_pattern):
    if not paths:
        paths = ['.']
    for path in paths: 
        for file_path in walk(path, exclude_dirs):
            base_path, filename = os.path.split(file_path)
            if fnmatch.fnmatch(filename, inc_pattern): 
                if (not exc_pattern or 
                    not fnmatch.fnmatch(filename, exc_pattern)): 
                    print file_path

 
def GetExcludesFromConfig():
    home = os.path.join(os.getenv('HOMEDRIVE'),
                        os.getenv('HOMEPATH'))

    rcfile = os.path.join(home, 'search.ini')
    config = ConfigObj(rcfile)
    exclude_dirs = config.get('exclude', [])
    if not isinstance(exclude_dirs, list):
        exclude_dirs = [exclude_dirs]
    
    return exclude_dirs


def ParseArgs():
    parser = ArgumentParser(description="Search paths for files.")
    parser.add_argument('-p', '--path',
                        action='append', dest='paths', 
                        default=[],
                        metavar='path',
                        help='paths to search', 
                       )
    parser.add_argument('-i', '--include',
                        action='store', dest='inc_patt', 
                        default='*', 
                        help='file name pattern to include', 
                       )
    parser.add_argument('-x', '--exclude',
                        action='store', dest='exc_patt', 
                        default=None, 
                        help='file name pattern to exclude', 
                       )
    return parser.parse_args()


if __name__ == '__main__':
    exclude_dirs = GetExcludesFromConfig()
    args = ParseArgs()
    
    search(exclude_dirs, args.paths, args.inc_patt, args.exc_patt)
        