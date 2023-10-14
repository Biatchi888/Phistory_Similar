import json
from django.shortcuts import render
from pymongo import MongoClient
import re
import numpy as np

# Initialize the MongoDB client
client = MongoClient('mongodb+srv://capstonesummer1:9Q8SkkzyUPhEKt8i@cluster0.5gsgvlz.mongodb.net/')
db = client['Product_Comparison_System']
collection = db['Sept_Final']

def format_price(price_str):
    # Clean the price by removing non-numeric characters and the peso sign (₱)
    cleaned_price_str = re.sub(r'[^\d.]', '', price_str)

    if cleaned_price_str:
        # Convert the cleaned price string to a float, preserving decimal points
        return float(cleaned_price_str)

    return 0.0

def calculate_price_per_product(price_str):
    # Calculate the price per product for prices in the format "X for Y.YY"
    match = re.match(r'(\d+)\s+for\s+(\d+\.\d+)', price_str)
    
    if match:
        # Skip prices with the specified format
        return None

    # For other formats, return the cleaned price
    return format_price(price_str)


def calculate_total_price_per_supermarket(data):
    # Create a dictionary to store the total prices for each supermarket
    total_prices_per_supermarket = {}

    for item in data:
        supermarket = item['supermarket']
        price = item['original_price']

        if supermarket not in total_prices_per_supermarket:
            total_prices_per_supermarket[supermarket] = price
        else:
            total_prices_per_supermarket[supermarket] += price

    return total_prices_per_supermarket

def calculate_price_stats(data):
    # Create a dictionary to store price statistics for each supermarket and category
    price_stats = {}

    for item in data:
        supermarket = item['supermarket']
        category = item['category']
        price = item['original_price']

        if supermarket not in price_stats:
            price_stats[supermarket] = {}

        if category not in price_stats[supermarket]:
            price_stats[supermarket][category] = []

        price_stats[supermarket][category].append(price)

    # Calculate summary statistics (min, max, median) for each supermarket and category
    for supermarket, categories in price_stats.items():
        for category, prices in categories.items():
            min_price = min(prices)
            max_price = max(prices)
            median_price = np.median(prices)

            price_stats[supermarket][category] = {
                'min_price': min_price,
                'max_price': max_price,
                'median_price': median_price,
            }

    return price_stats


def calculate_discounted_vs_regular_prices(data):
    # Create a dictionary to store the sum of discounted and regular prices for each category in each supermarket
    discounted_vs_regular_prices = {}

    for item in data:
        supermarket = item['supermarket']
        category = item['category']
        original_price = item['original_price']
        discounted_price = item.get('discounted_price', 0.0)

        if supermarket not in discounted_vs_regular_prices:
            discounted_vs_regular_prices[supermarket] = {}

        if category not in discounted_vs_regular_prices[supermarket]:
            discounted_vs_regular_prices[supermarket][category] = {
                'regular_price_sum': 0.0,
                'discounted_price_sum': 0.0,
            }

        discounted_vs_regular_prices[supermarket][category]['regular_price_sum'] += original_price
        discounted_vs_regular_prices[supermarket][category]['discounted_price_sum'] += discounted_price

    return discounted_vs_regular_prices
def chart1(request):
    # Fetch the data from MongoDB
    data = list(collection.find({}, {'supermarket': 1, 'category': 1, 'original_price': 1, 'discounted_price': 1, 'title': 1}))

    # Clean and format the 'original_price' field (remove the '₱' sign)
    for item in data:
        original_price = item['original_price']
        discounted_price = item.get('discounted_price', None)

        # Calculate price per product for prices in the format "X for Y.YY"
        price_per_product = calculate_price_per_product(original_price)
        price_per_product_discounted = calculate_price_per_product(discounted_price) if discounted_price else None

        if price_per_product is not None:
            # Use the calculated price per product
            item['original_price'] = price_per_product
        
        if price_per_product_discounted is not None:
            # Use the calculated price per product for discounted price
            item['discounted_price'] = price_per_product_discounted

#PRICES CHART--------------------------------------------------------------------

    # Create a dictionary to store total prices for each category in each supermarket
    category_prices = {}

    for item in data:
        supermarket = item['supermarket']
        category = item['category']
        price = item['original_price']

        if supermarket not in category_prices:
            category_prices[supermarket] = {}

        if category not in category_prices[supermarket]:
            category_prices[supermarket][category] = 0.0

        category_prices[supermarket][category] += price

    # Get a list of unique supermarkets
    supermarkets = list(category_prices.keys())

    # Create a dictionary to store the bar chart data for each supermarket
    bar_chart_data = {}

    # Add a special case for "all" to include total prices across all supermarkets
    all_categories = list(set(category for supermarket_data in category_prices.values() for category in supermarket_data.keys()))
    all_total_prices = [sum(supermarket_data[category] for supermarket_data in category_prices.values() if category in supermarket_data) for category in all_categories]
    bar_chart_data['all'] = {
        'categories': all_categories,
        'total_prices': all_total_prices,
    }

    for supermarket in supermarkets:
        categories = list(category_prices[supermarket].keys())
        total_prices = list(category_prices[supermarket].values())

        bar_chart_data[supermarket] = {
            'categories': categories,
            'total_prices': total_prices,
        }

    # Convert the data for the bar chart to JSON format for JavaScript
    bar_chart_data_json = json.dumps(bar_chart_data)

    # Calculate total prices per supermarket for the pie chart
    total_prices_per_supermarket = calculate_total_price_per_supermarket(data)
    # Convert the data for the pie chart to JSON format for JavaScript
    total_prices_json = json.dumps(total_prices_per_supermarket)


