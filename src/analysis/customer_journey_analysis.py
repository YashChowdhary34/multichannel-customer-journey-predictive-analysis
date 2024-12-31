def plot_journey_analysis():
    """Create visualizations for customer journey analysis"""
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Customer Journey Stages',
            'Channel Performance',
            'Conversion Funnel',
            'Time Between Stages'
        )
    )
    
    # Journey Stages Distribution
    stage_counts = customer_journey['current_stage'].value_counts()
    
    fig.add_trace(
        go.Bar(
            x=stage_counts.index,
            y=stage_counts.values,
            text=stage_counts.values,
            textposition='auto',
            name='Stage Distribution'
        ),
        row=1, col=1
    )
    
    # Channel Performance
    channel_conversion = customer_journey.groupby('acquisition_channel')['converted'].mean().sort_values()
    
    fig.add_trace(
        go.Bar(
            x=channel_conversion.index,
            y=channel_conversion.values * 100,
            text=(channel_conversion.values * 100).round(1),
            textposition='auto',
            name='Channel Conversion Rate'
        ),
        row=1, col=2
    )
    
    # Conversion Funnel
    funnel_stages = ['awareness', 'consideration', 'purchase', 'retention']
    funnel_values = [
        len(customer_journey[customer_journey['journey_stage'] >= stage])
        for stage in range(len(funnel_stages))
    ]
    
    fig.add_trace(
        go.Funnel(
            y=funnel_stages,
            x=funnel_values,
            textinfo="value+percent initial"
        ),
        row=2, col=1
    )
    
    # Time Between Stages
    stage_durations = customer_journey.groupby('current_stage')['days_in_stage'].mean().sort_values()
    
    fig.add_trace(
        go.Bar(
            x=stage_durations.index,
            y=stage_durations.values,
            text=stage_durations.values.round(1),
            textposition='auto',
            name='Avg Days in Stage'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=800, title_text="Customer Journey Analysis Dashboard")
    return fig