import networkx as nx
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['figure.figsize']=(10,8) #用来控制长宽比
matplotlib.use('agg')


def create_graphy(topic,pool,result):
    plt.figure()
    relations=[]
    list=result.split('\'')
    i=0
    while i+6<len(list):
        temp=[list[i+1],list[i+3],list[i+5]]
        relations.append(temp)
        i+=6
    # 创建一个有向图
    G = nx.DiGraph()
    step=0
    num=1
    # 添加节点
    for parent in pool:
        G.add_node(parent[0],level=num)
        num=num+step
        step=1-step
        for i in range(len(parent[1])):
            if(parent[1][i]!=parent[0]):
                G.add_node(parent[1][i],level=0)
                G.add_edge(parent[0], parent[1][i], edge_type='child')

    # 添加边
    for relation in relations:
        G.add_edge(relation[0], relation[2], edge_type='parent')

    # 设置绘图布局
    # pos = nx.multipartite_layout(G, subset_key='level')
    pos = nx.kamada_kawai_layout(G)

    # 绘制节点
    node_sizes = [500*(G.nodes[n]['level']==0)+1000*(G.nodes[n]['level']!=0) for n in G.nodes()]
    node_colors = ['lightblue' if G.nodes[n]['level'] == 0 else 'lightgreen'for n in G.nodes()]  # 设置节点颜色
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)

    # 绘制父节点边
    parent_edges = [(u, v) for u, v, attrs in G.edges(data=True) if attrs['edge_type'] == 'parent']
    nx.draw_networkx_edges(G, pos, edgelist=parent_edges, arrowstyle='->', arrowsize=50, width=5,edge_color='gray')

    # 绘制子节点边
    child_edges = [(u, v) for u, v, attrs in G.edges(data=True) if attrs['edge_type'] == 'child']
    nx.draw_networkx_edges(G, pos, edgelist=child_edges, arrowstyle='-', arrowsize=15, width=1,edge_color='blue')

    # 绘制标签
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')

    # 显示图形
    patch1 = mpatches.Patch(color='gray', label='A->B，表示A为B的先修知识', linewidth=5.0,linestyle='-',)
    patch2 = mpatches.Patch(color='blue', label='子主题，表示蓝色的主题为相连的绿色主题的子主题', linewidth=1.0,linestyle='-',)
    plt.legend(handles=[patch1, patch2], loc = 'best')
    plt.title(topic, fontsize = 16)
    plt.axis('off')
    plt.savefig('temp.jpeg', dpi=300)

if __name__ == "__main__":
    pool= [['数组', []], ['链表', []], ['栈', []], ['队列', []], ['树', []], ['图', []], ['算法设计', ['简单算法', '高级算法']]]
    relations="relations = Relations([Triple(Knowledge('数组'), Rel('Precursor'),Knowledge('链表')),\n                       Triple(Knowledge('链表'), Rel('Precursor'),Knowledge('栈')),\n                       Triple(Knowledge('栈'), Rel('Precursor'),Knowledge('队列')),\n                       Triple(Knowledge('队列'), Rel('Precursor'),Knowledge('树')),\n                       Triple(Knowledge('树'), Rel('Precursor'),Knowledge('图')),\n                       Triple(Knowledge('图'), Rel('Precursor'),Knowledge('算法设计')),])"
    create_graphy("学习数据结构", pool, relations)
    pool= [['数组', []], ['链表', []], ['栈', []], ['队列', []], ['树', []], ['图', []], ['算法设计', []]]
    create_graphy("学习数据结构", pool, relations)