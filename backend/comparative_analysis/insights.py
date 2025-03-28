from compare import compare_companies

def generate_insights(sentiment_data):
    """Generate insights from comparative sentiment analysis."""
    insights = []

    sorted_companies = sorted(sentiment_data.items(), key=lambda x: x[1], reverse=True)
    best_performing = sorted_companies[0]
    worst_performing = sorted_companies[-1]

    insights.append(f"The company with the highest positive sentiment: {best_performing[0]} ({best_performing[1]:.2f})")
    insights.append(f"The company with the lowest sentiment: {worst_performing[0]} ({worst_performing[1]:.2f})")

    avg_sentiment = sum(sentiment_data.values()) / len(sentiment_data)
    insights.append(f"Overall industry sentiment: {'Positive' if avg_sentiment > 0 else 'Negative' if avg_sentiment < 0 else 'Neutral'} ({avg_sentiment:.2f})")

    return insights


if __name__ == "__main__":
    companies = ["Google", "Microsoft", "Apple", "Amazon", "Meta"]
    sentiment_data = compare_companies(companies)
    insights = generate_insights(sentiment_data)
    
    for insight in insights:
        print(insight)
