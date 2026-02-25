import { useState, useCallback } from 'react';
import { Award, Plus, X, Upload, FileCheck } from 'lucide-react';
import { useDropzone } from 'react-dropzone';

export default function CertificationsForm({ certs, onChange }) {
  const [name, setName] = useState('');
  const [issuer, setIssuer] = useState('');
  const [year, setYear] = useState(2024);
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);

  const addCert = () => {
    if (!name.trim()) return;
    onChange([...certs, { name: name.trim(), issuer: issuer.trim(), year }]);
    setName(''); setIssuer(''); setYear(2024);
  };

  const removeCert = idx => onChange(certs.filter((_, i) => i !== idx));

  const onDrop = useCallback(async (acceptedFiles) => {
    for (const file of acceptedFiles) {
      setScanning(true);
      setScanResult(null);
      try {
        const formData = new FormData();
        formData.append('file', file);
        const res = await fetch('/api/score/certifications/scan', {
          method: 'POST', body: formData
        });
        const result = await res.json();
        setScanResult(result);
        if (result.identified && result.cert_name) {
          const certName = result.cert_name;
          const tierLabel = result.match?.tier_label || '';
          onChange([...certs, { name: certName, issuer: tierLabel, year: 2024 }]);
        }
      } catch (err) {
        setScanResult({ error: 'Failed to scan certificate file.' });
      }
      setScanning(false);
    }
  }, [certs, onChange]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    multiple: true,
  });

  const getTierColor = (tier) => {
    const colors = { platinum: '#e5e7eb', gold: '#fbbf24', silver: '#9ca3af', bronze: '#d97706' };
    return colors[tier] || '#6366f1';
  };

  return (
    <div className="animate-fadeIn">
      <div style={{ marginBottom: '24px' }}>
        <h2 className="flex items-center gap-2" style={{ fontSize: '22px', fontWeight: 700, marginBottom: '6px' }}>
          <Award size={24} color="#6366f1" /> Certifications
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          Add certifications manually or upload certificate PDFs for auto-detection. (Weight: 15%)
        </p>
      </div>

      {/* File Upload Zone */}
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`} style={{ marginBottom: '20px' }}>
        <input {...getInputProps()} />
        <Upload size={32} color="var(--primary)" style={{ margin: '0 auto 12px' }} />
        <p style={{ fontWeight: 600, marginBottom: '4px' }}>
          {scanning ? '🔍 Scanning certificate...' : 'Drop certificate PDFs here or click to upload'}
        </p>
        <p style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>
          Supported: PDF files. The system will auto-detect and rank the certification.
        </p>
      </div>

      {/* Scan Result */}
      {scanResult && (
        <div className="card" style={{ marginBottom: '20px', borderColor: scanResult.identified ? 'var(--success)' : 'var(--warning)' }}>
          <div className="flex items-center gap-2" style={{ marginBottom: '8px' }}>
            <FileCheck size={18} color={scanResult.identified ? 'var(--success)' : 'var(--warning)'} />
            <span style={{ fontWeight: 600, fontSize: '14px' }}>
              {scanResult.identified ? 'Certificate Identified!' : 'Could not identify certificate'}
            </span>
          </div>
          {scanResult.identified && (
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
              <p><strong>Name:</strong> {scanResult.cert_name}</p>
              {scanResult.match && (
                <p><strong>Tier:</strong> <span style={{ color: getTierColor(scanResult.match.tier) }}>{scanResult.match.tier_label}</span></p>
              )}
              {scanResult.extracted_text_preview && (
                <details style={{ marginTop: '8px' }}>
                  <summary style={{ cursor: 'pointer', color: 'var(--primary-light)' }}>View extracted text</summary>
                  <pre style={{ marginTop: '8px', padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', whiteSpace: 'pre-wrap', fontSize: '11px' }}>
                    {scanResult.extracted_text_preview}
                  </pre>
                </details>
              )}
            </div>
          )}
          {scanResult.error && <p style={{ color: 'var(--warning)', fontSize: '13px' }}>{scanResult.error}</p>}
        </div>
      )}

      {/* Manual Add */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3 style={{ fontWeight: 600, fontSize: '14px', marginBottom: '16px' }}>Add Manually</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '12px', alignItems: 'end' }}>
          <div>
            <label>Certification Name *</label>
            <input value={name} onChange={e => setName(e.target.value)} placeholder="e.g., AWS Solutions Architect" />
          </div>
          <div>
            <label>Issuing Organization</label>
            <input value={issuer} onChange={e => setIssuer(e.target.value)} placeholder="e.g., Amazon" />
          </div>
          <button className="btn-primary" onClick={addCert} disabled={!name.trim()} style={{ height: '45px' }}>
            <Plus size={18} /> Add
          </button>
        </div>
      </div>

      {/* Listed Certs */}
      {certs.length > 0 && (
        <div style={{ display: 'grid', gap: '10px' }}>
          {certs.map((c, i) => (
            <div key={i} className="card flex items-center justify-between" style={{ padding: '14px 20px' }}>
              <div>
                <span style={{ fontWeight: 600 }}>{c.name}</span>
                {c.issuer && <span style={{ color: 'var(--text-secondary)', fontSize: '13px', marginLeft: '8px' }}>— {c.issuer}</span>}
              </div>
              <button onClick={() => removeCert(i)} style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>
          ))}
        </div>
      )}

      {certs.length === 0 && (
        <div className="text-center" style={{ padding: '40px', color: 'var(--text-secondary)' }}>
          <Award size={40} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
          <p>No certifications added yet. Upload PDFs or add manually above.</p>
        </div>
      )}
    </div>
  );
}
