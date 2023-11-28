



def test(data):
    result = set()
    result.update(data.split(','))
    return ','.join(x for x in result if x)


data = 'a,b,c,a,f,c'
print(test(data))