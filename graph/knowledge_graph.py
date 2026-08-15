from pathlib import Path
import webbrowser

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


def get_cluster_color(cluster):
    if not cluster:
        return OTHER_COLOR

    try:
        cluster_number = int(cluster[1:])
    except (ValueError, IndexError):
        return OTHER_COLOR

    if 1 <= cluster_number <= len(CLUSTER_COLORS):
        return CLUSTER_COLORS[cluster_number - 1]

    return OTHER_COLOR


def visualize(risks, mitigations, relationships):
    # ---------------------------------------------------------
    # 1. Collect valid nodes
    # ---------------------------------------------------------
    risk_ids = {risk.risk_id for risk in risks}
    mitigation_ids = {mitigation.mitigation_id for mitigation in mitigations}
    node_ids = risk_ids | mitigation_ids

    # ---------------------------------------------------------
    # 2. Create PyVis graph
    #    Cluster information is read directly from the objects.
    #    No clustering is recalculated here.
    # ---------------------------------------------------------
    graph = Network(
        height="900px",
        width="100%",
        directed=True,
    )

    for risk in risks:
        cluster = risk.cluster

        graph.add_node(
            risk.risk_id,
            label=risk.risk_id,
            title=f"{risk.risk_name}<br>Cluster {cluster or 'Unknown'}",
            color=get_cluster_color(cluster),
            shape="dot",
        )

    for mitigation in mitigations:
        cluster = mitigation.cluster

        graph.add_node(
            mitigation.mitigation_id,
            label=mitigation.mitigation_id,
            title=f"{mitigation.mitigation_name}<br>Cluster {cluster or 'Unknown'}",
            color=get_cluster_color(cluster),
            shape="box",
        )

    # ---------------------------------------------------------
    # 3. Add relationships as graph edges
    # ---------------------------------------------------------
    connected_ids = set()

    for relationship in relationships:
        source = clean_id(relationship.source_id)
        target = clean_id(relationship.target_id)

        if source in node_ids and target in node_ids:
            graph.add_edge(
                source,
                target,
                label=relationship.relationship_type,
                title=relationship.reasoning_notes,
            )
            connected_ids.add(source)
            connected_ids.add(target)

    # ---------------------------------------------------------
    # 4. Print simple graph statistics
    # ---------------------------------------------------------
    cluster_counts = {}

    for risk in risks:
        if risk.cluster:
            cluster_counts[risk.cluster] = cluster_counts.get(risk.cluster, 0) + 1

    for mitigation in mitigations:
        if mitigation.cluster:
            cluster_counts[mitigation.cluster] = cluster_counts.get(mitigation.cluster, 0) + 1

    sorted_cluster_sizes = sorted(cluster_counts.values(), reverse=True)

    print("Clusters found:", len(cluster_counts))
    print("Largest clusters:", sorted_cluster_sizes[:15])
    print("Nodes without relationships:", len(node_ids - connected_ids))

    # ---------------------------------------------------------
    # 5. Write and open HTML graph
    # ---------------------------------------------------------
    output_file = Path("graph/knowledge_graph.html").resolve()

    graph.write_html(
        str(output_file),
        open_browser=False,
    )

    webbrowser.open(output_file.as_uri())