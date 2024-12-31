def plot_clv_analysis():
    """Create comprehensive CLV analysis visualizations"""
    
    # Create subplots for CLV analysis
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'CLV Distribution by Segment',
            'Average CLV by Purchase Frequency',
            'CLV Trend Over Time',
            'CLV vs Customer Age'
        )
    )
    
    # CLV Distribution by Segment
    segment_clv = customer_segments.groupby('segment')['predicted_clv'].mean().sort_values()
    
    fig.add_trace(
        go.Bar(
            x=segment_clv.index,
            y=segment_clv.values,
            text=segment_clv.values.round(2),
            textposition='auto',
            name='Avg CLV'
        ),
        row=1, col=1
    )
    
    # Average CLV by Purchase Frequency
    purchase_freq_bins = pd.qcut(customer_metrics['purchase_frequency'], 5)
    avg_clv_by_freq = customer_metrics.groupby(purchase_freq_bins)['clv'].mean()
    
    fig.add_trace(
        go.Scatter(
            x=avg_clv_by_freq.index.astype(str),
            y=avg_clv_by_freq.values,
            mode='lines+markers',
            name='CLV by Frequency'
        ),
        row=1, col=2
    )
    
    # CLV Trend Over Time
    monthly_clv = customer_metrics.groupby(pd.to_datetime(customer_metrics['first_purchase']).dt.to_period('M'))['clv'].mean()
    
    fig.add_trace(
        go.Scatter(
            x=monthly_clv.index.astype(str),
            y=monthly_clv.values,
            mode='lines',
            name='Monthly CLV Trend'
        ),
        row=2, col=1
    )
    
    # CLV vs Customer Age
    fig.add_trace(
        go.Scatter(
            x=customer_metrics['customer_age_days'],
            y=customer_metrics['clv'],
            mode='markers',
            marker=dict(
                size=8,
                color=customer_metrics['purchase_frequency'],
                colorscale='Viridis',
                showscale=True
            ),
            name='CLV vs Age'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=800, title_text="Customer Lifetime Value Analysis Dashboard")
    return fig