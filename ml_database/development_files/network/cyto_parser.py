# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:45:58 2022

@author: weixiong001
"""

import py4cytoscape as py4
dir(py4)
py4.cytoscape_ping()
py4.cytoscape_version_info()

py4.import_network_from_file("overall2.cyjs")
py4.select_nodes('go_GO:0009808', 'shared name')
py4.get_selected_nodes()
subnetwork = py4.select_first_neighbors()
#py4.networks.export_network('./output/go_GO_0033014','cyjs', subnetwork)
