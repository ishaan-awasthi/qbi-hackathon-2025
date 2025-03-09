import pandas as pd
import matplotlib.pyplot as plt

# Define path and metric
path = './DATA/1000interhel_data.csv'  # Path to the dataset
metric = 'Delta_InterhelicalContacts'  # The metric to analyze
metric_name = 'Interhelical Contacts'

# Load the CSV data
data = pd.read_csv(path)

# Define the weightages dictionary
weightages = {
    '5UAK': 1, '5W81': 0.75, '5UAR': 75, '6MSM': 1,
    '6O1V': 1, '6O2P': 0.5, '7SVR': 0.5, '7SVD': 1,
    '7SV7': 0.5, '8EJ1': 0.5, '8EIQ': 0.4, '8EIO': 0.4,
    '8FZQ': 1
}

# Extract structure and mutation information
data['Structure'] = data['Structure_Residue'].apply(lambda x: x.split('_')[0])
data['Mutation'] = data['Structure_Residue'].apply(
    lambda x: '_'.join(x.split('_')[1:-1]))

# Filter out rows with missing metric values
data_filtered = data.dropna(subset=[metric])

# Function to calculate the weighted score for each mutation


def calculate_weighted_score(group):
    score = 0
    for _, row in group.iterrows():
        structure = row['Structure']
        metric_value = row[metric]
        if structure in weightages:
            score += metric_value * weightages[structure]
    return score


# Apply the calculation to each mutation
mutation_scores = data_filtered.groupby('Mutation').apply(
    calculate_weighted_score).reset_index(name=f'{metric}_Score')

# Save the scores to a CSV
output_csv_path = f'./RESULTS/mutation_{metric.lower()}_scores.csv'
mutation_scores.to_csv(output_csv_path, index=False)

# Generate a histogram
plt.figure(figsize=(8, 6))
plt.hist(mutation_scores[f'{metric}_Score'], bins=10, edgecolor='black')
plt.title(f'Histogram of Mutation {metric_name} Scores')
plt.xlabel(f'Final {metric_name} Score Ranges')
plt.ylabel('Number of Mutations')

# Save the histogram as an image
histogram_image_path = f'./RESULTS/mutation_{metric.lower()}_score_histogram.png'
plt.savefig(histogram_image_path)

# Output file paths
print(f"CSV saved at: {output_csv_path}")
print(f"Histogram saved at: {histogram_image_path}")
