import asyncio
import networkx as nx
from pyper import task
from pipeline_steps import (
    stream_huggingface_etymology_data,
    group_records_by_term_id,
    create_networkx_subgraph,
    merge_into_global_graph,
    GLOBAL_GRAPH
)

HF_DATASET="Nickmancol/mini_etymology"

async def main():
    pipeline = task(stream_huggingface_etymology_data) \
    | task(group_records_by_term_id, branch=True) \
    | task(create_networkx_subgraph, branch=True) \
    | task(merge_into_global_graph)
    async for _ in pipeline(HF_DATASET):
        pass

if __name__ == "__main__":
    asyncio.run(main())
    print("\n✅ Pipeline run finished. Summary of the global graph:")
    print(f"🔹 Nodes: {GLOBAL_GRAPH.number_of_nodes()}")
    print(f"🔸 Edges: {GLOBAL_GRAPH.number_of_edges()}")
    wccs = list(nx.connected_components(GLOBAL_GRAPH))
    largest_wcc_nodes = max(wccs, key=len)
    S = GLOBAL_GRAPH.subgraph(largest_wcc_nodes)
    print(f"Largest subgraph: {S.number_of_nodes()} nodes")
    print(f"Largest subgraph: {S.number_of_edges()} edges")
    nx.write_gexf(GLOBAL_GRAPH, "etymology_global_graph.gexf")
    nx.write_gexf(S, "largest_subgraph.gexf")
