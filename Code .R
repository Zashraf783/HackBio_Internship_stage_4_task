# Load necessary libraries
library(TCGAbiolinks)
library(SummarizedExperiment)
library(DESeq2)

# Downloading data
LGGdata <- GDCquery(
  project = "TCGA-LGG",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  experimental.strategy = "RNA-Seq"
)
output <- getResults(LGGdata)
GDCdownload(LGGdata)

# Preparing the data
LGG.data <- GDCprepare(LGGdata)
data <- assay(LGG.data, "unstranded")

# Metadata
simpleMeta <- data.frame(
  "barcode" = LGG.data$barcode,
  "IDH_status" = LGG.data$paper_IDH.status
)

# Remove samples with missing IDH status
simpleMeta_clean <- simpleMeta[!is.na(simpleMeta$IDH_status), ]
data <- data[, simpleMeta_clean$barcode]  # Match expression data to clean metadata

# Preprocessing: Remove genes with more than 25 zero values
data <- data[apply(data, 1, function(row) sum(row == 0) <= 25), ]

####################################################################
######## Differential Expression Analysis (DEA) with DESeq2 ########

# Create DESeq2 object
dds <- DESeqDataSetFromMatrix(countData = data, 
                              colData = simpleMeta_clean, 
                              design = ~ IDH_status)

# Filter out genes with low counts (keep rows with more than 10 reads across all samples)
dds <- dds[rowSums(counts(dds)) > 10, ]

# Run the DESeq pipeline
dds <- DESeq(dds)

# Get the results for IDH Wildtype vs IDH Mutant
res <- results(dds, contrast = c("IDH_status", "WT", "Mutant"))
summary(res)

# Filter significant genes (padj < 0.05 and log2FoldChange > 1)
degs <- res[which(res$padj < 0.05 & abs(res$log2FoldChange) > 1), ]
deg_list <- rownames(degs)

# Save results to CSV
write.csv(as.data.frame(res), "DESeq2_results_TCGA_LGG.csv")

######################## Visualization ###########################

# MA Plot
plotMA(res, main = "MA Plot of DESeq2 (IDH WT vs Mutant)")
