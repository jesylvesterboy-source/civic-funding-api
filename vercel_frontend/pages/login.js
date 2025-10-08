@"
import { useState } from 'react';
import { useRouter } from 'next/router';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate login - in production, connect to your auth system
    setTimeout(() => {
      localStorage.setItem('authenticated', 'true');
      router.push('/');
    }, 1000);
  };

  return (
    <div style={styles.container}>
      <div style={styles.loginCard}>
        <div style={styles.header}>
          <h1 style={styles.title}>Civic Funding Intelligence</h1>
          <p style={styles.subtitle}>Access the funding analytics dashboard</p>
        </div>
        
        <form onSubmit={handleLogin} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={styles.input}
              placeholder="admin@civicfunding.org"
              required
            />
          </div>
          
          <div style={styles.inputGroup}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
              placeholder="Enter your password"
              required
            />
          </div>
          
          <button 
            type="submit" 
            style={styles.loginButton}
            disabled={loading}
          >
            {loading ? 'Signing In...' : 'Sign In to Dashboard'}
          </button>
        </form>
        
        <div style={styles.demoNote}>
          <p><strong>Demo Access:</strong> Use any email/password to explore</p>
          <p>Full authentication integrates with Supabase Auth</p>
        </div>
        
        <div style={styles.techStack}>
          <p>Powered by: React • FastAPI • Supabase • PostgreSQL</p>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
  },
  loginCard: {
    background: 'white',
    padding: '40px',
    borderRadius: '15px',
    boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '400px'
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px'
  },
  title: {
    fontSize: '1.8rem',
    fontWeight: 'bold',
    color: '#1e293b',
    marginBottom: '8px'
  },
  subtitle: {
    color: '#64748b',
    fontSize: '1rem'
  },
  form: {
    marginBottom: '25px'
  },
  inputGroup: {
    marginBottom: '20px'
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontWeight: '600',
    color: '#374151'
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '1rem',
    transition: 'border-color 0.2s',
    boxSizing: 'border-box'
  },
  loginButton: {
    width: '100%',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    padding: '14px 20px',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'opacity 0.2s'
  },
  demoNote: {
    background: '#f0f9ff',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '20px',
    fontSize: '0.9rem',
    color: '#0369a1'
  },
  techStack: {
    textAlign: 'center',
    fontSize: '0.8rem',
    color: '#6b7280',
    paddingTop: '20px',
    borderTop: '1px solid #e5e7eb'
  }
};
"@ | Out-File -FilePath "vercel_frontend/pages/login.js" -Encoding utf8