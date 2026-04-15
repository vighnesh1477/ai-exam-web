from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Global storage for latest answer
latest_data = {
    "question": "",
    "options": ["", "", "", ""],
    "answer": "",
    "explanation": "",
    "timestamp": ""
}

@app.route('/')
def index():
    """Main page - serves your beautiful HTML"""
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    """
    API endpoint for your JavaScript to fetch data
    This matches your fetchData() function call to "/data"
    """
    return jsonify(latest_data)

@app.route('/update', methods=['POST'])
def update():
    """Receive data from main.py"""
    global latest_data
    
    try:
        data = request.get_json()
        
        # Validate and store data
        latest_data = {
            "question": data.get('question', '') or '',
            "options": data.get('options', ['', '', '', '']) or ['', '', '', ''],
            "answer": str(data.get('answer', '') or ''),
            "explanation": data.get('explanation', '') or '',
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        
        print(f"\n{'='*50}")
        print(f"📥 WEB SERVER RECEIVED UPDATE")
        print(f"{'='*50}")
        print(f"❓ Question: {latest_data['question'][:60]}...")
        print(f"🔤 Options: {len([o for o in latest_data['options'] if o])} received")
        print(f"✅ Answer: {latest_data['answer']}")
        print(f"💡 Explanation: {latest_data['explanation'][:60]}...")
        print(f"⏰ Time: {latest_data['timestamp']}")
        print(f"{'='*50}\n")
        
        return jsonify({
            "status": "success", 
            "message": "Data received and stored!",
            "timestamp": latest_data['timestamp']
        })
        
    except Exception as e:
        print(f"❌ Error processing update: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/health')
def health():
    """Health check endpoint for hosting platforms"""
    return jsonify({"status": "healthy", "service": "ai-exam-assistant"})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("\n" + "="*65)
    print("🌐 AI EXAM ASSISTANT - FLASK WEB SERVER")
    print("="*65)
    print("\n✅ Server Features:")
    print("   • Beautiful responsive UI (your design!)")
    print("   • Dark/Light theme toggle")
    print("   • Vertical/Horizontal layout")
    print("   • Auto-refresh every 2 seconds")
    print("   • Mobile optimized")
    print("\n📍 Endpoints:")
    print("   GET  /         → Main webpage")
    print("   GET  /data     → JSON data API (for your JS)")
    print("   POST /update   → Receive data from main.py")
    print("   GET  /health   → Health check")
    print("\n" + "="*65)
    
    # For local development
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )