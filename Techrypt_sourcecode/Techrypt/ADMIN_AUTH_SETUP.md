# Admin Authentication Setup Guide

## Overview
The admin authentication system has been implemented with the following features:

- Secure login page at `/admin` route
- JWT token-based authentication
- Protected admin dashboard routes
- Automatic token verification
- Logout functionality

## Setup Instructions

### 1. Environment Variables
Make sure your backend has the following environment variables set:

```env
ADMIN_EMAIL=your-admin-email@example.com
ADMIN_PASSWORD=your-secure-password
JWT_SECRET=your-jwt-secret-key
MONGO_URI=your-mongodb-connection-string
```

### 2. Create Admin User
Run the admin creation utility to create your first admin user:

```bash
cd server
node utils/createAdmin.js
```

### 3. Start the Application
1. Start the backend server:
   ```bash
   cd server
   npm start
   ```

2. Start the frontend:
   ```bash
   cd Techrypt
   npm run dev
   ```

### 4. Access Admin Panel
1. Navigate to `http://localhost:5173/admin`
2. Use the email and password from your environment variables
3. After successful login, you'll be redirected to the admin dashboard

## Features

### Authentication Flow
1. User visits `/admin`
2. If not authenticated, shows login form
3. On successful login, JWT token is stored in localStorage
4. User is redirected to admin dashboard
5. All subsequent admin API calls include the JWT token

### Protected Routes
- `/admin` - Login page (if not authenticated) or dashboard (if authenticated)
- `/admin/dashboard` - Main dashboard
- `/admin/blogs` - Blog management
- `/admin/appointments` - Appointment management

### Security Features
- Automatic token verification on app load
- Token expiration handling
- Secure logout (clears token)
- Protected API endpoints

## API Endpoints Used

- `POST /api/admin/login` - Admin login
- `GET /api/admin/me` - Get current admin info (requires auth)

## Components Structure

```
src/
├── context/
│   └── AuthContext.jsx          # Authentication context
├── components/AdminDashboard/
│   ├── AdminLogin.jsx           # Login form component
│   ├── ProtectedRoute.jsx       # Route protection wrapper
│   └── AdminSidebar.jsx         # Updated with logout functionality
└── pages/AdminDashboard/
    └── AdminDashboard.jsx       # Updated with protection
```

## Notes

- The authentication state is managed globally using React Context
- JWT tokens are stored in localStorage for persistence
- The login form includes proper validation and error handling
- All admin components now use the authentication context
- The system automatically handles token expiration and invalid tokens
