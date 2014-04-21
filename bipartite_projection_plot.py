# This script creates bipartite plots and stats (mostly with Colombian sellers as nodes)

import igraph as ig
import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt

def load_dat():
    graph = ig.read('igraph_small.csv',format='edge')
    vals = pd.read_csv('vals_small.csv')[' val']
    return graph, vals

def make_projection(graph, vals):
    """ makes bipartite projections, returns seller projection"""

    # PREPARE ATTRIBUTE (FOB SHIPMENT VALUE)
    graph.es['val'] = list(vals)
    graph.vs['val'] = graph.strength(range(len(graph.vs)), weights='val')
    
    # SIZES FROM graph.csv
    size =12689
    edge_size = 75384
    big_size = 47231
    sub = size
    
    # MAKE THE TWO TYPES (SELLER AND BUYER)
    graph.vs['type'] = [1] * big_size
    graph.vs[sub:]['type'] = [0] * (big_size - sub)

    # PROEJECT AND ADD ATTRIBUTES
    proj2, proj1 = graph.bipartite_projection()
    proj1.vs['val'] = graph.vs[0:sub]['val']
    
    # WRITE AND READ
    proj1.write_pickle('proj1.pickle')
    proj1 = ig.read('proj1.pickle')
    print ig.summary(proj1)

    return proj1, proj2


def get_comps(proj1):
    """ finds components and component statistics"""

    totval = sum(proj1.vs['val'])
    clust = proj1.clusters()
    lcc = clust.giant()
    giantval = sum(lcc.vs['val'])

    print "".join(['Average path length: ', str(proj1.diameter())])
    print "".join(['Average path length: ', str(proj1.average_path_length())])
    print "".join(['Seller count: ', str(proj1.vcount())])
    print "".join(['Total value, FOB dollars: ', str(totval)])
    print "".join(['Percent value in giant component: ',
                    str(giantval / float(totval))])
    return clust, lcc, totval, giantval


def csize(clust):
    """ calculate component sizes and print counts"""

    # GET COMPONENT SIZES
    cv_size = []
    for k in range(len(clust)):
        verts = clust.subgraph(k).vcount()
        cv_size.append(verts)
    
    # PRINT HISTOGRAM
    print "COMPONENT SIZE HISTOGRAM"
    print ''
    for k in range(27):
        print "".join([str(k), ',', str(cv_size.count(k))])
    print ''
    
    # Confirm 2nd largest component size
    print "".join(['Largest component size: ',
        str(sorted(cv_size)[-1])])
    print "".join(['2nd largest component size: ',
        str(sorted(cv_size)[-2])])

    return 0

def plot_comp(comp, fname, layout):
    """ plot component """

    size = len(comp.vs)
    edge_size = len(comp.es)
    comp.vs['label'] = [''] * size
    comp.vs['size']  = [1] * size
    comp.vs['label_size']  = [0] * size
    comp.es['arrow_size']  = [0] * edge_size
    comp.es['width']  = [0.1] * edge_size
    layout = comp.layout(layout)
    ig.plot(comp, fname,
            layout = layout)
    return 0

def pl_hist(g):
    """creaate and save path length histogram to disk""" 

    #OPEN FILE FOR WRITING
    f = open('pl_hist.txt','w')  

    #CREATE PATH LENGTH HISTOGRAM  
    h = g.path_length_hist() 

    f.write(h.to_string(show_bars=False))

    return 0

def bc_hist(g, name):
    """create and save betweenness centrality histogram to disk""" 

    #GET BETWEENNESS LIST 
    bl = g.betweenness() 

    #GET DEGREE LIST 
    dl = g.degree()
    
    #CREATE SERIES
    bs = pd.Series(bl)
    ds = pd.Series(dl)

    #PRINT BETWEENNESS AND DEGREE
    bs.to_csv('bs_' + name + '.csv')
    ds.to_csv('ds_' + name + '.csv')

    #SCATTER
    #plt.scatter(ds,bs)
    #plt.show()

    return 0

if __name__ == "__main__":
    """ runs all the functions """

    # LOAD DATA
    graph, vals = load_dat()    

    # SET ATTRIBUTES
    proj1, proj2 = make_projection(graph, vals)

    
    # GET COMPONENTS AND VAL INFO
    clust, lcc, totval, giantval = get_comps(proj1)
    
    # PRINT COMPONENT SIZE COUNTS
    csize(clust)

    # GET PATH LENGTH HISTOGRAM
    pl_hist(proj1)

    # GET NODE BY NODE BETWEENNESS CENTRALITY HISTOGRAM
    bc_hist(proj1, 'expexp')
    #bc_hist(proj2, 'impimp')

    # PLOT LARGEST COMPONENT
    plot_comp(lcc, 'largest_component_drl.png', 'drl')
    plot_comp(lcc, 'largest_component_lgl.png', 'lgl')
