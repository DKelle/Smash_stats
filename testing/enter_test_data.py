import json

res = {}
tag = '.'
while tag != '':
    tag = raw_input('enter tag: ')
    res[tag] = []
    wins = raw_input('enter players {} beat on single line, no spaces: '.format(tag))
    for op in wins:
        res[tag].append(op)

print json.dumps(res)
