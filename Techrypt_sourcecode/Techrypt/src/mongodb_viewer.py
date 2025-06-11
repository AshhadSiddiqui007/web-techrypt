#!/usr/bin/env python3
"""
👁️ MONGODB VIEWER FOR TECHRYPT
Web-based database viewer and management interface
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
from mongodb_backend import TechryptMongoDBBackend

app = Flask(__name__)
CORS(app)

# Initialize MongoDB backend
db_backend = TechryptMongoDBBackend()

# HTML Template for the viewer
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Techrypt MongoDB Viewer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white; 
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .nav { 
            background: #34495e;
            padding: 0;
            display: flex;
            justify-content: center;
        }
        .nav button { 
            background: none;
            border: none;
            color: white;
            padding: 15px 30px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        .nav button:hover, .nav button.active { 
            background: #2c3e50;
        }
        .content { 
            padding: 30px;
            min-height: 400px;
        }
        .stats-grid { 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card { 
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .stat-card h3 { font-size: 2em; margin-bottom: 5px; }
        .stat-card p { opacity: 0.9; }
        .data-table { 
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .data-table th { 
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
        }
        .data-table td { 
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        .data-table tr:hover { background: #f8f9fa; }
        .loading { 
            text-align: center;
            padding: 50px;
            font-size: 1.2em;
            color: #666;
        }
        .error { 
            background: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .success { 
            background: #27ae60;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .json-view { 
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
        }
        .refresh-btn { 
            background: #27ae60;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 0;
        }
        .refresh-btn:hover { background: #229954; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗄️ Techrypt MongoDB Viewer</h1>
            <p>Real-time database monitoring and management</p>
        </div>
        
        <div class="nav">
            <button onclick="showSection('dashboard')" class="active" id="dashboard-btn">📊 Dashboard</button>
            <button onclick="showSection('users')" id="users-btn">👥 Users</button>
            <button onclick="showSection('appointments')" id="appointments-btn">📅 Appointments</button>
            <button onclick="showSection('conversations')" id="conversations-btn">💬 Conversations</button>
            <button onclick="showSection('analytics')" id="analytics-btn">📈 Analytics</button>
        </div>
        
        <div class="content">
            <div id="dashboard-section">
                <h2>📊 Database Overview</h2>
                <button class="refresh-btn" onclick="loadDashboard()">🔄 Refresh</button>
                <div id="stats-container" class="loading">Loading statistics...</div>
            </div>
            
            <div id="users-section" style="display: none;">
                <h2>👥 Users Management</h2>
                <button class="refresh-btn" onclick="loadUsers()">🔄 Refresh</button>
                <div id="users-container" class="loading">Loading users...</div>
            </div>
            
            <div id="appointments-section" style="display: none;">
                <h2>📅 Appointments Management</h2>
                <button class="refresh-btn" onclick="loadAppointments()">🔄 Refresh</button>
                <div id="appointments-container" class="loading">Loading appointments...</div>
            </div>
            
            <div id="conversations-section" style="display: none;">
                <h2>💬 Conversations History</h2>
                <button class="refresh-btn" onclick="loadConversations()">🔄 Refresh</button>
                <div id="conversations-container" class="loading">Loading conversations...</div>
            </div>
            
            <div id="analytics-section" style="display: none;">
                <h2>📈 Advanced Analytics</h2>
                <button class="refresh-btn" onclick="loadAnalytics()">🔄 Refresh</button>
                <div id="analytics-container" class="loading">Loading analytics...</div>
            </div>
        </div>
    </div>

    <script>
        let currentSection = 'dashboard';
        
        function showSection(section) {
            // Hide all sections
            document.querySelectorAll('[id$="-section"]').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.nav button').forEach(btn => btn.classList.remove('active'));
            
            // Show selected section
            document.getElementById(section + '-section').style.display = 'block';
            document.getElementById(section + '-btn').classList.add('active');
            
            currentSection = section;
            
            // Load data for the section
            switch(section) {
                case 'dashboard': loadDashboard(); break;
                case 'users': loadUsers(); break;
                case 'appointments': loadAppointments(); break;
                case 'conversations': loadConversations(); break;
                case 'analytics': loadAnalytics(); break;
            }
        }
        
        async function loadDashboard() {
            try {
                const response = await fetch('/api/statistics');
                const stats = await response.json();
                
                const statsHtml = `
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>${stats.total_users || 0}</h3>
                            <p>Total Users</p>
                        </div>
                        <div class="stat-card">
                            <h3>${stats.total_appointments || 0}</h3>
                            <p>Total Appointments</p>
                        </div>
                        <div class="stat-card">
                            <h3>${stats.total_conversations || 0}</h3>
                            <p>Total Conversations</p>
                        </div>
                        <div class="stat-card">
                            <h3>${stats.pending_appointments || 0}</h3>
                            <p>Pending Appointments</p>
                        </div>
                    </div>
                    <div class="success">✅ Database is connected and operational</div>
                    <div class="json-view">${JSON.stringify(stats, null, 2)}</div>
                `;
                
                document.getElementById('stats-container').innerHTML = statsHtml;
            } catch (error) {
                document.getElementById('stats-container').innerHTML = 
                    '<div class="error">❌ Failed to load statistics: ' + error.message + '</div>';
            }
        }
        
        async function loadUsers() {
            try {
                const response = await fetch('/api/users');
                const users = await response.json();
                
                let html = `<p>Total Users: ${users.length}</p>`;
                
                if (users.length > 0) {
                    html += `
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Business Type</th>
                                    <th>Created At</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    
                    users.forEach(user => {
                        html += `
                            <tr>
                                <td>${user.name || 'N/A'}</td>
                                <td>${user.email || 'N/A'}</td>
                                <td>${user.phone || 'N/A'}</td>
                                <td>${user.business_type || 'N/A'}</td>
                                <td>${new Date(user.created_at).toLocaleString()}</td>
                            </tr>
                        `;
                    });
                    
                    html += '</tbody></table>';
                } else {
                    html += '<div class="loading">No users found</div>';
                }
                
                document.getElementById('users-container').innerHTML = html;
            } catch (error) {
                document.getElementById('users-container').innerHTML = 
                    '<div class="error">❌ Failed to load users: ' + error.message + '</div>';
            }
        }
        
        async function loadAppointments() {
            try {
                const response = await fetch('/api/appointments');
                const appointments = await response.json();
                
                let html = `<p>Total Appointments: ${appointments.length}</p>`;
                
                if (appointments.length > 0) {
                    html += `
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Services</th>
                                    <th>Phone</th>
                                    <th>Date</th>
                                    <th>Time</th>
                                    <th>Status</th>
                                    <th>Notes</th>
                                    <th>Created</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    
                    appointments.forEach(apt => {
                        html += `
                            <tr>
                                <td>${(apt.services || []).join(', ')}</td>
                                <td>${apt.phone || 'N/A'}</td>
                                <td>${apt.preferred_date || 'N/A'}</td>
                                <td>${apt.preferred_time || 'N/A'}</td>
                                <td>${apt.status || 'N/A'}</td>
                                <td>${apt.notes || 'N/A'}</td>
                                <td>${new Date(apt.created_at).toLocaleString()}</td>
                            </tr>
                        `;
                    });
                    
                    html += '</tbody></table>';
                } else {
                    html += '<div class="loading">No appointments found</div>';
                }
                
                document.getElementById('appointments-container').innerHTML = html;
            } catch (error) {
                document.getElementById('appointments-container').innerHTML = 
                    '<div class="error">❌ Failed to load appointments: ' + error.message + '</div>';
            }
        }
        
        async function loadConversations() {
            try {
                const response = await fetch('/api/conversations');
                const conversations = await response.json();
                
                let html = `<p>Total Conversations: ${conversations.length}</p>`;
                
                if (conversations.length > 0) {
                    html += `
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>User</th>
                                    <th>Message</th>
                                    <th>Response</th>
                                    <th>Business Type</th>
                                    <th>Timestamp</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    
                    conversations.forEach(conv => {
                        html += `
                            <tr>
                                <td>${conv.user_name || 'N/A'}</td>
                                <td>${(conv.user_message || '').substring(0, 50)}...</td>
                                <td>${(conv.bot_response || '').substring(0, 50)}...</td>
                                <td>${conv.business_type || 'N/A'}</td>
                                <td>${new Date(conv.timestamp).toLocaleString()}</td>
                            </tr>
                        `;
                    });
                    
                    html += '</tbody></table>';
                } else {
                    html += '<div class="loading">No conversations found</div>';
                }
                
                document.getElementById('conversations-container').innerHTML = html;
            } catch (error) {
                document.getElementById('conversations-container').innerHTML = 
                    '<div class="error">❌ Failed to load conversations: ' + error.message + '</div>';
            }
        }
        
        async function loadAnalytics() {
            try {
                const response = await fetch('/api/analytics');
                const analytics = await response.json();
                
                const html = `
                    <div class="json-view">${JSON.stringify(analytics, null, 2)}</div>
                `;
                
                document.getElementById('analytics-container').innerHTML = html;
            } catch (error) {
                document.getElementById('analytics-container').innerHTML = 
                    '<div class="error">❌ Failed to load analytics: ' + error.message + '</div>';
            }
        }
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            if (currentSection === 'dashboard') {
                loadDashboard();
            }
        }, 30000);
        
        // Load dashboard on page load
        loadDashboard();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main viewer page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/statistics')
def get_statistics():
    """Get database statistics"""
    try:
        stats = db_backend.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users')
def get_users():
    """Get all users"""
    try:
        users = db_backend.get_all_users(limit=100)
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/appointments')
def get_appointments():
    """Get all appointments"""
    try:
        appointments = db_backend.get_all_appointments(limit=100)
        return jsonify(appointments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations')
def get_conversations():
    """Get all conversations"""
    try:
        conversations = db_backend.get_all_conversations(limit=100)
        return jsonify(conversations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics')
def get_analytics():
    """Get advanced analytics"""
    try:
        analytics = {
            "database_status": "connected" if db_backend.is_connected() else "disconnected",
            "collections": {
                "users": db_backend.db.users.count_documents({}) if db_backend.is_connected() else 0,
                "appointments": db_backend.db.appointments.count_documents({}) if db_backend.is_connected() else 0,
                "conversations": db_backend.db.conversations.count_documents({}) if db_backend.is_connected() else 0
            },
            "last_updated": datetime.now().isoformat()
        }
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Techrypt MongoDB Viewer...")
    print("📊 Access the viewer at: http://localhost:5001")
    print("🔄 Auto-refresh enabled for real-time monitoring")
    
    if not db_backend.is_connected():
        print("⚠️ Warning: MongoDB connection failed")
        print("💡 Make sure MongoDB is running on localhost:27017")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
