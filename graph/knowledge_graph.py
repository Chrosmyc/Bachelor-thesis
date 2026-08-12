from pathlib import Path
import webbrowser

import networkx as nx
from pyvis.network import Network


# 15 clearly distinguishable cluster colors.
# Smaller clusters after the 15 largest are shown in grey.
CLUSTER_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
]
OTHER_COLOR = "#c7c7c7"


def clean_id(value):
    if not value:
        return ""
    return value.split()[0]


def visualize(risks, mitigations, relationships):
    # ---------------------------------------------------------
    # 1. Build an undirected NetworkX graph only for clustering
    # ---------------------------------------------------------
    nx_graph = nx.Graph()

    risk_ids = {risk.risk_id for risk in risks}
    mitigation_ids = {m.mitigation_id for m in mitigations}
    node_ids = risk_ids | mitigation_ids

    nx_graph.add_nodes_from(node_ids)

    valid_relationships = []

    for relationship in relationships:
        source = clean_id(relationship.source_id)
        target = clean_id(relationship.target_id)

        if source in node_ids and target in node_ids:
            nx_graph.add_edge(source, target)
            valid_relationships.append((relationship, source, target))

    # ---------------------------------------------------------
    # 2. Recalculate clusters with Louvain
    # ---------------------------------------------------------
    communities = list(
        nx.community.louvain_communities(
            nx_graph,
            seed=42,
        )
    )

    # Largest cluster = C01, second largest = C02, ...
    communities.sort(key=len, reverse=True)

    node_to_cluster = {}
    cluster_to_color = {}

    for index, community in enumerate(communities, start=1):
        cluster_id = index
        color = (
            CLUSTER_COLORS[index - 1]
            if index <= len(CLUSTER_COLORS)
            else OTHER_COLOR
        )

        cluster_to_color[cluster_id] = color

        for node_id in community:
            node_to_cluster[node_id] = cluster_id

    # ---------------------------------------------------------
    # 3. Create PyVis graph
    #    Color = cluster
    #    Shape = Risk/Mitigation
    # ---------------------------------------------------------
    graph = Network(
        height="900px",
        width="100%",
        directed=True,
    )

    connected_ids = set()

    for risk in risks:
        cluster = node_to_cluster.get(risk.risk_id)
        graph.add_node(
            risk.risk_id,
            label=risk.risk_id,
            title=f"{risk.risk_name}<br>Cluster C{cluster:02d}",
            color=cluster_to_color.get(cluster, OTHER_COLOR),
            shape="dot",
        )

    for mitigation in mitigations:
        cluster = node_to_cluster.get(mitigation.mitigation_id)
        graph.add_node(
            mitigation.mitigation_id,
            label=mitigation.mitigation_id,
            title=f"{mitigation.mitigation_name}<br>Cluster C{cluster:02d}",
            color=cluster_to_color.get(cluster, OTHER_COLOR),
            shape="box",
        )

    for relationship, source, target in valid_relationships:
        graph.add_edge(
            source,
            target,
            label=relationship.relationship_type,
            title=relationship.reasoning_notes,
        )
        connected_ids.add(source)
        connected_ids.add(target)

    print("Clusters found:", len(communities))
    print("Largest clusters:", [len(c) for c in communities[:15]])
    print("Nodes without relationships:", len(node_ids - connected_ids))

    output_file = Path("graph/knowledge_graph.html").resolve()

    graph.write_html(
        str(output_file),
        open_browser=False,
    )

    webbrowser.open(output_file.as_uri())
