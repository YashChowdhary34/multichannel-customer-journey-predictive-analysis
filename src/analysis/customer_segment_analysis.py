import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

customer_segments = pd.read_csv('../../data/processed/customer_segments.csv')

def plot_segmentation_analysis():
    """Create visualizations for customer segmentation insights"""
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Segment Size Distribution',
            'Segment Value Distribution',
            'Segment Characteristics',
            'Segment Purchase Patterns'
        )
    )
    
    # Segment Size Distribution
    segment_sizes = customer_segments['Segment_Label'].value_counts()
    
    fig.add_trace(
        go.Pie(
            labels=segment_sizes.index,
            values=segment_sizes.values,
            textinfo='label+percent',
            hole=0.3
        ),
        row=1, col=1
    )
    
    # Segment Value Distribution
    segment_value = customer_segments.groupby('Segment').agg({
        'total_spend': 'sum',
        'Segment_Label': 'count'
    })
    
    fig.add_trace(
        go.Bar(
            x=segment_value['Segment_Label'],
            y=segment_value['total_spend'],
            text=(segment_value['total_spend']/1000).round(1),
            textposition='auto',
            name='Segment Revenue (K)'
        ),
        row=1, col=2
    )
    
    # Segment Characteristics
    segment_chars = customer_segments.groupby('segment').agg({
        'avg_order_value': 'mean',
        'purchase_frequency_mean': 'mean',
        'customer_lifespan_mean': 'mean'
    }).round(2)
    
    # Normalize for radar chart
    segment_chars_norm = (segment_chars - segment_chars.min()) / (segment_chars.max() - segment_chars.min())
    
    for segment in segment_chars_norm.index:
        fig.add_trace(
            go.Scatterpolar(
                r=segment_chars_norm.loc[segment],
                theta=segment_chars_norm.columns,
                name=segment,
                fill='toself'
            ),
            row=2, col=1
        )
    
    # Segment Purchase Patterns
    customer_segments['first_purchase'] = pd.to_datetime(customer_segments['first_purchase'])
    customer_segments['last_purchase'] = pd.to_datetime(customer_segments['last_purchase'])
    customer_segments['days_between_purchases'] = (customer_segments['last_purchase'] -     customer_segments['first_purchase'] ).dt.days

    purchase_patterns = customer_segments.groupby('segment').agg({
        'days_between_purchases': 'mean',
        'purchase_frequency_mean': 'mean'
    }).round(2)
    
    fig.add_trace(
        go.Scatter(
            x=purchase_patterns['days_between_purchases'],
            y=purchase_patterns['purchase_frequency_mean'],
            mode='markers+text',
            text=purchase_patterns.index,
            textposition="top center",
            marker=dict(size=15),
            name='Purchase Patterns'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=1000, title_text="Customer Segmentation Analysis Dashboard")
    return fig

segmentation_fig = plot_segmentation_analysis()