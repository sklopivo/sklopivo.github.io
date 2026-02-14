#!/bin/bash

# Sklopivo Brewing Statistics Refresh Script
# This script fetches the latest data from Brewfather and regenerates all statistics

set -e  # Exit on error

echo "🍺 Sklopivo Brewing Statistics Refresh"
echo "======================================"
echo ""

# Load credentials from environment variables
if [ -z "$BREWFATHER_USER_ID" ] || [ -z "$BREWFATHER_API_KEY" ]; then
    echo "❌ Error: Environment variables not set!"
    echo "   Please set BREWFATHER_USER_ID and BREWFATHER_API_KEY"
    echo ""
    echo "   For local development, create .env file:"
    echo "   cp .env.example .env"
    echo "   # Edit .env with your credentials"
    echo "   export \$(cat .env | xargs)"
    echo "   ./refresh_stats.sh"
    exit 1
fi

echo "✅ Using environment variables for credentials"
USER_ID="$BREWFATHER_USER_ID"
API_KEY="$BREWFATHER_API_KEY"

# Step 1: Fetch all batches
echo ""
echo "📥 Step 1/4: Fetching batch list from Brewfather API..."
curl -s -u "${USER_ID}:${API_KEY}" \
  "https://api.brewfather.app/v2/batches?limit=100" \
  -H "Accept: application/json" > brewfather_batches_all.json

BATCH_COUNT=$(jq 'length' brewfather_batches_all.json)
echo "   Found ${BATCH_COUNT} batches"

# Step 2: Fetch detailed batch information
echo ""
echo "📥 Step 2/4: Fetching detailed batch information..."
echo "   This may take a minute..."

batch_ids=$(jq -r '.[]._id' brewfather_batches_all.json)

echo "[" > detailed_batches_all.json
first=true
counter=0

for id in $batch_ids; do
  counter=$((counter + 1))

  # Progress indicator
  if [ $((counter % 5)) -eq 0 ]; then
    echo "   Progress: ${counter}/${BATCH_COUNT} batches..."
  fi

  if [ "$first" = false ]; then
    echo "," >> detailed_batches_all.json
  fi

  curl -s -u "${USER_ID}:${API_KEY}" \
    "https://api.brewfather.app/v2/batches/${id}?include=recipe" \
    -H "Accept: application/json" >> detailed_batches_all.json

  first=false
  sleep 0.3  # Be nice to the API
done

echo "]" >> detailed_batches_all.json
echo "   ✅ Fetched ${BATCH_COUNT} detailed batches"

# Step 3: Analyze data and generate reports
echo ""
echo "📊 Step 3/4: Analyzing brewing data..."
python3 analyze_brewing_data.py

# Step 4: Clean up temporary files
echo ""
echo "🧹 Step 4/4: Cleaning up..."
rm -f brewfather_batches_all.json

echo ""
echo "======================================"
echo "✅ Statistics refresh complete!"
echo ""
echo "📁 Generated files:"
echo "   - brewing_statistics.json (JSON data)"
echo "   - index.html (Web showcase)"
echo ""
echo "🌐 To view your showcase:"
echo "   open index.html"
echo ""
echo "🍻 Cheers!"
