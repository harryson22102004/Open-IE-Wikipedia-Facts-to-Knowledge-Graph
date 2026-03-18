import re
import networkx as nx
 
def open_ie_extract(text):
    """Rule-based Open IE triplet extraction."""
    triplets = []
    patterns = [
        r'([A-Z][^,.]+?) (?:is|was|are|were) (?:a|an|the)? ?([^,.]+?) (?:in|of|at|from) ([^,.]+)',
        r'([A-Z][^,.]+?) (?:founded|established|created|built) ([^,.]+?) in (d{4})',
        r'([A-Z][^,.]+?) (?:born|died) in ([^,.]+)',
    ]
    for sent in re.split(r'(?<=[.!?]) +', text):
        words = sent.split()
        for i, word in enumerate(words):
            if word.lower() in ['is','was','founded','established','born','invented']:
                subj = ' '.join(words[max(0,i-3):i])
                rel = word
                obj = ' '.join(words[i+1:min(len(words),i+5)])
                if len(subj) > 2 and len(obj) > 2:
                    triplets.append((subj.strip(), rel, obj.strip()))
                     return triplets
 
class KnowledgeGraph:
    def __init__(self):
        self.G = nx.MultiDiGraph()
 
    def add_triple(self, subj, rel, obj):
        self.G.add_node(subj, type='entity')
        self.G.add_node(obj, type='entity')
        self.G.add_edge(subj, obj, relation=rel)
 
    def query(self, subject):
        if subject not in self.G: return []
        return [(subject, d['relation'], v) for _, v, d in self.G.out_edges(subject, data=True)]
 
    def stats(self):
        return {'nodes': self.G.number_of_nodes(), 'edges': self.G.number_of_edges()}
 
wiki_text = """
Albert Einstein was a German-born theoretical physicist. Einstein developed the
theory of relativity. He was born in Ulm in 1879. Einstein founded modern physics.
Marie Curie was a Polish physicist. She discovered radioactivity. Curie was born
in Warsaw in 1867. Isaac Newton invented calculus and discovered gravity.
"""
triplets = open_ie_extract(wiki_text)
kg = KnowledgeGraph()
for s, r, o in triplets:
    kg.add_triple(s, r, o)
print(f"Extracted {len(triplets)} triplets")
for t in triplets[:5]: print(f"  ({t[0]}) --[{t[1]}]--> ({t[2]})")
print(f"KG stats: {kg.stats()}")
