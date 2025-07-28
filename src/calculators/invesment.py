class StockInvestment:
    """
    A class to calculate investment returns for monthly investments with inflation and tax considerations.
    """
    
    def __init__(self, monthly_investments, annual_return_rate, annual_inflation_rate=0.03, tax_rate=0.25):
        """
        Initialize the investment calculator.
        
        Args:
            monthly_investments (list): List of monthly investment amounts
            annual_return_rate (float): Annual return rate (e.g., 0.07 for 7%)
            annual_inflation_rate (float): Annual inflation rate (default 0.03 for 3%)
            tax_rate (float): Tax rate on real profits (default 0.25 for 25%)
        """
        self.monthly_investments = monthly_investments
        self.annual_return_rate = annual_return_rate
        self.annual_inflation_rate = annual_inflation_rate
        self.tax_rate = tax_rate
        self.total_months = len(monthly_investments)
        
        # Calculate all investment details
        self._calculate_all_investments()
    
    def _calculate_single_investment(self, month, investment_amount):
        """Calculate details for a single monthly investment.
        
        Args:
            month (int): Month number (1-based)
            investment_amount (float): Amount invested in this month
        
        Returns:
            dict: Investment details for this month
        """
        # Calculate months growing (how long this investment grows)
        months_growing = self.total_months - month + 1
        years_growing = months_growing / 12
        
        # Calculate final value with compound interest
        monthly_rate = self.annual_return_rate / 12
        final_value = investment_amount * ((1 + monthly_rate) ** months_growing)
        
        # Calculate inflation-adjusted amount
        inflation_adjusted_amount = investment_amount * ((1 + self.annual_inflation_rate) ** years_growing)
        
        # Calculate real profit (nominal profit minus inflation)
        nominal_profit = final_value - investment_amount
        real_profit = final_value - inflation_adjusted_amount
            
            # Calculate taxes on real profit
        taxes = real_profit * self.tax_rate if real_profit > 0 else 0
            
            # Calculate profit after tax
        profit_after_tax = real_profit - taxes
            
            # Calculate net value after tax
        net_value_after_tax = inflation_adjusted_amount + profit_after_tax
        
        # Calculate return multiple
        return_multiple = final_value / investment_amount
            
        return {
            'month_invested': month,
                'investment_amount': investment_amount,
                'months_growing': months_growing,
            'years_growing': years_growing,
                'final_value': final_value,
                'inflation_adjusted_amount': inflation_adjusted_amount,
            'nominal_profit': nominal_profit,
                'real_profit': real_profit,
                'taxes': taxes,
                'profit_after_tax': profit_after_tax,
                'net_value_after_tax': net_value_after_tax,
            'return_multiple': return_multiple
            }
            
    def _calculate_all_investments(self):
        """Calculate details for all monthly investments."""
        self.investment_details = []
        
        for month, investment_amount in enumerate(self.monthly_investments, 1):
            detail = self._calculate_single_investment(month, investment_amount)
            self.investment_details.append(detail)
    
    def get_month_details(self, month):
        """
        Get detailed information for a specific month's investment.
        
        Args:
            month (int): Month number (1-based)
            
        Returns:
            dict: Investment details for the specified month
        """
        if 1 <= month <= self.total_months:
            return self.investment_details[month - 1]
        else:
            raise ValueError(f"Month must be between 1 and {self.total_months}")
    
    def get_summary(self):
        """
        Get a summary of all investments.
        
        Returns:
            dict: Summary statistics
        """
        total_invested = sum(detail['investment_amount'] for detail in self.investment_details)
        total_final_value = sum(detail['final_value'] for detail in self.investment_details)
        total_inflation_adjusted = sum(detail['inflation_adjusted_amount'] for detail in self.investment_details)
        total_real_profit = sum(detail['real_profit'] for detail in self.investment_details)
        total_taxes = sum(detail['taxes'] for detail in self.investment_details)
        total_profit_after_tax = sum(detail['profit_after_tax'] for detail in self.investment_details)
        total_net_after_tax = sum(detail['net_value_after_tax'] for detail in self.investment_details)
        
        # Calculate effective annual return
        years = self.total_months / 12
        effective_annual_return = (total_final_value / total_invested) ** (1/years) - 1 if total_invested > 0 else 0
        effective_annual_return_after_tax = (total_net_after_tax / total_invested) ** (1/years) - 1 if total_invested > 0 else 0
        
        return {
            'total_invested': total_invested,
            'total_final_value': total_final_value,
            'total_inflation_adjusted': total_inflation_adjusted,
            'total_real_profit': total_real_profit,
            'total_taxes': total_taxes,
            'total_profit_after_tax': total_profit_after_tax,
            'total_net_after_tax': total_net_after_tax,
            'effective_annual_return': effective_annual_return,
            'effective_annual_return_after_tax': effective_annual_return_after_tax,
            'total_months': self.total_months,
            'annual_return_rate': self.annual_return_rate,
            'annual_inflation_rate': self.annual_inflation_rate,
            'tax_rate': self.tax_rate
        }
    
    def print_summary(self):
        """Print a comprehensive summary of all investments."""
        summary = self.get_summary()
        
        # print(f"\n{'INVESTMENT SUMMARY':-^80}")
        print(f"Total Period: {summary['total_months']} months ({summary['total_months']/12:.1f} years)")
        print(f"Annual Return Rate: {summary['annual_return_rate']:.1%}")
        print(f"Annual Inflation Rate: {summary['annual_inflation_rate']:.1%}")
        print(f"Tax Rate on Real Profits: {summary['tax_rate']:.1%}")
        
        print(f"\n{'AMOUNTS':-^80}")
        print(f"Total Invested: ${summary['total_invested']:,.2f}")
        print(f"Total Final Value (Nominal): ${summary['total_final_value']:,.2f}")
        print(f"Total Inflation-Adjusted Amount: ${summary['total_inflation_adjusted']:,.2f}")
        
        print(f"\n{'PROFIT ANALYSIS':-^80}")
        print(f"Total Real Profit: ${summary['total_real_profit']:,.2f}")
        print(f"Total Taxes: ${summary['total_taxes']:,.2f}")
        print(f"Total Profit After Tax: ${summary['total_profit_after_tax']:,.2f}")
        print(f"Total Net Value After Tax: ${summary['total_net_after_tax']:,.2f}")
        
        print(f"\n{'RETURN RATES':-^80}")
        print(f"Effective Annual Return (Nominal): {summary['effective_annual_return']:.2%}")
        print(f"Effective Annual Return (After Tax): {summary['effective_annual_return_after_tax']:.2%}")
        
        # Calculate some additional metrics
        nominal_return_multiple = summary['total_final_value'] / summary['total_invested']
        after_tax_return_multiple = summary['total_net_after_tax'] / summary['total_invested']
        
        print(f"\n{'RETURN MULTIPLES':-^80}")
        print(f"Nominal Return Multiple: {nominal_return_multiple:.2f}x")
        print(f"After-Tax Return Multiple: {after_tax_return_multiple:.2f}x")
        
        # Show inflation impact
        inflation_loss = summary['total_invested'] - summary['total_inflation_adjusted']
        print(f"\n{'INFLATION IMPACT':-^80}")
        print(f"Inflation Loss: ${inflation_loss:,.2f}")
        print(f"Real Return Rate: {summary['effective_annual_return_after_tax']:.2%}")
    
    def print_month_details(self, month):
        """
        Print detailed information for a specific month's investment.
        
        Args:
            month (int): Month number (1-based)
        """
        try:
            details = self.get_month_details(month)
            
            print(f"\n{'MONTH ' + str(month) + ' INVESTMENT DETAILS':-^80}")
            print(f"Investment Amount: ${details['investment_amount']:,.2f}")
            print(f"Months Growing: {details['months_growing']}")
            print(f"Years Growing: {details['years_growing']:.2f}")
            
            print(f"\n{'VALUES':-^80}")
            print(f"Final Value: ${details['final_value']:,.2f}")
            print(f"Inflation-Adjusted Amount: ${details['inflation_adjusted_amount']:,.2f}")
            print(f"Return Multiple: {details['return_multiple']:.2f}x")
            
            print(f"\n{'PROFIT ANALYSIS':-^80}")
            print(f"Nominal Profit: ${details['nominal_profit']:,.2f}")
            print(f"Real Profit (after inflation): ${details['real_profit']:,.2f}")
            print(f"Taxes (25% of real profit): ${details['taxes']:,.2f}")
            print(f"Profit After Tax: ${details['profit_after_tax']:,.2f}")
            print(f"Net Value After Tax: ${details['net_value_after_tax']:,.2f}")
            
        except ValueError as e:
            print(f"Error: {e}")