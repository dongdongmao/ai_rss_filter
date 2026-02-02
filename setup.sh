#!/bin/bash
# setup.sh - Linux/Mac Quick Setup Script

echo ""
echo "========================================"
echo "  RSS Filter - Quick Setup"
echo "========================================"
echo ""

# Check Python
echo "✓ Checking Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "✗ Python not found, please install Python 3.8+"
    exit 1
fi

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
echo ""
echo "✓ Installing dependency packages..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check directories
echo ""
echo "✓ Checking directory structure..."
mkdir -p logs
mkdir -p data

echo ""
echo "========================================"
echo "  ✓ Setup complete!"
echo "========================================"
echo ""

echo "Next steps:"
echo ""
echo "1. Configure (optional): cp .env.example .env"
echo "2. Web app: python api.py  (then open http://localhost:7860)"
echo "3. CLI test: python main.py"
echo "4. Scheduler: python scheduler.py"
echo ""
