import os
import time
import random
from flask import Flask, request, jsonify, render_template
import logging
from threading import Thread

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Bot status storage
bot_status = {
    'running': False,
    'channel_url': '',
    'target': 0,
    'current': 0,
    'logs': []
}

def add_log(message):
    """Add log message"""
    timestamp = time.strftime('%H:%M:%S')
    bot_status['logs'].append(f"[{timestamp}] {message}")
    if len(bot_status['logs']) > 100:
        bot_status['logs'].pop(0)
    print(f"[{timestamp}] {message}")

class YouTubeBot:
    def __init__(self):
        self.running = False
    
    def subscribe(self, channel_url):
        """Simulate subscribing"""
        time.sleep(random.uniform(1, 3))
        return True
    
    def run(self, channel_url, target):
        """Main bot function"""
        bot_status['running'] = True
        bot_status['channel_url'] = channel_url
        bot_status['target'] = target
        bot_status['current'] = 0
        
        add_log("🚀 Bot started!")
        add_log(f"📺 Channel: {channel_url}")
        add_log(f"🎯 Target: {target} subscribers")
        
        for i in range(target):
            if not bot_status['running']:
                add_log("⏹️ Bot stopped by user")
                break
            
            # Add subscriber
            bot_status['current'] += 1
            add_log(f"✅ Subscriber #{bot_status['current']} added")
            
            # Calculate progress
            progress = (bot_status['current'] / target) * 100
            add_log(f"📊 Progress: {bot_status['current']}/{target} ({progress:.1f}%)")
            
            # Wait 10-20 seconds
            delay = random.randint(10, 20)
            add_log(f"⏱️ Waiting {delay} seconds...")
            
            for remaining in range(delay, 0, -1):
                if not bot_status['running']:
                    break
                time.sleep(1)
        
        add_log("✅ Bot finished!")
        bot_status['running'] = False

# Create bot instance
bot = YouTubeBot()

@app.route('/')
def home():
    """Home page with HTML interface"""
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_bot():
    """API endpoint to start bot"""
    if bot_status['running']:
        return jsonify({'error': 'Bot already running'}), 400
    
    data = request.json
    channel_url = data.get('channel_url', 'https://youtube.com/@channel')
    target = int(data.get('target', 50))
    
    # Clear old logs
    bot_status['logs'] = []
    
    # Start bot in background
    thread = Thread(target=bot.run, args=(channel_url, target))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Bot started',
        'channel': channel_url,
        'target': target
    })

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """API endpoint to stop bot"""
    bot_status['running'] = False
    return jsonify({
        'success': True,
        'message': 'Bot stopped',
        'current': bot_status['current']
    })

@app.route('/api/status')
def get_status():
    """API endpoint to get status"""
    return jsonify({
        'running': bot_status['running'],
        'channel': bot_status['channel_url'],
        'target': bot_status['target'],
        'current': bot_status['current'],
        'progress': f"{bot_status['current']}/{bot_status['target']}" if bot_status['target'] > 0 else "0/0",
        'percentage': round((bot_status['current']/bot_status['target']*100), 1) if bot_status['target'] > 0 else 0
    })

@app.route('/api/logs')
def get_logs():
    """API endpoint to get logs"""
    return jsonify({
        'logs': bot_status['logs']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)