import asyncio
import networkx as nx
from datasets import load_dataset
from typing import Iterable, Dict, List, Set, Tuple, Any, AsyncGenerator

GLOBAL_GRAPH = nx.Graph()
GLOBAL_GRAPH_LOCK = asyncio.Lock()

def stream_huggingface_etymology_data(hf_dataset):
    dataset_stream = load_dataset(hf_dataset, split="train", streaming=True)
    for line in dataset_stream:
        yield line
        
async def group_records_by_term_id(data_stream):
    current_term_id: str | None = None
    current_group_records: List[Dict[str, Any]] = []
    for record in data_stream:
        record_term_id = record['term_id']
        if current_term_id is None:
            current_term_id = record_term_id
            current_group_records.append(record)
        elif record_term_id == current_term_id:
            current_group_records.append(record)
        else:
            yield (current_term_id, current_group_records)
            current_term_id = record_term_id
            current_group_records = [record]

    if current_group_records:
        yield (current_term_id, current_group_records)


def _extract_nodes_and_edges_from_records(records,internal_reltypes):
    nodes_to_add ={} 
    edges_to_add = [] 

    for record in records:
        source_id = record.get('term_id')
        target_id = record.get('related_term_id')
        rel_type = record.get('reltype')

        if source_id:
            current_attrs = nodes_to_add.get(source_id, {})
            current_attrs.update({
                'label': record.get('term', source_id),
                'lang': record.get('lang')
            })
            nodes_to_add[source_id] = {k: v for k, v in current_attrs.items() if v is not None}

        if target_id:
            current_attrs = nodes_to_add.get(target_id, {})
            current_attrs.update({
                'label': record.get('related_term', target_id),
                'lang': record.get('related_lang')
            })
            nodes_to_add[target_id] = {k: v for k, v in current_attrs.items() if v is not None}
        
        if source_id and target_id and rel_type and rel_type not in internal_reltypes:
            edge_attrs = {
                'reltype': rel_type,
                'position': record.get('position'),
                'group_tag': record.get('group_tag'),
                'parent_tag': record.get('parent_tag'),
                'parent_position': record.get('parent_position')
            }

            cleaned_edge_attrs = {}
            for k, v in edge_attrs.items():
                if v is None:
                    continue
                if isinstance(v, str):
                    stripped_v = v.strip()
                    if stripped_v == '':
                        continue
                    cleaned_edge_attrs[k] = stripped_v
                else:
                    cleaned_edge_attrs[k] = v
            edges_to_add.append((source_id, target_id, cleaned_edge_attrs))

    final_nodes = [(node_id, attrs) for node_id, attrs in nodes_to_add.items()]

    return final_nodes, edges_to_add

def _add_main_term_node(subgraph, group_term_id,records): 
    main_term_record = None
    for r in records:
        if r.get('term_id') == group_term_id and not r.get('related_term_id'):
            main_term_record = r
            break
    if not main_term_record and records:
        main_term_record = records[0]

    if main_term_record:
        subgraph.add_node(group_term_id, 
                           label=main_term_record.get('term', group_term_id), 
                           lang=main_term_record.get('lang'))
    else:
        subgraph.add_node(group_term_id, label=group_term_id, lang=None)

async def create_networkx_subgraph(grouped_data):
    group_term_id, records = grouped_data
    subgraph = nx.DiGraph() 
    internal_reltypes = {'group_derived_root', 'group_affix_root', 'internal_grouping_tag'}
    _add_main_term_node(subgraph, group_term_id, records)
    nodes_to_add, edges_to_add = _extract_nodes_and_edges_from_records(records, internal_reltypes)
    subgraph.add_nodes_from(nodes_to_add)
    subgraph.add_edges_from(edges_to_add)

    yield subgraph

async def merge_into_global_graph(subgraph: nx.DiGraph):
    async with GLOBAL_GRAPH_LOCK:
        GLOBAL_GRAPH.add_nodes_from(subgraph.nodes(data=True))
        GLOBAL_GRAPH.add_edges_from(subgraph.edges(data=True))
