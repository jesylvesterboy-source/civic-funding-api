@"
import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'https://civic-funding-api.onrender.com';

export default function CivicFundingDashboard() {
  const [initiatives, setInitiatives] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [initiativesRes, analyticsRes] = await Promise.all([
        axios.get(API_BASE_URL + '/api/initiatives'),
        axios.get(API_BASE_URL + '/api/analytics')
      ]);
      
      setInitiatives(initiativesRes.data);
      setAnalytics(analyticsRes.data);
    } catch (err) {
      console.error('API Error:', err);
      setError('Backend is warming up... Please wait 30 seconds and refresh.');
      // Fallback demo data
      setInitiatives([
        {name: 'Urban Renewal Program', budget: 1500000, region: 'Metropolitan', impact: 92, status: 'Active'},
        {name: 'Rural Education Initiative', budget: 800000, region: 'Rural', impact: 88, status: 'Planning'},
        {name: 'Healthcare Access Project', budget: 1200000, region: 'Suburban', impact: 95, status: 'Active'},
        {name: 'Infrastructure Development', budget: 2000000, region: 'Metropolitan', impact: 90, status: 'Completed'}
      ]);
      setAnalytics({
        total_funding: 5500000,
        initiatives_count: 4,
        average_impact: 91.2,
        regions_served: 3
      });
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active': return '#10b981';
      case 'Planning': return '#f59e0b';
      case 'Completed': return '#3b82f6';
      default: return '#6b7280';
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>
          <h2>🚀 Loading Civic Funding Intelligence Platform...</h2>
          <p>Initializing real-time analytics dashboard</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <h1 style={styles.title}>Civic Funding Intelligence Platform</h1>
        <p style={styles.subtitle}>Real-time funding analytics & impact measurement</p>
      </header>

      {error && (
        <div style={styles.error}>
          ⚠️ {error}
          <button onClick={fetchData} style={styles.retryButton}>Retry</button>
        </div>
      )}

      {/* Analytics Overview */}
      {analytics && (
        <div style={styles.analyticsGrid}>
          <div style={styles.metricCard}>
            <h3>Total Funding</h3>
            <p style={styles.metricValue}>${analytics.total_funding?.toLocaleString()}</p>
            <span style={styles.metricLabel}>Across all initiatives</span>
          </div>
          
          <div style={styles.metricCard}>
            <h3>Initiatives</h3>
            <p style={styles.metricValue}>{analytics.initiatives_count}</p>
            <span style={styles.metricLabel}>Active projects</span>
          </div>
          
          <div style={styles.metricCard}>
            <h3>Avg Impact</h3>
            <p style={styles.metricValue}>{analytics.average_impact?.toFixed(1)}%</p>
            <span style={styles.metricLabel}>Success rate</span>
          </div>
          
          <div style={styles.metricCard}>
            <h3>Regions</h3>
            <p style={styles.metricValue}>{analytics.regions_served}</p>
            <span style={styles.metricLabel}>Areas covered</span>
          </div>
        </div>
      )}

      {/* Initiatives List */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>🏗️ Funding Initiatives</h2>
        <div style={styles.initiativesGrid}>
          {initiatives.map((initiative, index) => (
            <div key={index} style={styles.initiativeCard}>
              <div style={styles.initiativeHeader}>
                <h3 style={styles.initiativeName}>{initiative.name}</h3>
                <span style={{...styles.status, backgroundColor: getStatusColor(initiative.status)}}>
                  {initiative.status}
                </span>
              </div>
              
              <div style={styles.initiativeDetails}>
                <div style={styles.detailItem}>
                  <span style={styles.detailLabel}>💰 Budget:</span>
                  <span style={styles.detailValue}>${initiative.budget?.toLocaleString()}</span>
                </div>
                
                <div style={styles.detailItem}>
                  <span style={styles.detailLabel}>📍 Region:</span>
                  <span style={styles.detailValue}>{initiative.region}</span>
                </div>
                
                <div style={styles.detailItem}>
                  <span style={styles.detailLabel}>⭐ Impact:</span>
                  <span style={styles.detailValue}>{initiative.impact}/100</span>
                </div>
              </div>
              
              <div style={styles.progressBar}>
                <div 
                  style={{
                    ...styles.progressFill,
                    width: `${initiative.impact}%`,
                    backgroundColor: initiative.impact >= 90 ? '#10b981' : initiative.impact >= 80 ? '#f59e0b' : '#ef4444'
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Tech Stack Footer */}
      <footer style={styles.footer}>
        <p>
          <strong>Tech Stack:</strong> React + Next.js + FastAPI + Supabase + PostgreSQL
        </p>
        <p style={styles.footerNote}>
          Real-time civic funding intelligence platform
        </p>
      </footer>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: '#f8fafc',
    minHeight: '100vh'
  },
  header: {
    textAlign: 'center',
    marginBottom: '40px',
    padding: '40px 20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    borderRadius: '15px',
    color: 'white'
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: 'bold',
    marginBottom: '10px'
  },
  subtitle: {
    fontSize: '1.2rem',
    opacity: 0.9
  },
  loading: {
    textAlign: 'center',
    padding: '60px 20px'
  },
  error: {
    background: '#fef2f2',
    border: '1px solid #fecaca',
    color: '#dc2626',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  retryButton: {
    background: '#dc2626',
    color: 'white',
    border: 'none',
    padding: '8px 16px',
    borderRadius: '6px',
    cursor: 'pointer'
  },
  analyticsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '40px'
  },
  metricCard: {
    background: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
    textAlign: 'center',
    border: '1px solid #e2e8f0'
  },
  metricValue: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#1e293b',
    margin: '10px 0'
  },
  metricLabel: {
    color: '#64748b',
    fontSize: '0.9rem'
  },
  section: {
    marginBottom: '40px'
  },
  sectionTitle: {
    fontSize: '1.8rem',
    marginBottom: '20px',
    color: '#1e293b'
  },
  initiativesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
    gap: '20px'
  },
  initiativeCard: {
    background: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
    border: '1px solid #e2e8f0',
    transition: 'transform 0.2s, box-shadow 0.2s'
  },
  initiativeHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '15px'
  },
  initiativeName: {
    fontSize: '1.3rem',
    fontWeight: '600',
    color: '#1e293b',
    margin: '0',
    flex: 1,
    marginRight: '15px'
  },
  status: {
    padding: '4px 12px',
    borderRadius: '20px',
    fontSize: '0.8rem',
    fontWeight: '600',
    color: 'white',
    whiteSpace: 'nowrap'
  },
  initiativeDetails: {
    marginBottom: '15px'
  },
  detailItem: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '8px',
    paddingBottom: '8px',
    borderBottom: '1px solid #f1f5f9'
  },
  detailLabel: {
    color: '#64748b',
    fontWeight: '500'
  },
  detailValue: {
    color: '#1e293b',
    fontWeight: '600'
  },
  progressBar: {
    height: '6px',
    background: '#e2e8f0',
    borderRadius: '3px',
    overflow: 'hidden'
  },
  progressFill: {
    height: '100%',
    transition: 'width 0.3s ease'
  },
  footer: {
    textAlign: 'center',
    padding: '30px 20px',
    color: '#64748b',
    borderTop: '1px solid #e2e8f0',
    marginTop: '40px'
  },
  footerNote: {
    fontSize: '0.9rem',
    marginTop: '10px',
    opacity: 0.7
  }
};
"@ | Out-File -FilePath "vercel_frontend/pages/index.js" -Encoding utf8