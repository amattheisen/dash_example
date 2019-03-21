"""
Consume a file of sections - create a pandas dataframe for each section.

Note: this does not handle nested sections.

"""
import pandas as pd

def parse_data(filename="data.txt", verbose=True):
    data = {}
    with open(filename, 'r') as fd:
        section = None
        for line in fd:
            line = line.strip()
            if not line or line[0] == "#":
                # strip off blanks and comments
                continue
            if line[0] == "<" and line[-1] == ">":
                if line[1] == '/':
                    # found end of section
                    section = None
                else:
                    # found start of section
                    # (overrides prior duplicate section)
                    section = line[1:-1]
                    data[section] = []
                continue
            if not section:
                continue
            data[section].append(line.split(','))
    
    pd_data = {}
    for section in data:
        pd_data[section] = pd.DataFrame(data[section][1:], columns=data[section][0])
        if verbose:
            print('**', section, '**\n', pd_data[section], '\n')
    return pd_data

if __name__ == '__main__':
    parse_data()
