import math
import plotly.graph_objects as go
from typing import Dict, List, Any

class CitationVisualizationService:
    @staticmethod
    def generate_network_graph(paper_title: str, citations: List[Dict[str, Any]], references: List[Dict[str, Any]]) -> go.Figure:
        """
        Creates a circular layout network graph in Plotly representing the paper,
        its key citations, and its references.
        """
        # Node format: (id, name, type, year)
        nodes = [(0, paper_title[:40] + "...", "target", 2024)]
        edges = []
        
        # Add citations (papers that cite our paper)
        node_idx = 1
        for c in citations[:5]:
            title = c.get("title", f"Citing Paper {node_idx}")
            year = c.get("year", 2025)
            nodes.append((node_idx, title[:30] + "...", "citing", year))
            edges.append((node_idx, 0))  # cites target
            node_idx += 1
            
        # Add references (papers our paper cites)
        for r in references[:5]:
            title = r.get("title", f"Reference Paper {node_idx}")
            year = r.get("year", 2020)
            nodes.append((node_idx, title[:30] + "...", "referenced", year))
            edges.append((0, node_idx))  # target cites reference
            node_idx += 1
            
        # Layout calculation (circular layout around target node 0)
        # Target node is in the center (0, 0)
        x_coords = [0.0]
        y_coords = [0.0]
        
        n_outer = len(nodes) - 1
        for i in range(1, len(nodes)):
            angle = (2 * math.pi * (i - 1)) / n_outer if n_outer > 0 else 0
            x_coords.append(math.cos(angle))
            y_coords.append(math.sin(angle))
            
        # Edge lines
        edge_x = []
        edge_y = []
        for start, end in edges:
            edge_x.extend([x_coords[start], x_coords[end], None])
            edge_y.extend([y_coords[start], y_coords[end], None])
            
        # Create Scatter of Edges
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Split nodes by type for distinct colors
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        
        colors = {
            "target": "#FF4B4B",     # Streamlit Red
            "citing": "#1F77B4",     # Blue
            "referenced": "#2CA02C"  # Green
        }
        
        for idx, (nid, name, ntype, year) in enumerate(nodes):
            node_x.append(x_coords[idx])
            node_y.append(y_coords[idx])
            node_text.append(f"{name} ({year})<br>Type: {ntype.upper()}")
            node_color.append(colors[ntype])
            node_size.append(30 if ntype == "target" else 20)
            
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[nodes[i][1] for i in range(len(nodes))],
            textposition="top center",
            hovertext=node_text,
            marker=dict(
                showscale=False,
                color=node_color,
                size=node_size,
                line=dict(width=2, color='#fff')
            )
        )
        
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='Citation Network Graph',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        )
        
        return fig