#2 DOUGHNUT CHART-----------------------------------------------------------------------------------------------------
    # Create a dictionary to store category counts for the doughnut chart
    doughnut_chart_data = {}

    # Add a special case for "all" to include the total number of products across all supermarkets
    all_category_counts = [len(data)]
    doughnut_chart_data['all'] = {
        'categories': ['All Products'],
        'category_counts': all_category_counts,
    }

    for supermarket in supermarkets:
        categories = list(category_prices[supermarket].keys())
        category_counts = [len([item for item in data if item['supermarket'] == supermarket and item['category'] == category]) for category in categories]

        doughnut_chart_data[supermarket] = {
            'categories': categories,
            'category_counts': category_counts,
        }


      # Create a dictionary to store the count of products for each category in each supermarket
    category_counts = {}

    for item in data:
        supermarket = item['supermarket']
        category = item['category']

        if supermarket not in category_counts:
            category_counts[supermarket] = {}

        if category not in category_counts[supermarket]:
            category_counts[supermarket][category] = 0

        category_counts[supermarket][category] += 1

    # Get a list of unique supermarkets
    supermarkets = list(category_counts.keys())

    # Create a dictionary to store the doughnut chart data
    doughnut_chart_data = {}

    # Add a special case for "all" to include the total number of products across all supermarkets
    all_category_counts = [sum(counts.values()) for counts in category_counts.values()]
    doughnut_chart_data['all'] = {
        'categories': supermarkets,
        'category_counts': all_category_counts,
    }

    for supermarket in supermarkets:
        categories = list(category_counts[supermarket].keys())
        category_counts_list = [category_counts[supermarket][category] for category in categories]

        doughnut_chart_data[supermarket] = {
            'categories': categories,
            'category_counts': category_counts_list,
        }

    # Convert the data for the doughnut chart to JSON format for JavaScript
    doughnut_chart_data_json = json.dumps(doughnut_chart_data)

    # Convert the data for the doughnut chart to JSON format for JavaScript
    doughnut_chart_data_json = json.dumps(doughnut_chart_data)
#3 HORIZONTAL CHART---------------------------------------------------------------------------------------------------------------------------


# Create a dictionary to store the count of products with discounts for each category in each supermarket
    category_discount_counts = {}

    for item in data:
        supermarket = item['supermarket']
        category = item['category']
        has_discount = 'discounted_price' in item and item['discounted_price'] is not None

        if supermarket not in category_discount_counts:
            category_discount_counts[supermarket] = {}

        if category not in category_discount_counts[supermarket]:
            category_discount_counts[supermarket][category] = 0

        if has_discount:
            category_discount_counts[supermarket][category] += 1

    # Get a list of unique supermarkets
    supermarkets = list(category_discount_counts.keys())

    # Create a dictionary to store the horizontal bar chart data
    horizontal_bar_chart_data = {}

    # Add a special case for "all" to include total counts of products with discounts across all supermarkets
    all_category_discount_counts = [sum(counts.values()) for counts in category_discount_counts.values()]
    horizontal_bar_chart_data['all'] = {
        'categories': supermarkets,
        'category_discount_counts': all_category_discount_counts,
    }

    for supermarket in supermarkets:
        categories = list(category_discount_counts[supermarket].keys())
        category_discount_counts_list = [category_discount_counts[supermarket][category] for category in categories]

        horizontal_bar_chart_data[supermarket] = {
            'categories': categories,
            'category_discount_counts': category_discount_counts_list,
        }

    # Convert the data for the horizontal bar chart to JSON format for JavaScript
    horizontal_bar_chart_data_json = json.dumps(horizontal_bar_chart_data)


    # Convert the data for the horizontal stacked bar chart to JSON format for JavaScript
    context = {
        'bar_chart_data_json': bar_chart_data_json,
        'total_prices_json': total_prices_json,
        'doughnut_chart_data_json': doughnut_chart_data_json,  # Add doughnut chart data to the context
        'supermarkets': supermarkets,
        'horizontal_bar_chart_data_json':horizontal_bar_chart_data_json,
    }

    return render(request, 'charts/chart1.html', context)