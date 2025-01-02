import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import logging

class CustomerScorer:
  
  def __init__(self):
    self.scalar = MinMaxScaler()
    self.weights = {
      'avg_order_value': 0.3,
      'recency': 0.25,
      'avg_purchase_interval': 0.2,
      'purchase_regularity': 0.15,
      'purchase_frequency': 0.1
    }

    logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    self.logger = logging.getLogger(__name__)

  def calculate_scores_component(self, customer_data):
    try:
      scores_df = customer_data.copy()

      for column in self.weights.keys():
        if column == 'recency':
          scores_df[f'{column}_score'] = self.scalar.fit_transform(
            scores_df[[column]].fillna(scores_df[column].mean())
          )
          scores_df[f'{column}_score'] = 1 - scores_df[f'{column}_score']
        
        else:
          scores_df[f'{column}_score'] = self.scalar.fit_transform(
            scores_df[[column]].fillna(scores_df[column].mean())
          )
      
      self.logger.info('---Components scores calculated successfully---')
      return scores_df
    
    except Exception as e:
      self.logger.error(f'---Error calculating components scores: {str(e)}---')
      raise
  
  def calculate_final_score(self, scores_df):
    try:
      final_score = sum(scores_df[f'{component}_score']*weight for component, weight in self.weights.items())

      final_score = (final_score * 100).round(0)

      score_categories = pd.cut(
        final_score,
        bins=[0, 20, 40, 60, 80, 100],
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
      )

      result_df = scores_df.copy()
      result_df['final_score'] = final_score
      result_df['score_category'] = score_categories

      self.logger.info('---Final scores calculated successfully---')
      return result_df
    
    except Exception as e:
      self.logger.error(f'---Error calculating final scores: {str(e)}---')
      raise

  def generate_insights(self, scored_data):
    try:
      insights = {
        'score_distribution': scored_data['score_category'].value_counts().to_dict(),
        'average_score': scored_data['final_score'].mean(),
        'median_score': scored_data['final_score'].median(),
        'top_performers': scored_data.nlargest(5, 'final_score')[
          ['customer_id', 'final_score', 'score_category']
        ].to_dict('records')
      }

      self.logger.info('---Customer insights generated successfully---')
      return insights
    
    except Exception as e:
      self.logger.error(f'---Error generating insights: {str(e)}---')
      raise