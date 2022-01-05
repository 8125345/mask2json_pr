'''
@lanhuage: python
@Descripttion: check json
@version: beta
'''

def rm(filepath):
    p = open(filepath, 'r+')

    lines = p.readlines()

    d = ""
    for line in lines:
        c = line.replace('"group_id": "null",', '"group_id": null,')
        d += c

    p.seek(0)
    p.truncate()
    p.write(d)
    p.close()