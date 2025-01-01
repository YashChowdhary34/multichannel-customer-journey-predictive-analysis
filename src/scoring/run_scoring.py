import pandas as pd
from customer_scorer import CustomerScorer
import logging
import json
from pathlib import Path

def main():
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  )
  logger = logging.getLogger(__name__)

  try:
    data_dir = Path('data/processed')
    output_dir = Path('data/scored')
    output_dir.mkdir(exist_ok=True)

    predictions_path = data_dir/'customer_predictions.csv'
    customer_data = pd.read_csv(predictions_path)
    logger.info(f'Loaded customer data with {len(customer_data)} records')

    scorer = CustomerScorer()

    customer_data['recency'] = (customer_data['last_purchase'].max() - customer_data['last_purchase']).dt.days
    
    scored_data = scorer.calculate_scores_component(customer_data)

    final_scored_data = scorer.calculate_final_score(scored_data)

    insights = scorer.generate_insights(final_scored_data)

    final_scored_data.to_csv(output_dir / 'customer_scores.csv', index=False)
    logger.info('Scoring process completed successfully')
  
  except Exception as e:
    logger.info(f'Error in scoring process: {str(e)}')
    raise

if __name__ == '__main__':
  main()