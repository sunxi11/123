import sys
sys.path.append('..')
from topo import *

sorted_topo = [_[0] for _ in sorted(topo_node_cnt.items(), key=lambda x:x[1])]

def GetAllPath(network, node_cnt, cur, target):
    all_path = set()
    visited = set()
    mymap = [[] for _ in range(node_cnt)]
    for k in network.keys():
        src = k[0]
        des = k[1]
        mymap[src].append(des)
        mymap[des].append(src)

    #     print(mymap)

    def dfs(mmap, cur, target, cur_path):
        if len(cur_path) > 5:
            return
        if cur == target:
            cur_path.append(cur)
            #             all_path.append(cur_path[:])
            all_path.add(' '.join([str(i) for i in cur_path]))
            cur_path.pop()
            return

        cur_path.append(cur)  # 这一段用于从一条路遍历到底
        visited.add(cur)  #
        for node in mymap[cur]:  #
            if node not in visited:  #
                dfs(mmap, node, target, cur_path)  #
        visited.remove(cur)
        cur_path.remove(cur)
        return

    dfs(mmap=mymap, cur=cur, target=target, cur_path=[])
    all_path = sorted(list(all_path))
    r2 = []
    for i in sorted(all_path):
        r2.append(list(map(int, i.split())))

    return r2

def build_link_map(substrate_network, substrate_node_cnt):
    link_map = [[0 for _ in range(substrate_node_cnt)] for _ in range(substrate_node_cnt)]
    for k in substrate_network.keys():
        src = k[0]
        des = k[1]
        link_map[src][des] = 1
        link_map[des][src] = 1
    return link_map


def add_single_link(link, network, node_cnt, src, des):
    # link_map = build_link_map(network, node_cnt)
    pre_keys = network.keys()
    pre_res = GetAllPath(network, node_cnt, src, des)
    if (link in pre_keys) or ((link[1], link[0]) in pre_keys):
        print(f'链接{link[0]}->{link[1]}已经存在！！！')
        return network, pre_res
    new_net = network.copy()
    new_net[link] = 0
    res = GetAllPath(new_net, node_cnt, src, des)

    print(f'新增链路 {link[0]}->{link[1]} 后 {src} 到 {des} 的链路增加了 {len(res) - len(pre_res)} 条')

    return new_net, res



def get_add_link(pre_res, res):
    pre_res = sorted(pre_res)
    res = sorted(res)
    add_link = res.copy()
    for i in res:
        if i in pre_res:
            add_link.remove(i)
    return add_link



if __name__ == '__main__':
    topo_name = sorted_topo[0]
    substrate_network = eval(topo_name)
    substrate_node_cnt = topo_node_cnt[topo_name]
    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            new_net, res = add_single_link((i, j), substrate_network, substrate_node_cnt, 0, 1)