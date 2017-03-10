class DomainTree:
    def __init__(self,  domain_list):
        self._root = {}
        self._domain_set = set([tuple(reversed(d.split('.'))) for d in domain_list])

        for domain in domain_list:
            parts = domain.split('.')
            parts.reverse()
            tmp = self._root
            for p in parts:
                if p not in tmp:
                    tmp[p] = {}
                tmp = tmp[p]

        self._cache = {}

    def find_max_match(self, domain):
        tmp = self._root
        matched = []

        if domain in self._cache:
            return self._cache[domain]

        parts = domain.split('.')
        for idx in xrange(len(parts)-1, -1, -1):
            p = parts[idx]
            if p in tmp:
                tmp = tmp[p]
                matched.append(p)
            else:
                break

        self._cache[domain] = tuple(matched) if tuple(matched) in self._domain_set else None
        return self._cache[domain]

    def cache_count(self):
        return len(self._cache)


def test():
    tree = DomainTree(['b.com', 'a.com', 'www.a.com'])

    print tree.find_max_match('c.com')

    print tree.find_max_match('b.com')
    print tree.find_max_match('www.b.com')

    print tree.find_max_match('xxx.a.com')
    print tree.find_max_match('xxx.www.a.com')


if __name__ == '__main__':
    test()
