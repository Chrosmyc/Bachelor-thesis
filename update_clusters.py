from pathlib import Path
import re

import networkx as nx

from parser.load_all import (
    load_all_risks,
    load_all_mitigations,
    load_all_relationships,
)


BASE_DIR = Path(__file__).resolve().parent
RISK_FOLDER = BASE_DIR / "data" / "risks"
MITIGATION_FOLDER = BASE_DIR / "data" / "mitigations"
RELATIONSHIP_FOLDER = BASE_DIR / "data" / "relationships"


def clean_id(value):
    if not value:
        return ""
    return value.split()[0]


def calculate_clusters(risks, mitigations, relationships):
    graph = nx.Graph()

    risk_ids = {risk.risk_id for risk in risks}
    mitigation_ids = {mitigation.mitigation_id for mitigation in mitigations}
    node_ids = risk_ids | mitigation_ids

    # Wichtig: stabile Reihenfolge der Nodes
    graph.add_nodes_from(sorted(node_ids))

    # Beziehungen zuerst sammeln
    edges = []

    for relationship in relationships:
        source = clean_id(relationship.source_id)
        target = clean_id(relationship.target_id)

        if source in node_ids and target in node_ids:
            # Auch innerhalb einer Edge stabile Reihenfolge
            edge = tuple(sorted((source, target)))
            edges.append(edge)

    # Wichtig: stabile Reihenfolge der Edges
    graph.add_edges_from(sorted(set(edges)))

    communities = list(
        nx.community.louvain_communities(
            graph,
            seed=42,
        )
    )

    # Größtes Cluster zuerst.
    # Bei gleicher Größe entscheidet die alphabetische Node-Reihenfolge.
    communities.sort(
        key=lambda community: (
            -len(community),
            tuple(sorted(community)),
        )
    )

    node_to_cluster = {}

    for index, community in enumerate(communities, start=1):
        cluster_id = f"C{index:02d}"

        for node_id in community:
            node_to_cluster[node_id] = cluster_id

    return node_to_cluster


def update_markdowns(folder, node_to_cluster):
    changed = 0

    for file_path in sorted(folder.glob("*.md")):
        node_id = file_path.stem
        new_cluster = node_to_cluster.get(node_id)

        if not new_cluster:
            continue

        content = file_path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^cluster:\s*(.*)$", content)

        if not match:
            print(f"Skipped {node_id}: no cluster field found")
            continue

        old_cluster = match.group(1).strip()

        if old_cluster == new_cluster:
            continue

        updated_content = re.sub(
            r"(?m)^cluster:.*$",
            f"cluster: {new_cluster}",
            content,
            count=1,
        )

        file_path.write_text(updated_content, encoding="utf-8")
        print(f"{node_id}: {old_cluster or '<empty>'} -> {new_cluster}")
        changed += 1

    return changed


def main():
    risks = load_all_risks(RISK_FOLDER)
    mitigations = load_all_mitigations(MITIGATION_FOLDER)
    relationships = load_all_relationships(RELATIONSHIP_FOLDER)

    node_to_cluster = calculate_clusters(
        risks,
        mitigations,
        relationships,
    )

    changed_risks = update_markdowns(RISK_FOLDER, node_to_cluster)
    changed_mitigations = update_markdowns(MITIGATION_FOLDER, node_to_cluster)

    print(f"\nUpdated files: {changed_risks + changed_mitigations}")


if __name__ == "__main__":
    main()
