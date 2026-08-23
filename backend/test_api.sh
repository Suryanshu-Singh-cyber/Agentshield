#!/bin/bash
# backend/test_api.sh
# Simple API test for CI/CD

set -e  # Exit on error

BASE_URL="http://127.0.0.1:8000"

echo "🚀 Running AgentShield API tests..."
echo "================================================"

# Test 1: Health check
echo ""
echo "📊 Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -f "$BASE_URL/health" || echo "FAILED")
if [[ "$HEALTH_RESPONSE" == "FAILED" ]]; then
    echo "❌ Health check failed"
    exit 1
else
    echo "✅ Health check passed"
fi

# Test 2: Generate tests
echo ""
echo "📝 Testing generate-tests endpoint..."
GENERATE_RESPONSE=$(curl -s -X POST "$BASE_URL/generate-tests" \
    -H "Content-Type: application/json" \
    -d '{"count": 5}' || echo "FAILED")
if [[ "$GENERATE_RESPONSE" == "FAILED" ]]; then
    echo "❌ Generate tests failed"
    exit 1
else
    echo "✅ Generate tests passed"
fi

# Test 3: Run tests
echo ""
echo "🏃 Testing run-tests endpoint..."
RUN_RESPONSE=$(curl -s -X POST "$BASE_URL/run-tests" || echo "FAILED")
if [[ "$RUN_RESPONSE" == "FAILED" ]]; then
    echo "❌ Run tests failed"
    exit 1
else
    echo "✅ Run tests passed"
fi

# All passed
echo ""
echo "================================================"
echo "✅ All tests passed! System is operational."
exit 0
