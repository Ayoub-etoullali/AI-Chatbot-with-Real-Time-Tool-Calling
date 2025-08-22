from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load CSV once when the app starts
stock_df = pd.read_csv("../data/docs/csv/stock_data.csv")

@app.route("/search_product", methods=["GET"])
def search_product():
    """
    Endpoint: /search_product?query=headphones
    Returns products whose name contains the query string (case-insensitive).
    """
    query = request.args.get("query")
    
    if not query:
        return jsonify({"error": "Please provide a search query, e.g., ?query=headphones"}), 400

    # Filter products containing the query (case-insensitive)
    filtered = stock_df[stock_df["name"].str.contains(query, case=False, na=False)]

    if filtered.empty:
        return jsonify({"error": f"No products found matching '{query}'"}), 404

    # Convert filtered rows to dictionary list
    result = filtered.to_dict(orient="records")
    
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)