from ydata_profiling import ProfileReport
import pandas as pd

# Load the CSV data into a Pandas DataFrame
data = pd.read_csv("scraped_product_details-4.csv")

# Generate the profiling report
profile = ProfileReport(data, title="Tesco Report")

# Save the report as an HTML file
profile.to_file("profiling_report.html")
