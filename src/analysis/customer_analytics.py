import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

class CustomerAnalyticsVisualizer:
    def __init__(self, df_predictions):
        """
        Initialize the visualizer with customer predictions dataframe
        """
        self.df = df_predictions
        plt.style.use('seaborn')
        
    def plot_churn_distribution(self):
        """
        Create an advanced visualization of churn probability distribution with risk segments
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Churn Probability Distribution', 'Churn Risk by Segment',
                          'Customer Lifetime Value vs Churn Risk', 'Churn Risk Timeline')
        )
        
        # Distribution plot
        fig.add_trace(
            go.Histogram(x=self.df['churn_probability'], 
                        nbinsx=50,
                        name='Distribution',
                        marker_color='rgba(58, 71, 80, 0.6)'),
            row=1, col=1
        )
        
        # Risk segments by customer segment
        risk_by_segment = pd.crosstab(
            pd.qcut(self.df['churn_probability'], q=4, labels=['Low', 'Medium', 'High', 'Critical']),
            self.df['Segment_Label']
        )
        
        fig.add_trace(
            go.Bar(x=risk_by_segment.index, 
                  y=risk_by_segment['High-Value'],
                  name='High-Value'),
            row=1, col=2
        )
        
        # CLV vs Churn scatter
        fig.add_trace(
            go.Scatter(x=self.df['churn_probability'],
                      y=self.df['predicted_clv'],
                      mode='markers',
                      marker=dict(
                          size=8,
                          color=self.df['total_spend'],
                          colorscale='Viridis',
                          showscale=True
                      ),
                      name='CLV vs Churn'),
            row=2, col=1
        )
        
        # Churn risk timeline
        timeline_data = self.df.groupby('last_purchase')['churn_probability'].mean().reset_index()
        fig.add_trace(
            go.Scatter(x=timeline_data['last_purchase'],
                      y=timeline_data['churn_probability'],
                      mode='lines+markers',
                      name='Risk Timeline'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, width=1200, title_text="Customer Churn Analysis Dashboard")
        return fig
    
    def plot_customer_segments(self):
        """
        Create visualization for customer segmentation analysis
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Segment Distribution', 'Average CLV by Segment',
                          'Purchase Frequency vs Total Spend', 'Customer Lifespan Analysis')
        )
        
        # Segment distribution
        segment_counts = self.df['Segment_Label'].value_counts()
        fig.add_trace(
            go.Pie(labels=segment_counts.index,
                  values=segment_counts.values,
                  hole=0.4),
            row=1, col=1
        )
        
        # Average CLV by segment
        avg_clv = self.df.groupby('Segment_Label')['predicted_clv'].mean().sort_values(ascending=True)
        fig.add_trace(
            go.Bar(x=avg_clv.index,
                  y=avg_clv.values,
                  marker_color='rgb(158,202,225)'),
            row=1, col=2
        )
        
        # Purchase frequency vs total spend scatter
        fig.add_trace(
            go.Scatter(x=self.df['purchase_frequency'],
                      y=self.df['total_spend'],
                      mode='markers',
                      marker=dict(
                          size=8,
                          color=self.df['customer_lifespan'],
                          colorscale='Viridis',
                          showscale=True
                      )),
            row=2, col=1
        )
        
        # Customer lifespan analysis
        lifespan_data = self.df.groupby('Segment_Label')['customer_lifespan'].agg(['mean', 'std']).reset_index()
        fig.add_trace(
            go.Bar(x=lifespan_data['Segment_Label'],
                  y=lifespan_data['mean'],
                  error_y=dict(type='data', array=lifespan_data['std']),
                  name='Avg Lifespan'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, width=1200, title_text="Customer Segmentation Analysis Dashboard")
        return fig
    
    def generate_risk_matrix(self):
        """
        Create a risk matrix combining CLV and churn probability
        """
        fig = go.Figure()
        
        # Create risk quadrants
        fig.add_trace(
            go.Scatter(x=self.df['churn_probability'],
                      y=self.df['predicted_clv'],
                      mode='markers',
                      marker=dict(
                          size=10,
                          color=self.df['total_spend'],
                          colorscale='Viridis',
                          showscale=True
                      ),
                      text=self.df['CustomerID'],
                      name='Customers')
        )
        
        # Add quadrant lines
        churn_median = self.df['churn_probability'].median()
        clv_median = self.df['predicted_clv'].median()
        
        fig.add_hline(y=clv_median, line_dash="dash", line_color="gray")
        fig.add_vline(x=churn_median, line_dash="dash", line_color="gray")
        
        # Add annotations for quadrants
        fig.add_annotation(x=0.25, y=self.df['predicted_clv'].max() * 0.9,
                         text="Loyal High-Value", showarrow=False)
        fig.add_annotation(x=0.75, y=self.df['predicted_clv'].max() * 0.9,
                         text="At-Risk High-Value", showarrow=False)
        fig.add_annotation(x=0.25, y=self.df['predicted_clv'].min() * 1.1,
                         text="Loyal Low-Value", showarrow=False)
        fig.add_annotation(x=0.75, y=self.df['predicted_clv'].min() * 1.1,
                         text="At-Risk Low-Value", showarrow=False)
        
        fig.update_layout(
            title="Customer Risk-Value Matrix",
            xaxis_title="Churn Probability",
            yaxis_title="Predicted Customer Lifetime Value",
            height=600,
            width=800
        )
        
        return fig

    def save_for_power_bi(self, output_path):
        """
        Save processed data for Power BI consumption
        """
        # Create risk segments
        self.df['risk_segment'] = pd.qcut(self.df['churn_probability'], 
                                        q=4, 
                                        labels=['Low', 'Medium', 'High', 'Critical'])
        
        # Calculate additional metrics for Power BI
        risk_metrics = self.df.groupby('risk_segment').agg({
            'predicted_clv': 'mean',
            'total_spend': 'sum',
            'purchase_frequency': 'mean',
            'customer_lifespan': 'mean'
        }).reset_index()
        
        segment_metrics = self.df.groupby('Segment_Label').agg({
            'churn_probability': 'mean',
            'predicted_clv': 'sum',
            'total_spend': 'mean',
            'customer_lifespan': 'mean'
        }).reset_index()
        
        # Save processed files for Power BI
        self.df.to_csv(f"{output_path}/customer_full_analysis.csv", index=False)
        risk_metrics.to_csv(f"{output_path}/risk_segment_metrics.csv", index=False)
        segment_metrics.to_csv(f"{output_path}/customer_segment_metrics.csv", index=False)