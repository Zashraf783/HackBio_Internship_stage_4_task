
# Load libraries
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Load the gene expression data
gene_data = pd.read_csv('New_data.csv')
labels = pd.read_csv('labels1.csv')

# Display shapes of the datasets
print(f"Labels Shape: {labels.shape}")
print(f"Gene Data Shape: {gene_data.shape}")

# Separate gene IDs from gene data
gene_ids = gene_data.iloc[:, 0]  # Assuming the first column is gene IDs
gene_data = gene_data.iloc[:, 1:]

# Normalize the numeric expression data
scaler = StandardScaler()
gene_data_normalized = pd.DataFrame(scaler.fit_transform(gene_data), columns=gene_data.columns)


# Apply PCA to reduce dimensions for visualization
pca = PCA(n_components=2)  # Reduce to 2 dimensions
gene_data_pca = pca.fit_transform(gene_data_normalized)

# Display the explained variance ratio by the two principal components
print("Explained variance by components:", pca.explained_variance_ratio_)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=6, random_state=42)  # Assume 6 clusters based on the six IDH statuses
clusters = kmeans.fit_predict(gene_data_normalized)

# Add cluster labels to the normalized data
gene_data_normalized['Cluster'] = clusters

# Plot the clusters based on the first two principal components
plt.figure(figsize=(10, 7))
plt.scatter(gene_data_pca[:, 0], gene_data_pca[:, 1], c=clusters, cmap='viridis', marker='o')
plt.title('K-Means Clustering of Gene Expression Data (PCA)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Cluster')
plt.show()

# Calculate and print the silhouette score to assess clustering quality
silhouette_avg = silhouette_score(gene_data_normalized.drop(columns='Cluster'), clusters)
silhouette_percentage = silhouette_avg * 100
print(f'Silhouette Score: {silhouette_percentage:.2f}%')
