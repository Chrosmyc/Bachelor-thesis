from pathlib import Path
import webbrowser

from pyvis.network import Network


def clean_id(value):
    if not value:
        return ""

    return value.split()[0]


def visualize(risks, mitigations, relationships):
    graph = Network(
        height="900px",
        width="100%",
        directed=True,
    )

    node_ids = set()
    connected_ids = set()
    added = 0
    skipped = 0

    for risk in risks:
        graph.add_node(
            risk.risk_id,
            label=risk.risk_id,
            title=risk.risk_name,
            color="red",
        )
        node_ids.add(risk.risk_id)

    for mitigation in mitigations:
        graph.add_node(
            mitigation.mitigation_id,
            label=mitigation.mitigation_id,
            title=mitigation.mitigation_name,
            color="green",
        )
        node_ids.add(mitigation.mitigation_id)

    for relationship in relationships:
        source = clean_id(relationship.source_id)
        target = clean_id(relationship.target_id)

        if source not in node_ids or target not in node_ids:
            print(
                f"Skipped {relationship.relationship_id}: "
                f"{source!r} -> {target!r}"
            )
            skipped += 1
            continue

        graph.add_edge(
            source,
            target,
            label=relationship.relationship_type,
            title=relationship.reasoning_notes,
        )

        connected_ids.add(source)
        connected_ids.add(target)
        added += 1

    print("Relationships loaded:", len(relationships))
    print("Relationships added:", added)
    print("Relationships skipped:", skipped)
    print("Nodes without relationships:", len(node_ids - connected_ids))

    output_file = Path(
        "graph/knowledge_graph.html"
    ).resolve()

    graph.write_html(
        str(output_file),
        open_browser=False,
    )

    webbrowser.open(output_file.as_uri())