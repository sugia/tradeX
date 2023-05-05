if __name__ == '__main__':
    buybacks = []
    for year in range(2013, 2024):
        with open('./data/stock_buybacks/{}.txt'.format(year), 'r') as f:
            next(f)
            content = f.read().split('\n')
            vec = []
            for line in content:
                if not line:
                    continue
                if 'stock' in line:
                    buybacks.append(vec)
                    vec = [line, year]
                else:
                    vec.append(line)
            buybacks.append(vec)
    buybacks.sort()
    for row in buybacks:
        print(row)
        

