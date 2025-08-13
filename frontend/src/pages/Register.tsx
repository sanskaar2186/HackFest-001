import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../App';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setIsLoading(true);
    
    try {
      // This is a placeholder for the actual API call
      // In a real implementation, you would call your backend API
      console.log('Registration attempt with:', { 
        username: formData.username, 
        email: formData.email,
        password: formData.password 
      });
      
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
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      // After successful registration, log the user in
      const loginResponse = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
      });

      if (!loginResponse.ok) {
        throw new Error('Registration successful but login failed');
      }

      const data = await loginResponse.json();
      login(data.access_token);
      navigate('/dashboard');
      */
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed. Please try again.');
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
            <Link to="/login" className="btn btn-outline">Login</Link>
          </div>
        </div>
      </nav>

      {/* Registration Form */}
      <div className="container">
        <div className="form-container">
          <h2 className="form-title">Create Your Account</h2>
          
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
                name="username"
                className="form-input"
                value={formData.username}
                onChange={handleChange}
                required
                autoComplete="username"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="email" className="form-label">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                className="form-input"
                value={formData.email}
                onChange={handleChange}
                required
                autoComplete="email"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="password" className="form-label">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                className="form-input"
                value={formData.password}
                onChange={handleChange}
                required
                autoComplete="new-password"
                minLength={8}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                className="form-input"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                autoComplete="new-password"
              />
            </div>
            
            <button 
              type="submit" 
              className="btn btn-block" 
              disabled={isLoading}
              style={{ opacity: isLoading ? 0.7 : 1 }}
            >
              {isLoading ? 'Creating Account...' : 'Sign Up'}
            </button>
          </form>
          
          <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
            <p>Already have an account? <Link to="/login" style={{ color: 'var(--primary-color)' }}>Login</Link></p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;