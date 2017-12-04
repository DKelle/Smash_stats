import shared_data

def interact():
    while True:
        a = input()
        runners = [interaction(a, 'rank', shared_data.get_rank_data),
                interaction(a, 'valid', shared_data.get_valid_range),
                interaction(a, 'data', shared_data.get_dated_data),
                interaction(a, 'win', shared_data.get_win_loss_data),
                interaction(a, 'html', shared_data.get_html)]


        for runner in runners:
            runner.run()

class interaction(object):
    def __init__(self, query, keyword, data_source):
        self.query = query
        self.keyword = keyword
        self.data_source = data_source

    def run(self):
        if self.keyword in self.query:
            b = self.query.split()
            data = self.data_source()
            if len(b) > 1:
                if b[-1] in data:
                    print(data[b[-1]])
                else:
                    print('key not in')

            else:
                print(data)


