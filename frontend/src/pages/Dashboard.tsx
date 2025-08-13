import { useContext, useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../App';

const Dashboard = () => {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [userData, setUserData] = useState({
    username: 'User',
    email: 'user@example.com',
    joinDate: new Date().toLocaleDateString(),
  });

  useEffect(() => {
    // In a real app, you would fetch user data from your backend
    // This is a placeholder for demonstration purposes
    const fetchUserData = async () => {
      try {
        // Simulate API call
        setTimeout(() => {
          setUserData({
            username: 'HackUser',
            email: 'hackuser@example.com',
            joinDate: new Date().toLocaleDateString(),
          });
        }, 500);

        /* 
        // Example of how to connect to a real backend:
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/users/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user data');
        }

        const data = await response.json();
        setUserData({
          username: data.username,
          email: data.email,
          joinDate: new Date(data.created_at).toLocaleDateString(),
        });
        */
      } catch (error) {
        console.error('Error fetching user data:', error);
        // If there's an authentication error, log the user out
        if (error instanceof Error && error.message.includes('authentication')) {
          handleLogout();
        }
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>HackFest</h2>
          <p>{userData.username}</p>
        </div>
        
        <div className="sidebar-nav">
          <a 
            href="#" 
            className={`sidebar-link ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </a>
          <a 
            href="#" 
            className={`sidebar-link ${activeTab === 'hackathons' ? 'active' : ''}`}
            onClick={() => setActiveTab('hackathons')}
          >
            Hackathons
          </a>
          <a 
            href="#" 
            className={`sidebar-link ${activeTab === 'projects' ? 'active' : ''}`}
            onClick={() => setActiveTab('projects')}
          >
            My Projects
          </a>
          <a 
            href="#" 
            className={`sidebar-link ${activeTab === 'teams' ? 'active' : ''}`}
            onClick={() => setActiveTab('teams')}
          >
            Teams
          </a>
          <a 
            href="#" 
            className={`sidebar-link ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            Profile
          </a>
          <a 
            href="#" 
            className="sidebar-link"
            onClick={handleLogout}
          >
            Logout
          </a>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div>
            <h1>Welcome, {userData.username}!</h1>
            <p>Here's what's happening in your HackFest world today.</p>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginTop: '2rem' }}>
              <div className="card">
                <div className="card-header">
                  <h3 className="card-title">Upcoming Hackathons</h3>
                </div>
                <div>
                  <div style={{ padding: '1rem', borderLeft: '3px solid var(--primary-color)', marginBottom: '1rem' }}>
                    <p style={{ color: '#666', fontSize: '0.875rem' }}>May 15-17, 2023</p>
                    <h4>AI Innovation Challenge</h4>
                    <p>Build AI solutions to solve real-world problems.</p>
                  </div>
                  
                  <div style={{ padding: '1rem', borderLeft: '3px solid var(--primary-color)', marginBottom: '1rem' }}>
                    <p style={{ color: '#666', fontSize: '0.875rem' }}>June 5-7, 2023</p>
                    <h4>Web3 Hackathon</h4>
                    <p>Create decentralized applications on blockchain.</p>
                  </div>
                </div>
              </div>
              
              <div className="card">
                <div className="card-header">
                  <h3 className="card-title">Your Projects</h3>
                </div>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', borderBottom: '1px solid #eee' }}>
                    <div>
                      <h4>Smart Home Assistant</h4>
                      <p style={{ color: '#666', fontSize: '0.875rem' }}>Last updated: 3 days ago</p>
                    </div>
                    <span style={{ backgroundColor: 'var(--success-color)', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Active</span>
                  </div>
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem' }}>
                    <div>
                      <h4>Blockchain Voting System</h4>
                      <p style={{ color: '#666', fontSize: '0.875rem' }}>Last updated: 2 weeks ago</p>
                    </div>
                    <span style={{ backgroundColor: '#6c757d', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Completed</span>
                  </div>
                </div>
              </div>
              
              <div className="card">
                <div className="card-header">
                  <h3 className="card-title">Team Activity</h3>
                </div>
                <div>
                  <div style={{ padding: '1rem', borderBottom: '1px solid #eee' }}>
                    <p><strong>Alex</strong> commented on <strong>Smart Home Assistant</strong></p>
                    <p style={{ color: '#666', fontSize: '0.875rem' }}>2 hours ago</p>
                  </div>
                  
                  <div style={{ padding: '1rem', borderBottom: '1px solid #eee' }}>
                    <p><strong>Sarah</strong> pushed 5 commits to <strong>Smart Home Assistant</strong></p>
                    <p style={{ color: '#666', fontSize: '0.875rem' }}>Yesterday</p>
                  </div>
                  
                  <div style={{ padding: '1rem' }}>
                    <p><strong>Team CodeCrafters</strong> was created</p>
                    <p style={{ color: '#666', fontSize: '0.875rem' }}>3 days ago</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div>
            <h1>Your Profile</h1>
            
            <div className="card" style={{ maxWidth: '600px', margin: '2rem 0' }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2rem' }}>
                <div style={{ 
                  width: '100px', 
                  height: '100px', 
                  borderRadius: '50%', 
                  backgroundColor: 'var(--primary-color)', 
                  color: 'white', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  fontSize: '2.5rem',
                  marginRight: '1.5rem'
                }}>
                  {userData.username.charAt(0).toUpperCase()}
                </div>
                
                <div>
                  <h2 style={{ marginBottom: '0.5rem' }}>{userData.username}</h2>
                  <p style={{ color: '#666' }}>Member since {userData.joinDate}</p>
                </div>
              </div>
              
              <div>
                <div style={{ marginBottom: '1.5rem' }}>
                  <h3 style={{ fontSize: '1.1rem', color: '#666', marginBottom: '0.5rem' }}>Email</h3>
                  <p>{userData.email}</p>
                </div>
                
                <div style={{ marginBottom: '1.5rem' }}>
                  <h3 style={{ fontSize: '1.1rem', color: '#666', marginBottom: '0.5rem' }}>Bio</h3>
                  <p>No bio added yet.</p>
                </div>
                
                <div style={{ marginBottom: '1.5rem' }}>
                  <h3 style={{ fontSize: '1.1rem', color: '#666', marginBottom: '0.5rem' }}>Skills</h3>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    <span style={{ backgroundColor: '#f8f9fa', padding: '0.5rem 0.75rem', borderRadius: '20px', fontSize: '0.875rem' }}>React</span>
                    <span style={{ backgroundColor: '#f8f9fa', padding: '0.5rem 0.75rem', borderRadius: '20px', fontSize: '0.875rem' }}>TypeScript</span>
                    <span style={{ backgroundColor: '#f8f9fa', padding: '0.5rem 0.75rem', borderRadius: '20px', fontSize: '0.875rem' }}>Node.js</span>
                    <span style={{ backgroundColor: '#f8f9fa', padding: '0.5rem 0.75rem', borderRadius: '20px', fontSize: '0.875rem' }}>Python</span>
                  </div>
                </div>
              </div>
              
              <button className="btn" style={{ marginTop: '1rem' }}>Edit Profile</button>
            </div>
          </div>
        )}
        
        {/* Placeholder for other tabs */}
        {activeTab === 'hackathons' && (
          <div>
            <h1>Hackathons</h1>
            <p>Browse and join upcoming hackathons.</p>
            {/* Hackathon content would go here */}
          </div>
        )}
        
        {activeTab === 'projects' && (
          <div>
            <h1>My Projects</h1>
            <p>Manage your hackathon projects.</p>
            {/* Projects content would go here */}
          </div>
        )}
        
        {activeTab === 'teams' && (
          <div>
            <h1>Teams</h1>
            <p>Manage your teams and find teammates.</p>
            {/* Teams content would go here */}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;