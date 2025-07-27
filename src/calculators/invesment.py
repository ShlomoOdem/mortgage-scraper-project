class StockInvestment:
    """
    A class to calculate stock investment returns where all monthly investments
    are known upfront, and each month's contribution is tracked separately
    until the end of the investment period.
    """
    
    def __init__(self, monthly_investments, annual_return_rate, annual_inflation_rate=0.03, tax_rate=0.25):
        """
        Initialize the investment calculator with the complete investment sequence.
        
        Args:
            monthly_investments (list): List of monthly investment amounts
            annual_return_rate (float): Annual return rate (e.g., 0.07 for 7%)
            annual_inflation_rate (float): Annual inflation rate (default 3%)
            tax_rate (float): Tax rate on profits after inflation (default 25%)
        """
        self.monthly_investments = monthly_investments
        self.total_months = len(monthly_investments)
        self.annual_return_rate = annual_return_rate
        self.monthly_return_rate = (1 + annual_return_rate) ** (1/12) - 1
        self.annual_inflation_rate = annual_inflation_rate
        self.monthly_inflation_rate = (1 + annual_inflation_rate) ** (1/12) - 1
        self.tax_rate = tax_rate
        
        # Calculate investment details for each month
        self.investment_details = self._calculate_all_investments()
    
    def _calculate_all_investments(self):
        """
        Calculate investment details for each month's contribution.
        Each month's investment grows until the end of the investment period.
        
        Returns:
            list: Investment details for each month
        """
        details = []
        
        for month_invested in range(1, self.total_months + 1):
            investment_amount = self.monthly_investments[month_invested - 1]
            months_growing = self.total_months - month_invested + 1
            
            # Calculate final value of this month's investment
            final_value = investment_amount * (1 + self.monthly_return_rate) ** (months_growing - 1)
            
            # Calculate inflation-adjusted investment amount
            inflation_adjusted_amount = investment_amount * (1 + self.monthly_inflation_rate) ** (months_growing - 1)
            
            # Calculate real profit (after inflation)
            real_profit = max(0, final_value - inflation_adjusted_amount)
            
            # Calculate taxes on real profit
            taxes = real_profit * self.tax_rate
            
            # Calculate profit after tax
            profit_after_tax = real_profit - taxes
            
            # Calculate net value after tax
            net_value_after_tax = final_value - taxes
            
            month_data = {
                'month_invested': month_invested,
                'investment_amount': investment_amount,
                'months_growing': months_growing,
                'final_value': final_value,
                'inflation_adjusted_amount': inflation_adjusted_amount,
                'real_profit': real_profit,
                'taxes': taxes,
                'profit_after_tax': profit_after_tax,
                'net_value_after_tax': net_value_after_tax,
                'return_multiple': final_value / investment_amount if investment_amount > 0 else 0
            }
            
            details.append(month_data)
        
        return details
    
    def get_month_details(self, month):
        """
        Get investment details for a specific month.
        
        Args:
            month (int): Month number (1-based)
            
        Returns:
            dict: Month investment details or None if month doesn't exist
        """
        if month <= 0 or month > self.total_months:
            return None
        
        return self.investment_details[month - 1]
    
    def get_summary(self):
        """
        Get comprehensive summary of all investments.
        
        Returns:
            dict: Complete investment summary
        """
        if not self.investment_details:
            return {
                'total_months': 0,
                'total_invested': 0,
                'total_final_value': 0,
                'total_inflation_adjusted': 0,
                'total_real_profit': 0,
                'total_taxes': 0,
                'total_profit_after_tax': 0,
                'total_net_value_after_tax': 0,
                'effective_annual_return_before_tax': 0,
                'effective_annual_return_after_tax': 0,
                'monthly_details': []
            }
        
        # Calculate totals
        total_invested = sum(detail['investment_amount'] for detail in self.investment_details)
        total_final_value = sum(detail['final_value'] for detail in self.investment_details)
        total_inflation_adjusted = sum(detail['inflation_adjusted_amount'] for detail in self.investment_details)
        total_real_profit = sum(detail['real_profit'] for detail in self.investment_details)
        total_taxes = sum(detail['taxes'] for detail in self.investment_details)
        total_profit_after_tax = sum(detail['profit_after_tax'] for detail in self.investment_details)
        total_net_value_after_tax = sum(detail['net_value_after_tax'] for detail in self.investment_details)
        
        # Calculate effective annual returns
        years = self.total_months / 12
        if years > 0 and total_invested > 0:
            effective_annual_return_before_tax = (total_final_value / total_invested) ** (1/years) - 1
            effective_annual_return_after_tax = (total_net_value_after_tax / total_invested) ** (1/years) - 1
        else:
            effective_annual_return_before_tax = 0
            effective_annual_return_after_tax = 0
        
        summary = {
            'total_months': self.total_months,
            'investment_period_years': years,
            'total_invested': total_invested,
            'total_final_value': total_final_value,
            'total_inflation_adjusted': total_inflation_adjusted,
            'total_real_profit': total_real_profit,
            'total_taxes': total_taxes,
            'total_profit_after_tax': total_profit_after_tax,
            'total_net_value_after_tax': total_net_value_after_tax,
            'effective_annual_return_before_tax': effective_annual_return_before_tax,
            'effective_annual_return_after_tax': effective_annual_return_after_tax,
            'annual_return_rate': self.annual_return_rate,
            'annual_inflation_rate': self.annual_inflation_rate,
            'tax_rate': self.tax_rate,
            'monthly_details': self.investment_details.copy()
        }
        
        return summary
    
    def print_summary(self):
        """Print a formatted summary of all investments."""
        summary = self.get_summary()
        
        if summary['total_months'] == 0:
            print("No investments to analyze.")
            return
        
        print(f"\n{'='*80}")
        print(f"STOCK INVESTMENT ANALYSIS")
        print(f"{'='*80}")
        print(f"Investment Period: {summary['total_months']} months ({summary['investment_period_years']:.1f} years)")
        print(f"Annual Return Rate: {summary['annual_return_rate']:.1%}")
        print(f"Annual Inflation Rate: {summary['annual_inflation_rate']:.1%}")
        print(f"Tax Rate on Real Profits: {summary['tax_rate']:.1%}")
        
        print(f"\n{'OVERALL SUMMARY':-^80}")
        print(f"Total Amount Invested: ${summary['total_invested']:,.2f}")
        print(f"Total Inflation-Adjusted Investment: ${summary['total_inflation_adjusted']:,.2f}")
        print(f"Total Final Value: ${summary['total_final_value']:,.2f}")
        print(f"Total Real Profit (after inflation): ${summary['total_real_profit']:,.2f}")
        print(f"Total Taxes on Real Profit: ${summary['total_taxes']:,.2f}")
        print(f"Total Profit After Tax: ${summary['total_profit_after_tax']:,.2f}")
        print(f"Total Net Value After Tax: ${summary['total_net_value_after_tax']:,.2f}")
        print(f"Effective Annual Return (before tax): {summary['effective_annual_return_before_tax']:.2%}")
        print(f"Effective Annual Return (after tax): {summary['effective_annual_return_after_tax']:.2%}")
        
        print(f"\n{'MONTHLY INVESTMENT BREAKDOWN':-^80}")
        print(f"{'Month':<6} {'Invested':<10} {'Months':<7} {'Final':<12} {'Inflation':<12} {'Real':<10} {'Taxes':<8} {'Net After':<12}")
        print(f"{'Inv.':<6} {'Amount':<10} {'Growing':<7} {'Value':<12} {'Adjusted':<12} {'Profit':<10} {'':<8} {'Tax':<12}")
        print(f"{'-'*6} {'-'*10} {'-'*7} {'-'*12} {'-'*12} {'-'*10} {'-'*8} {'-'*12}")
        
        for detail in summary['monthly_details']:
            print(f"{detail['month_invested']:<6} "
                  f"${detail['investment_amount']:<9,.0f} "
                  f"{detail['months_growing']:<7} "
                  f"${detail['final_value']:<11,.0f} "
                  f"${detail['inflation_adjusted_amount']:<11,.0f} "
                  f"${detail['real_profit']:<9,.0f} "
                  f"${detail['taxes']:<7,.0f} "
                  f"${detail['net_value_after_tax']:<11,.0f}")
    
    def print_month_details(self, month):
        """Print detailed information for a specific month's investment."""
        details = self.get_month_details(month)
        if not details:
            print(f"Month {month} not found. Valid months: 1-{self.total_months}")
            return
        
        print(f"\n{'='*50}")
        print(f"MONTH {month} INVESTMENT DETAILS")
        print(f"{'='*50}")
        print(f"Investment Amount: ${details['investment_amount']:,.2f}")
        print(f"Months Growing: {details['months_growing']} months")
        print(f"Growth Multiple: {details['return_multiple']:.3f}x")
        print(f"Final Value: ${details['final_value']:,.2f}")
        print(f"Inflation-Adjusted Amount: ${details['inflation_adjusted_amount']:,.2f}")
        print(f"Real Profit (after inflation): ${details['real_profit']:,.2f}")
        print(f"Taxes (25% of real profit): ${details['taxes']:,.2f}")
        print(f"Profit After Tax: ${details['profit_after_tax']:,.2f}")
        print(f"Net Value After Tax: ${details['net_value_after_tax']:,.2f}")


