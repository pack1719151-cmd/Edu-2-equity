#!/bin/bash

# EduEquity OS Test Runner Script
# Runs all tests for the project

set -e

echo "======================================"
echo "  EduEquity OS Test Runner"
echo "======================================"
echo ""

# Run all tests
echo "Running all tests..."
pnpm test

echo ""
echo "======================================"
echo "  All Tests Complete"
echo "======================================"

