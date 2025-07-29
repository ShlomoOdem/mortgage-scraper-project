#!/usr/bin/env python3
"""
Verification System
Checks if mortgage combinations have already been extracted or analyzed
"""

import os
import json
import glob
from typing import List, Dict, Any, Tuple
from datetime import datetime

class VerificationSystem:
    def __init__(self, raw_data_dir="data/raw", analyzed_data_dir="data/analyzed"):
        self.raw_data_dir = raw_data_dir
        self.analyzed_data_dir = analyzed_data_dir
        self.extraction_tracking_file = "extraction_tracking.json"
        self.analysis_tracking_file = "analysis_tracking.json"
        
        # Ensure directories exist
        os.makedirs(raw_data_dir, exist_ok=True)
        os.makedirs(analyzed_data_dir, exist_ok=True)
    
    def get_combination_key(self, combination: Dict[str, Any]) -> str:
        """Generate a unique key for a mortgage combination"""
        return f"{combination['loan_amount']}_{combination['interest_rate']}_{combination['loan_term_months']}_{combination['cpi_rate']}_{combination['channel']}_{combination['amortization']}"
    
    def get_combination_filename(self, combination: Dict[str, Any]) -> str:
        """Generate filename for a combination"""
        key = self.get_combination_key(combination)
        amortization = combination.get('amortization', 'קרן_שווה')  # Default to קרן שווה if not present
        return f"loan_{combination['channel']}_int_{combination['interest_rate']}_term_{combination['loan_term_months']}_infl_{combination['cpi_rate']}_amort_{amortization}"
    
    def check_extraction_status(self, combination: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if combination has been extracted"""
        filename = self.get_combination_filename(combination)
        
        # Check if files exist
        payments_file = os.path.join(self.raw_data_dir, "payments_files", f"{filename}_payments.csv")
        summary_file = os.path.join(self.raw_data_dir, "summary_files", f"{filename}_summary.csv")
        
        payments_exist = os.path.exists(payments_file)
        summary_exist = os.path.exists(summary_file)
        
        if payments_exist and summary_exist:
            return True, f"Already extracted: {filename}"
        else:
            return False, f"Not extracted: {filename}"
    
    def check_analysis_status(self, combination: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if combination has been analyzed"""
        filename = self.get_combination_filename(combination)
        
        # Check if analyzed files exist
        enhanced_payments_file = os.path.join(self.analyzed_data_dir, "payments_files", f"{filename}_enhanced_payments.csv")
        enhanced_summary_file = os.path.join(self.analyzed_data_dir, "summary_files", f"{filename}_enhanced_summary.csv")
        
        payments_exist = os.path.exists(enhanced_payments_file)
        summary_exist = os.path.exists(enhanced_summary_file)
        
        if payments_exist and summary_exist:
            return True, f"Already analyzed: {filename}"
        else:
            return False, f"Not analyzed: {filename}"
    
    def check_combination_status(self, combination: Dict[str, Any]) -> Dict[str, Any]:
        """Check both extraction and analysis status for a combination"""
        extracted, extraction_msg = self.check_extraction_status(combination)
        analyzed, analysis_msg = self.check_analysis_status(combination)
        
        return {
            'combination': combination,
            'extracted': extracted,
            'analyzed': analyzed,
            'extraction_message': extraction_msg,
            'analysis_message': analysis_msg,
            'needs_extraction': not extracted,
            'needs_analysis': extracted and not analyzed
        }
    
    def filter_combinations(self, combinations: List[Dict[str, Any]], 
                          skip_extracted: bool = True, 
                          skip_analyzed: bool = True) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Filter combinations based on their status"""
        needs_extraction = []
        needs_analysis = []
        already_processed = []
        
        for combination in combinations:
            status = self.check_combination_status(combination)
            
            if status['needs_extraction']:
                needs_extraction.append(combination)
            elif status['needs_analysis']:
                needs_analysis.append(combination)
            else:
                already_processed.append(combination)
        
        # Apply filters - only clear lists if explicitly requested
        if skip_extracted:
            needs_extraction = []
        
        if skip_analyzed:
            needs_analysis = []
        
        return needs_extraction, needs_analysis, already_processed
    
    def get_processing_summary(self, combinations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get a summary of processing status for all combinations"""
        needs_extraction, needs_analysis, already_processed = self.filter_combinations(
            combinations, skip_extracted=False, skip_analyzed=False
        )
        
        return {
            'total_combinations': len(combinations),
            'needs_extraction': len(needs_extraction),
            'needs_analysis': len(needs_analysis),
            'already_processed': len(already_processed),
            'extraction_combinations': needs_extraction,
            'analysis_combinations': needs_analysis,
            'processed_combinations': already_processed
        }
    
    def mark_as_extracted(self, combination: Dict[str, Any], success: bool = True):
        """Mark a combination as extracted"""
        key = self.get_combination_key(combination)
        tracking_data = self._load_tracking_data(self.extraction_tracking_file)
        
        tracking_data[key] = {
            'combination': combination,
            'extracted': success,
            'timestamp': datetime.now().isoformat(),
            'filename': self.get_combination_filename(combination)
        }
        
        self._save_tracking_data(self.extraction_tracking_file, tracking_data)
    
    def mark_as_analyzed(self, combination: Dict[str, Any], success: bool = True):
        """Mark a combination as analyzed"""
        key = self.get_combination_key(combination)
        tracking_data = self._load_tracking_data(self.analysis_tracking_file)
        
        tracking_data[key] = {
            'combination': combination,
            'analyzed': success,
            'timestamp': datetime.now().isoformat(),
            'filename': self.get_combination_filename(combination)
        }
        
        self._save_tracking_data(self.analysis_tracking_file, tracking_data)
    
    def _load_tracking_data(self, filename: str) -> Dict[str, Any]:
        """Load tracking data from file"""
        filepath = os.path.join(self.raw_data_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_tracking_data(self, filename: str, data: Dict[str, Any]):
        """Save tracking data to file"""
        filepath = os.path.join(self.raw_data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def print_status_report(self, combinations: List[Dict[str, Any]]):
        """Print a detailed status report"""
        summary = self.get_processing_summary(combinations)
        
        print(f"\n{'PROCESSING STATUS REPORT':-^60}")
        print(f"Total combinations: {summary['total_combinations']}")
        print(f"Needs extraction: {summary['needs_extraction']}")
        print(f"Needs analysis: {summary['needs_analysis']}")
        print(f"Already processed: {summary['already_processed']}")
        
        if summary['needs_extraction'] > 0:
            print(f"\nCombinations needing extraction:")
            for i, combo in enumerate(summary['extraction_combinations'], 1):
                print(f"  {i}. {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
                print(f"     Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
        
        if summary['needs_analysis'] > 0:
            print(f"\nCombinations needing analysis:")
            for i, combo in enumerate(summary['analysis_combinations'], 1):
                print(f"  {i}. {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
                print(f"     Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
        
        if summary['already_processed'] > 0:
            print(f"\nAlready processed combinations:")
            for i, combo in enumerate(summary['processed_combinations'][:3], 1):  # Show first 3
                print(f"  {i}. {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
                print(f"     Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
            
            if len(summary['processed_combinations']) > 3:
                print(f"  ... and {len(summary['processed_combinations']) - 3} more")

def main():
    """Test the verification system"""
    from combination_loader import load_combinations, create_sample_combination_file
    
    # Create a sample combination file if it doesn't exist
    sample_file = "sample_combinations.json"
    if not os.path.exists(sample_file):
        create_sample_combination_file(sample_file)
    
    # Load combinations
    combinations = load_combinations(sample_file)
    
    # Create verification system
    verifier = VerificationSystem()
    
    # Print status report
    verifier.print_status_report(combinations)

if __name__ == "__main__":
    main() 