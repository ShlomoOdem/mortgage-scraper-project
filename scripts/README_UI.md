# Mortgage Data Graph Generator UI

A web-based interface for creating interactive graphs from the combined mortgage summary data.

## Features

- **Interactive Graph Types**: Scatter plots, line charts, bar charts, histograms, and box plots
- **Flexible Column Selection**: Choose any column for X-axis, Y-axis, color grouping, and size variation
- **Advanced Filtering**: Filter data by value ranges (numeric columns) or multiple selections (categorical columns)
- **Real-time Updates**: Generate graphs instantly with your selections
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_ui.txt
```

2. Make sure the combined summary file exists:
```bash
ls data/analyzed/combined_summary_files.csv
```

## Usage

1. Start the web server:
```bash
python scripts/graph_ui.py
```

2. Open your web browser and go to:
```
http://localhost:5000
```

## How to Use

### 1. Graph Configuration
- **Graph Type**: Choose from scatter plot, line chart, bar chart, histogram, or box plot
- **X-Axis Column**: Select the column for the horizontal axis
- **Y-Axis Column**: Select the column for the vertical axis
- **Color By**: Optional grouping by color (useful for categorical data)
- **Size By**: Optional size variation (only available for scatter plots)
- **Title**: Optional custom title for your graph

### 2. Data Filtering
Each column has its own filter controls:

**Numeric Columns** (Interest Rate, Term Months, etc.):
- Use the min/max input fields to set value ranges
- Only data within the specified range will be included

**Categorical Columns** (Channel, Loan Type, etc.):
- Use the multi-select dropdown to choose specific values
- Only selected values will be included in the graph

### 3. Generate Graph
- Click "Generate Graph" to create your visualization
- The graph will appear in the right panel
- Statistics about the data points will be shown below the graph

## Available Columns

### Numeric Columns
- **Interest_Rate**: Mortgage interest rate (2.0% - 6.0%)
- **Term_Months**: Loan term in months (96 - 360)
- **Inflation_Rate**: Inflation rate (1.0% - 4.0%)
- **Loan_Amount**: Original loan amount
- **Total_Monthly_Payments**: Number of payments
- **Total_Mortgage_Interest**: Total interest paid
- **Weighted_Cost**: Weighted calculation cost
- **Monthly_Income**: Monthly income
- **Total_Investment_Amount**: Total amount invested
- **Total_Investment_Final_Value**: Final investment value
- **Total_Investment_Profit_After_Tax**: Profit after taxes
- **Weighted_Monthly_Payment**: Weighted monthly payment
- **Weighted_Investment_Profit**: Weighted investment profit

### Categorical Columns
- **Channel**: Mortgage channel type (פריים, קבועה לא צמודה, etc.)
- **Loan_Type**: Type of loan
- **Amortization_Method**: Payment method (קרן שווה, etc.)
- **Weighted_Calculation_Converged**: Whether calculation converged

## Example Use Cases

### 1. Interest Rate Analysis
- **X-Axis**: Interest_Rate
- **Y-Axis**: Total_Mortgage_Interest
- **Color By**: Channel
- **Filter**: Channel = "פריים"

### 2. Investment Performance
- **X-Axis**: Term_Months
- **Y-Axis**: Total_Investment_Profit_After_Tax
- **Color By**: Channel
- **Filter**: Interest_Rate range 3.0-4.0

### 3. Weighted Payment Analysis
- **X-Axis**: Weighted_Monthly_Payment
- **Y-Axis**: Weighted_Cost
- **Color By**: Channel
- **Filter**: Term_Months range 240-360

### 4. Distribution Analysis
- **Graph Type**: Histogram
- **X-Axis**: Interest_Rate
- **Color By**: Channel
- **Filter**: Term_Months = 360

## Tips

1. **Start Simple**: Begin with scatter plots to explore relationships
2. **Use Filters**: Apply filters to focus on specific data subsets
3. **Try Different Graph Types**: Different visualizations reveal different insights
4. **Group by Color**: Use categorical columns for color grouping to see patterns
5. **Check Data Points**: The statistics show how many data points are included

## Troubleshooting

- **No Graph Appears**: Check that you've selected both X and Y columns
- **Empty Graph**: Try adjusting your filters - they might be too restrictive
- **Slow Loading**: Large datasets may take a moment to process
- **Browser Issues**: Try refreshing the page if the interface becomes unresponsive

## Data Source

The UI uses the combined summary file created by `scripts/combine_summary_files.py`, which contains data from 25,593 mortgage scenarios with various combinations of:
- 6 different mortgage channels
- 17 different interest rates (2.0% - 6.0%)
- 23 different loan terms (96 - 360 months)
- 13 different inflation rates (1.0% - 4.0%) 