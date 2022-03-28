import collections

l = collections.defaultdict(set)
l[1].add(1)
l[1].add(2)
l[1].add(3)
l[2].add(1)
l[2].add(2)
l[2].add(3)
print(l)