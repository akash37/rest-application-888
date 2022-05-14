def find_internal_nodes_num(tree):
    if len(tree) == 1:
        return 0

    unique = set()
    for i in tree:
        if i != -1:
            unique.add(i)

    if len(unique) == 0:
        return 0

    return len(unique) - 1


my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num(my_tree))
