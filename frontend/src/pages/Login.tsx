import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../App';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      // This is a placeholder for the actual API call
      // In a real implementation, you would call your backend API
      console.log('Login attempt with:', { username, password });
      
      // Simulate API call
      setTimeout(() => {
        // For demo purposes, we're using a mock token
        // In a real app, this would come from your backend
        const mockToken = 'mock-jwt-token-' + Math.random().toString(36).substring(2);
        login(mockToken);
        navigate('/dashboard');
      }, 1000);
      
      /* 
      // Example of how to connect to a real backend:
      const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      login(data.access_token);
      navigate('/dashboard');
      */
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed. Please try again.');
      setIsLoading(false);
    }
  };

  return (
    <div className="page">
      {/* Navbar */}
      <nav className="navbar">
        <div className="container">
          <Link to="/" className="navbar-brand">HackFest</Link>
          <div className="navbar-nav">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/register" className="btn btn-outline">Sign Up</Link>
          </div>
        </div>
      </nav>

      {/* Login Form */}
      <div className="container">
        <div className="form-container">
          <h2 className="form-title">Login to Your Account</h2>
          
          {error && (
            <div style={{ 
              backgroundColor: 'rgba(230, 57, 70, 0.1)', 
              color: 'var(--danger-color)', 
              padding: '0.75rem', 
              borderRadius: 'var(--border-radius)', 
              marginBottom: '1.5rem',
              textAlign: 'center'
            }}>
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username" className="form-label">Username</label>
              <input
                type="text"
                id="username"
                className="form-input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoComplete="username"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="password" className="form-label">Password</label>
              <input
                type="password"
                id="password"
                className="form-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
              />
            </div>
            
            <button 
              type="submit" 
              className="btn btn-block" 
              disabled={isLoading}
              style={{ opacity: isLoading ? 0.7 : 1 }}
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>
          
          <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
            <p>Don't have an account? <Link to="/register" style={{ color: 'var(--primary-color)' }}>Sign up</Link></p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;