# Example usage:
if __name__ == "__main__":
    # Define the complete investment sequence
    monthly_amounts = [1000, 1000, 1000, 1200, 1200, 1500, 1500, 1500, 1000, 1000, 1000, 1000]
    
    # Create investment object with all investments known upfront
    investment = StockInvestment(
        monthly_investments=monthly_amounts,
        annual_return_rate=0.07,  # 7% annual return
        annual_inflation_rate=0.03,  # 3% annual inflation
        tax_rate=0.25  # 25% tax on real profits
    )
    
    # Print comprehensive summary
    investment.print_summary()
    
    # Get details for specific months
    print(f"\n{'SPECIFIC MONTH EXAMPLES':-^80}")
    investment.print_month_details(1)  # First month investment
    investment.print_month_details(6)  # Middle month investment
    investment.print_month_details(12)  # Last month investment
    
    # Get summary data programmatically
    summary = investment.get_summary()
    print(f"\nProgrammatic access example:")
    print(f"Total return after tax: {summary['effective_annual_return_after_tax']:.2%}")

    def plot_investment_analysis(self, figsize=(15, 12)):
        """
        Create comprehensive plots showing all investment parameters.
        
        Args:
            figsize (tuple): Figure size for the plots
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            print("Error: matplotlib is required for plotting. Install with: pip install matplotlib")
            return
        
        # Prepare data for plotting
        months = [detail['month_invested'] for detail in self.investment_details]
        invested_amounts = [detail['investment_amount'] for detail in self.investment_details]
        final_values = [detail['final_value'] for detail in self.investment_details]
        inflation_adjusted = [detail['inflation_adjusted_amount'] for detail in self.investment_details]
        real_profits = [detail['real_profit'] for detail in self.investment_details]
        taxes = [detail['taxes'] for detail in self.investment_details]
        profits_after_tax = [detail['profit_after_tax'] for detail in self.investment_details]
        net_values_after_tax = [detail['net_value_after_tax'] for detail in self.investment_details]
        months_growing = [detail['months_growing'] for detail in self.investment_details]
        
        # Create subplots
        fig, axes = plt.subplots(2, 3, figsize=figsize)
        fig.suptitle(f'Stock Investment Analysis - {self.total_months} Month Period\n'
                    f'Annual Return: {self.annual_return_rate:.1%}, '
                    f'Inflation: {self.annual_inflation_rate:.1%}, '
                    f'Tax Rate: {self.tax_rate:.1%}', 
                    fontsize=14, fontweight='bold')
        
        # Plot 1: Investment Amount vs Final Value
        axes[0, 0].bar(months, invested_amounts, alpha=0.7, label='Invested Amount', color='lightblue')
        axes[0, 0].bar(months, final_values, alpha=0.7, label='Final Value', color='darkblue')
        axes[0, 0].set_title('Investment Amount vs Final Value by Month')
        axes[0, 0].set_xlabel('Month Invested')
        axes[0, 0].set_ylabel('Amount ($)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Growth Period Effect
        axes[0, 1].scatter(months_growing, final_values, c=invested_amounts, cmap='viridis', s=100, alpha=0.7)
        axes[0, 1].set_title('Final Value vs Growth Period')
        axes[0, 1].set_xlabel('Months Growing')
        axes[0, 1].set_ylabel('Final Value ($)')
        axes[0, 1].grid(True, alpha=0.3)
        cbar1 = plt.colorbar(axes[0, 1].collections[0], ax=axes[0, 1])
        cbar1.set_label('Investment Amount ($)')
        
        # Plot 3: Real Profit Analysis
        axes[0, 2].bar(months, real_profits, alpha=0.7, label='Real Profit', color='green')
        axes[0, 2].bar(months, taxes, alpha=0.7, label='Taxes', color='red')
        axes[0, 2].set_title('Real Profit and Taxes by Month')
        axes[0, 2].set_xlabel('Month Invested')
        axes[0, 2].set_ylabel('Amount ($)')
        axes[0, 2].legend()
        axes[0, 2].grid(True, alpha=0.3)
        
        # Plot 4: Inflation Impact
        axes[1, 0].plot(months, invested_amounts, 'o-', label='Original Investment', linewidth=2, markersize=6)
        axes[1, 0].plot(months, inflation_adjusted, 's-', label='Inflation Adjusted', linewidth=2, markersize=6)
        axes[1, 0].plot(months, final_values, '^-', label='Final Value', linewidth=2, markersize=6)
        axes[1, 0].set_title('Inflation Impact on Investment Value')
        axes[1, 0].set_xlabel('Month Invested')
        axes[1, 0].set_ylabel('Amount ($)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 5: After-Tax Analysis
        axes[1, 1].bar(months, final_values, alpha=0.5, label='Before Tax', color='lightcoral')
        axes[1, 1].bar(months, net_values_after_tax, alpha=0.8, label='After Tax', color='darkred')
        axes[1, 1].set_title('Value Before vs After Tax')
        axes[1, 1].set_xlabel('Month Invested')
        axes[1, 1].set_ylabel('Amount ($)')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        # Plot 6: Return Multiple by Month
        return_multiples = [detail['return_multiple'] for detail in self.investment_details]
        colors = ['red' if x < 1 else 'green' for x in return_multiples]
        axes[1, 2].bar(months, return_multiples, alpha=0.7, color=colors)
        axes[1, 2].axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Break-even')
        axes[1, 2].set_title('Return Multiple by Month Invested')
        axes[1, 2].set_xlabel('Month Invested')
        axes[1, 2].set_ylabel('Return Multiple (Final/Initial)')
        axes[1, 2].legend()
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_cumulative_analysis(self, figsize=(12, 8)):
        """
        Create cumulative analysis plots showing totals over time.
        
        Args:
            figsize (tuple): Figure size for the plots
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            print("Error: matplotlib is required for plotting. Install with: pip install matplotlib")
            return
        
        # Calculate cumulative values
        months = list(range(1, self.total_months + 1))
        cumulative_invested = []
        cumulative_final_value = []
        cumulative_real_profit = []
        cumulative_taxes = []
        cumulative_net_after_tax = []
        
        for i in range(self.total_months):
            cumulative_invested.append(sum(detail['investment_amount'] 
                                         for detail in self.investment_details[:i+1]))
            cumulative_final_value.append(sum(detail['final_value'] 
                                            for detail in self.investment_details[:i+1]))
            cumulative_real_profit.append(sum(detail['real_profit'] 
                                            for detail in self.investment_details[:i+1]))
            cumulative_taxes.append(sum(detail['taxes'] 
                                      for detail in self.investment_details[:i+1]))
            cumulative_net_after_tax.append(sum(detail['net_value_after_tax'] 
                                               for detail in self.investment_details[:i+1]))
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Cumulative Investment Analysis', fontsize=14, fontweight='bold')
        
        # Plot 1: Cumulative Investment Growth
        axes[0, 0].plot(months, cumulative_invested, 'o-', label='Total Invested', linewidth=2, markersize=4)
        axes[0, 0].plot(months, cumulative_final_value, 's-', label='Total Final Value', linewidth=2, markersize=4)
        axes[0, 0].plot(months, cumulative_net_after_tax, '^-', label='Total After Tax', linewidth=2, markersize=4)
        axes[0, 0].set_title('Cumulative Investment Growth')
        axes[0, 0].set_xlabel('Month')
        axes[0, 0].set_ylabel('Cumulative Amount ($)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Cumulative Profit and Taxes
        axes[0, 1].fill_between(months, cumulative_real_profit, alpha=0.7, label='Real Profit', color='green')
        axes[0, 1].fill_between(months, cumulative_taxes, alpha=0.7, label='Taxes', color='red')
        axes[0, 1].set_title('Cumulative Profit and Taxes')
        axes[0, 1].set_xlabel('Month')
        axes[0, 1].set_ylabel('Cumulative Amount ($)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Monthly Investment Pattern
        monthly_amounts = [detail['investment_amount'] for detail in self.investment_details]
        axes[1, 0].bar(months, monthly_amounts, alpha=0.7, color='lightblue')
        axes[1, 0].set_title('Monthly Investment Pattern')
        axes[1, 0].set_xlabel('Month')
        axes[1, 0].set_ylabel('Investment Amount ($)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Effective Return Rate Over Time
        effective_returns = []
        for i in range(self.total_months):
            if cumulative_invested[i] > 0:
                months_elapsed = i + 1
                if months_elapsed >= 12:  # Only calculate for periods >= 1 year
                    years = months_elapsed / 12
                    eff_return = (cumulative_net_after_tax[i] / cumulative_invested[i]) ** (1/years) - 1
                    effective_returns.append(eff_return)
                else:
                    effective_returns.append(0)
            else:
                effective_returns.append(0)
        
        axes[1, 1].plot(months, effective_returns, 'o-', linewidth=2, markersize=4)
        axes[1, 1].set_title('Effective Annual Return Over Time')
        axes[1, 1].set_xlabel('Month')
        axes[1, 1].set_ylabel('Effective Annual Return')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


# Example usage:
if __name__ == "__main__":
    # Define the complete investment sequence
    monthly_amounts = [1000, 1000, 1000, 1200, 1200, 1500, 1500, 1500, 1000, 1000, 1000, 1000]
    
    # Create investment object with all investments known upfront
    investment = StockInvestment(
        monthly_investments=monthly_amounts,
        annual_return_rate=0.07,  # 7% annual return
        annual_inflation_rate=0.03,  # 3% annual inflation
        tax_rate=0.25  # 25% tax on real profits
    )
    
    # Print comprehensive summary
    investment.print_summary()
    
    # Get details for specific months
    print(f"\n{'SPECIFIC MONTH EXAMPLES':-^80}")
    investment.print_month_details(1)  # First month investment
    investment.print_month_details(6)  # Middle month investment
    investment.print_month_details(12)  # Last month investment
    
    # Get summary data programmatically
    summary = investment.get_summary()
    print(f"\nProgrammatic access example:")
    print(f"Total return after tax: {summary['effective_annual_return_after_tax']:.2%}")