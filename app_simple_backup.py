# -*- coding: utf-8 -*-
"""
Indian Trademark Registry Search Tool - Flask Web Application (Railway-compatible version)
Simplified version that gracefully handles missing Chrome/Selenium
"""

from flask import Flask, render_template, request, jsonify, session, send_file, flash, redirect, url_for
import os
import uuid
import threading
import time
from datetime import datetime
import base64
from io import BytesIO
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global dictionary to store user sessions
user_sessions = {}
session_lock = threading.Lock()

def cleanup_old_sessions():
    """Clean up old sessions periodically"""
    with session_lock:
        current_time = time.time()
        sessions_to_remove = []
        for session_id, data in user_sessions.items():
            if current_time - data.get('last_activity', 0) > 3600:  # 1 hour timeout
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            if session_id in user_sessions:
                del user_sessions[session_id]

def get_or_create_session():
    """Get or create user session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_id = session['user_id']
    
    with session_lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                'scraper': None,
                'last_activity': time.time(),
                'search_results': [],
                'status': 'idle'
            }
        else:
            user_sessions[user_id]['last_activity'] = time.time()
    
    return user_id

@app.route('/')
def index():
    """Main page"""
    cleanup_old_sessions()
    user_id = get_or_create_session()
    return render_template('index.html')

@app.route('/start_search', methods=['POST'])
def start_search():
    """Initialize browser and load CAPTCHA"""
    user_id = get_or_create_session()
    
    try:
        # Check if Selenium is available
        try:
            from utils.scraper import TrademarkScraper
            selenium_available = True
        except ImportError as e:
            selenium_available = False
            return jsonify({
                'success': False, 
                'message': 'Search functionality is not available yet. Chrome/Selenium dependencies are being installed. Please try again in a few minutes.'
            })
        
        data = request.get_json()
        wordmark = data.get('wordmark', '').strip()
        trademark_class = data.get('class', '').strip()
        filter_type = data.get('filter', 'Contains')
        
        if not wordmark:
            return jsonify({'success': False, 'message': 'Wordmark is required'})
        
        with session_lock:
            # Clean up existing scraper if any
            if user_sessions[user_id]['scraper']:
                user_sessions[user_id]['scraper'].cleanup()
            
            # Create new scraper
            scraper = TrademarkScraper()
            user_sessions[user_id]['scraper'] = scraper
            user_sessions[user_id]['status'] = 'initializing'
        
        # Initialize browser in background thread
        def initialize_browser():
            try:
                captcha_data = scraper.initialize_browser(wordmark, trademark_class, filter_type)
                with session_lock:
                    user_sessions[user_id]['status'] = 'captcha_ready'
                    user_sessions[user_id]['captcha_data'] = captcha_data
            except Exception as e:
                with session_lock:
                    user_sessions[user_id]['status'] = 'error'
                    user_sessions[user_id]['error_message'] = str(e)
        
        thread = threading.Thread(target=initialize_browser)
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Initializing browser...'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/get_status')
def get_status():
    """Get current status and CAPTCHA if ready"""
    user_id = get_or_create_session()
    
    with session_lock:
        session_data = user_sessions.get(user_id, {})
        status = session_data.get('status', 'idle')
        
        response = {'status': status}
        
        if status == 'captcha_ready':
            captcha_data = session_data.get('captcha_data')
            if captcha_data:
                response['captcha'] = captcha_data
        elif status == 'error':
            response['error'] = session_data.get('error_message', 'Unknown error')
        elif status == 'searching':
            response['progress'] = session_data.get('progress', 0)
            response['message'] = session_data.get('progress_message', 'Searching...')
        elif status == 'complete':
            response['results_count'] = len(session_data.get('search_results', []))
    
    return jsonify(response)

@app.route('/submit_search', methods=['POST'])
def submit_search():
    """Submit search with CAPTCHA"""
    return jsonify({'success': False, 'message': 'Search functionality will be available after Chrome installation completes'})

@app.route('/get_results')
def get_results():
    """Get search results for display"""
    return jsonify({'success': True, 'results': [], 'total_count': 0})

@app.route('/export_excel')
def export_excel():
    """Export results to Excel with embedded images"""
    flash('Excel export will be available after search functionality is ready', 'info')
    return redirect(url_for('index'))

@app.route('/reset_search', methods=['POST'])
def reset_search():
    """Reset current search session"""
    user_id = get_or_create_session()
    
    try:
        with session_lock:
            # Reset session data
            user_sessions[user_id] = {
                'scraper': None,
                'last_activity': time.time(),
                'search_results': [],
                'status': 'idle'
            }
        
        return jsonify({'success': True, 'message': 'Search reset successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    
    # Check if Selenium dependencies are available
    try:
        import selenium
        from selenium import webdriver
        selenium_status = "available"
    except ImportError:
        selenium_status = "installing"
    
    try:
        import openpyxl
        excel_status = "available"
    except ImportError:
        excel_status = "missing"
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len(user_sessions),
        'selenium': selenium_status,
        'excel': excel_status,
        'message': 'Web interface ready. Search functionality will be available once Chrome installation completes.'
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # For development only
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)