import pandas as pd
import os

# Define file paths
files = {
    "clashes": "./NORM_RESULTS/clashes_normalized_data.csv",
    "interres": "./NORM_RESULTS/interres_normalized_data.csv",
    "interhel": "./NORM_RESULTS/interhel_normalized_data.csv",
    "hbonds": "./NORM_RESULTS/hbonds_normalized_data.csv",
    "locations": "./NORM_RESULTS/locations_normalized_data.csv"
}

# Define weightages
weights = {
    "clashes": 5,
    "locations": 4,
    "interres": 2,
    "interhel": 3,
    "hbonds": 2
}

# Load data
dfs = {key: pd.read_csv(file) for key, file in files.items()}

# Merge all dataframes on mutation
merged_df = dfs["clashes"]
for key, df in dfs.items():
    if key != "clashes":
        merged_df = merged_df.merge(
            df, on="Mutation", suffixes=(False, f"_{key}"))

# Rename columns for clarity
merged_df.columns = ["Mutation", "Clashes",
                     "Interresidual", "Interhelical", "Hbonds", "Location"]

# Compute weighted sum
merged_df["Weighted_Score"] = (
    merged_df["Clashes"] * weights["clashes"] +
    merged_df["Interresidual"] * weights["interres"] +
    merged_df["Interhelical"] * weights["interhel"] +
    merged_df["Hbonds"] * weights["hbonds"] +
    merged_df["Location"] * weights["locations"]
)

# Normalize to 0-10 scale
max_score = merged_df["Weighted_Score"].max()
merged_df["Final_Score"] = (merged_df["Weighted_Score"] / max_score) * 10

# Define classification


def classify(score):
    if score > 7:
        return "Very Deleterious"
    elif score > 5:
        return "Deleterious"
    elif score > 3:
        return "Intermediate Deleterious"
    elif score > 1:
        return "Benign"
    else:
        return "No Effect"


merged_df["Classification"] = merged_df["Final_Score"].apply(classify)

# Ensure output directory exists
output_dir = "./FINAL/"
os.makedirs(output_dir, exist_ok=True)

# Save full results
full_output_file = os.path.join(output_dir, "final_scoring_results.csv")
merged_df.to_csv(full_output_file, index=False)

# Save simplified results
simplified_output_file = os.path.join(output_dir, "final_scoring_summary.csv")
simplified_df = merged_df[["Mutation", "Final_Score", "Classification"]]
simplified_df.to_csv(simplified_output_file, index=False)

print(f"Final scoring results saved to {full_output_file}")
print(f"Summary results saved to {simplified_output_file}")
