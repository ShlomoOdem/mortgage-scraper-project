# Combination Generator Script

This script generates all possible mortgage combinations based on user-defined ranges and saves them to a JSON file that can be used with the modular workflow.

## Features

- **Flexible Ranges**: Define min, max, and step values for interest rates, inflation rates, and loan terms
- **Complete Coverage**: Includes all possible channels and amortization methods
- **Fixed Loan Amount**: Uses a fixed loan amount (default: 1,000,000 NIS)
- **Multiple Output Formats**: Supports JSON, CSV, and YAML formats
- **Preview Mode**: Test combinations without saving to file

## Usage

### Basic Usage

```bash
# Generate with default settings (7,560 combinations)
python3 scripts/generate_combinations.py

# Preview first 5 combinations without saving
python3 scripts/generate_combinations.py --preview

# Generate with custom ranges
python3 scripts/generate_combinations.py \
  --interest-min 3.5 \
  --interest-max 4.5 \
  --interest-step 0.25 \
  --inflation-min 2.0 \
  --inflation-max 3.0 \
  --inflation-step 0.5 \
  --term-min 240 \
  --term-max 360 \
  --term-step 60
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--interest-min` | 3.0 | Minimum interest rate (%) |
| `--interest-max` | 5.0 | Maximum interest rate (%) |
| `--interest-step` | 0.25 | Interest rate step (%) |
| `--inflation-min` | 1.0 | Minimum inflation rate (%) |
| `--inflation-max` | 4.0 | Maximum inflation rate (%) |
| `--inflation-step` | 0.5 | Inflation rate step (%) |
| `--term-min` | 120 | Minimum loan term (months) |
| `--term-max` | 360 | Maximum loan term (months) |
| `--term-step` | 60 | Loan term step (months) |
| `--loan-amount` | "1000000" | Fixed loan amount |
| `--output` | "data/combinations.json" | Output file path |
| `--preview` | False | Show preview without saving |

### Included Channels

The script includes all possible mortgage channels:
- קבועה צמודה (Fixed Linked)
- קבועה לא צמודה (Fixed Unlinked)
- פריים (Prime)
- משתנה צמודה (Variable Linked)
- משתנה לא צמודה (Variable Unlinked)
- דולר (Dollar)
- יורו (Euro)
- זכאות (Eligibility)

### Included Amortization Methods

The script includes all possible amortization methods:
- שפיצר (Spitzer)
- קרן שווה (Equal Principal)
- בוליט (Bullet)

## Examples

### Small Test Set (192 combinations)
```bash
python3 scripts/generate_combinations.py \
  --interest-min 3.5 \
  --interest-max 4.0 \
  --interest-step 0.5 \
  --inflation-min 2.0 \
  --inflation-max 2.5 \
  --inflation-step 0.5 \
  --term-min 240 \
  --term-max 300 \
  --term-step 60 \
  --output data/test_combinations.json
```

### Comprehensive Set (7,560 combinations)
```bash
python3 scripts/generate_combinations.py \
  --output data/full_combinations.json
```

### Using with Workflow

After generating combinations, you can use them with the modular workflow:

```bash
# Check status of all combinations
python3 run_modular_workflow.py --combination-file data/combinations.json --status

# Run extraction for all combinations
python3 run_modular_workflow.py --combination-file data/combinations.json --extract

# Run analysis for all combinations
python3 run_modular_workflow.py --combination-file data/combinations.json --analyze

# Run full workflow
python3 run_modular_workflow.py --combination-file data/combinations.json --full
```

## Output Format

The generated JSON file contains an array of combination objects:

```json
[
  {
    "loan_amount": "1000000",
    "interest_rate": "3.5",
    "loan_term_months": "240",
    "cpi_rate": "2.0",
    "channel": "קבועה צמודה",
    "amortization": "שפיצר"
  },
  ...
]
```

## Performance Considerations

- **Small Sets**: For testing, use 100-500 combinations
- **Medium Sets**: For analysis, use 1,000-5,000 combinations  
- **Large Sets**: For comprehensive analysis, use 5,000+ combinations

The default settings generate 7,560 combinations, which provides comprehensive coverage but may take significant time to process.

## Tips

1. **Start Small**: Use `--preview` to test your ranges before generating large files
2. **Use Steps**: Larger step values reduce the number of combinations
3. **Focus on Ranges**: Narrow your interest rate and inflation ranges to reduce combinations
4. **Batch Processing**: The workflow can handle large files but processes them in batches
5. **Status Checking**: Use the `--status` command to see what's already been processed 