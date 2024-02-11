import re
import os
import sys
import graphviz
import hashlib

def smd5(s):
    return hashlib.md5(s.encode()).hexdigest()

if __name__ == "__main__":
    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: file {input_file} not found")
        exit(-1)
    with open(input_file, 'r') as f:
        source_code = f.read()
    source_code = re.sub(re.compile(";.*?\n" ), "\n", source_code) # remove all comments
    labels = [{'name': x.group()[:-1], 'start': x.start(), 'end': x.end()} for x in re.finditer(r'^\w+:', source_code, re.MULTILINE)] + [{'start': len(source_code) - 1, 'end': len(source_code) - 1}]
    
    for i in range(len(labels) - 1):
        labels[i]['code'] = source_code[labels[i]['end'] : labels[i + 1]['start']]

    g = graphviz.Digraph(filename = input_file + '_graph.dot', encoding='utf-8', graph_attr={'rankdir':'LR'})

    for l in labels[:-1]:
        g.node(smd5(l['name']), l['name'])
        for l2 in labels[:-1]:
            if ' ' + l2['name'] + '\n' in l['code']:
                g.edge(smd5(l['name']), smd5(l2['name']))

    g.render()

