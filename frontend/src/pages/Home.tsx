import { Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../App';

const Home = () => {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <div className="page">
      {/* Navbar */}
      <nav className="navbar">
        <div className="container">
          <Link to="/" className="navbar-brand">HackFest</Link>
          <div className="navbar-nav">
            <Link to="/" className="nav-link active">Home</Link>
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="nav-link">Dashboard</Link>
                <Link to="/dashboard" className="btn">My Account</Link>
              </>
            ) : (
              <>
                <Link to="/login" className="nav-link">Login</Link>
                <Link to="/register" className="btn">Sign Up</Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container" style={{ padding: '5rem 0' }}>
        <div style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '1.5rem', color: 'var(--primary-color)' }}>Welcome to HackFest</h1>
          <p style={{ fontSize: '1.25rem', marginBottom: '2rem', color: 'var(--text-color)' }}>
            Join the community of innovators, developers, and creators. Participate in hackathons, 
            build amazing projects, and connect with like-minded individuals.
          </p>
          <div>
            {isAuthenticated ? (
              <Link to="/dashboard" className="btn" style={{ marginRight: '1rem' }}>Go to Dashboard</Link>
            ) : (
              <>
                <Link to="/register" className="btn" style={{ marginRight: '1rem' }}>Get Started</Link>
                <Link to="/login" className="btn btn-outline">Login</Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ backgroundColor: 'white', padding: '5rem 0' }}>
        <div className="container">
          <h2 className="text-center" style={{ marginBottom: '3rem' }}>Why Join HackFest?</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
            <div className="card">
              <h3 style={{ color: 'var(--primary-color)', marginBottom: '1rem' }}>Participate in Hackathons</h3>
              <p>Join exciting hackathons with various themes and challenges. Showcase your skills and win amazing prizes.</p>
            </div>
            
            <div className="card">
              <h3 style={{ color: 'var(--primary-color)', marginBottom: '1rem' }}>Build Your Portfolio</h3>
              <p>Create and showcase projects that demonstrate your abilities to potential employers or collaborators.</p>
            </div>
            
            <div className="card">
              <h3 style={{ color: 'var(--primary-color)', marginBottom: '1rem' }}>Connect with Others</h3>
              <p>Network with other developers, designers, and innovators. Form teams and collaborate on exciting projects.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{ backgroundColor: 'var(--primary-color)', color: 'white', padding: '4rem 0', textAlign: 'center' }}>
        <div className="container">
          <h2 style={{ marginBottom: '1.5rem' }}>Ready to Start Your Journey?</h2>
          <p style={{ marginBottom: '2rem', maxWidth: '600px', margin: '0 auto' }}>
            Join our community today and take part in the next big hackathon event.
          </p>
          {!isAuthenticated && (
            <Link to="/register" className="btn" style={{ backgroundColor: 'white', color: 'var(--primary-color)' }}>
              Create Your Account
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer style={{ backgroundColor: 'var(--dark-color)', color: 'white', padding: '2rem 0', textAlign: 'center' }}>
        <div className="container">
          <p>© {new Date().getFullYear()} HackFest. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;