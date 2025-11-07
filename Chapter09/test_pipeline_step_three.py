import pytest
import asyncio
import networkx as nx
from typing import List, Dict, Any, Tuple
from pipeline_steps import create_networkx_subgraph # Asegúrate de que las auxiliares estén en pipeline_steps.py

@pytest.mark.asyncio
async def test_create_networkx_subgraph_with_real_fixed_data():
    test_term_id = "JN6Uml0yVsW5IXZMLr94gg"
    fixed_records_from_dataset = [
        {
            'term_id': 'JN6Uml0yVsW5IXZMLr94gg', 'lang': 'Latin', 'term': 'encyclopaedia', 
            'reltype': 'borrowed_from', 'related_term_id': 'cAiYCdUVXxe7CzwKH3rR1g', 'related_lang': 'Ancient Greek', 'related_term': 'ἐγκυκλοπαιδεία',
            'position': '0', 'group_tag': '', 'parent_tag': '', 'parent_position': ''
        },
        {
            'term_id': 'JN6Uml0yVsW5IXZMLr94gg', 'lang': 'Latin', 'term': 'encyclopaedia', 
            'reltype': 'group_derived_root', 'related_term_id': '', 'related_lang': '', 'related_term': '',
            'position': '0', 'group_tag': 'PdeKgdn0RDmyyejStXrMbQ', 'parent_tag': '', 'parent_position': ''
        },
        {
            'term_id': 'JN6Uml0yVsW5IXZMLr94gg', 'lang': 'Latin', 'term': 'encyclopaedia', 
            'reltype': 'etymologically_related_to', 'related_term_id': 'dQuegarKXeyzqn_4Bpfatg', 'related_lang': 'Ancient Greek', 'related_term': 'ἐγκύκλιος παιδείᾱ',
            'position': '0', 'group_tag': '', 'parent_tag': 'PdeKgdn0RDmyyejStXrMbQ', 'parent_position': '0'
        },
        {
            'term_id': 'JN6Uml0yVsW5IXZMLr94gg', 'lang': 'Latin', 'term': 'encyclopaedia', 
            'reltype': 'group_affix_root', 'related_term_id': '', 'related_lang': '', 'related_term': '',
            'position': '0', 'group_tag': 'rt2vt0MrSpSGl3zvWLPIUQ', 'parent_tag': 'PdeKgdn0RDmyyejStXrMbQ', 'parent_position': '1'
        },
        {
            'term_id': 'JN6Uml0yVsW5IXZMLr94gg', 'lang': 'Latin', 'term': 'encyclopaedia', 
            'reltype': 'etymologically_related_to', 'related_term_id': 'PIsyIrZQXnqu4Faflkgbvg', 'related_lang': 'Ancient Greek', 'related_term': 'ἐγκύκλιος',
            'position': '0', 'group_tag': '', 'parent_tag': 'rt2vt0MrSpSGl3zvWLPIUQ', 'parent_position': '0'
        },
        {
            'term_id': 'JN6Uml0yVsW5IXZMLr94gg', 'lang': 'Latin', 'term': 'encyclopaedia', 
            'reltype': 'etymologically_related_to', 'related_term_id': 'LIQjzB8gUaCYjywHWuofSA', 'related_lang': 'Ancient Greek', 'related_term': 'παιδείᾱ',
            'position': '0', 'group_tag': '', 'parent_tag': 'rt2vt0MrSpSGl3zvWLPIUQ', 'parent_position': '1'
        }
    ]

    grouped_data_input: Tuple[str, List[Dict[str, Any]]] = (test_term_id, fixed_records_from_dataset)
    subgraph_generator = create_networkx_subgraph(grouped_data_input)
    subgraph: nx.DiGraph | None = None
    async for sg in subgraph_generator:
        subgraph = sg
        break 
    assert subgraph is not None
    assert isinstance(subgraph, nx.DiGraph)
    expected_node_ids = {
        'JN6Uml0yVsW5IXZMLr94gg', 
        'cAiYCdUVXxe7CzwKH3rR1g', 
        'dQuegarKXeyzqn_4Bpfatg', 
        'PIsyIrZQXnqu4Faflkgbvg', 
        'LIQjzB8gUaCYjywHWuofSA'
    }
    assert set(subgraph.nodes()) == expected_node_ids, \
        f"Número o IDs de nodos incorrectos. Esperado: {expected_node_ids}, Obtenido: {set(subgraph.nodes())}"
    assert subgraph.number_of_nodes() == 5, "El número de nodos no es 5."

    expected_edges = {
        ('JN6Uml0yVsW5IXZMLr94gg', 'cAiYCdUVXxe7CzwKH3rR1g'),
        ('JN6Uml0yVsW5IXZMLr94gg', 'dQuegarKXeyzqn_4Bpfatg'),
        ('JN6Uml0yVsW5IXZMLr94gg', 'PIsyIrZQXnqu4Faflkgbvg'),
        ('JN6Uml0yVsW5IXZMLr94gg', 'LIQjzB8gUaCYjywHWuofSA')
    }
    assert set(subgraph.edges()) == expected_edges, \
        f"Los ejes no coinciden. Esperado: {expected_edges}, Obtenido: {set(subgraph.edges())}"
    assert subgraph.number_of_edges() == 4, "El número de ejes no es 4."

    node_main = subgraph.nodes[test_term_id]
    assert node_main['label'] == 'encyclopaedia'
    assert node_main['lang'] == 'Latin'
    node_related_greek = subgraph.nodes['cAiYCdUVXxe7CzwKH3rR1g']
    assert node_related_greek['label'] == 'ἐγκυκλοπαιδεία'
    assert node_related_greek['lang'] == 'Ancient Greek'
    edge_attrs_borrowed = subgraph.get_edge_data(test_term_id, 'cAiYCdUVXxe7CzwKH3rR1g')
    assert edge_attrs_borrowed is not None
    assert edge_attrs_borrowed['reltype'] == 'borrowed_from'
    assert 'position' in edge_attrs_borrowed
    assert edge_attrs_borrowed['position'] == '0'
    assert 'group_tag' not in edge_attrs_borrowed # Debería ser eliminado si es vacío
    assert 'parent_tag' not in edge_attrs_borrowed # Debería ser eliminado si es vacío
    edge_attrs_etym = subgraph.get_edge_data(test_term_id, 'dQuegarKXeyzqn_4Bpfatg')
    assert edge_attrs_etym is not None
    assert edge_attrs_etym['reltype'] == 'etymologically_related_to'
    assert 'position' in edge_attrs_etym
    assert edge_attrs_etym['position'] == '0'
    assert 'group_tag' not in edge_attrs_etym # Debería ser eliminado si es vacío
    assert edge_attrs_etym['parent_tag'] == 'PdeKgdn0RDmyyejStXrMbQ' # Este sí tiene un valor
