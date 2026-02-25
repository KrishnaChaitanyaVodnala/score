import { useState, useCallback } from 'react';
import { FileText, Upload, Check } from 'lucide-react';
import { useDropzone } from 'react-dropzone';

export default function ResumeUpload({ resumeText, onChange }) {
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState('');
  const [preview, setPreview] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;
    setUploading(true);
    setFileName(file.name);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch('/api/score/resume', { method: 'POST', body: formData });
      const result = await res.json();
      setPreview(result);
      // Also read as text for the final calculation
      const reader = new FileReader();
      reader.onload = () => {
        // Send filename as a marker so backend knows we uploaded a resume
        onChange(result.total_words ? `[Resume uploaded: ${file.name}]\n` + (result.suggestions?.join('\n') || '') : '');
      };
      reader.readAsText(file);
    } catch (err) {
      console.error('Upload error:', err);
    }
    setUploading(false);
  }, [onChange]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'application/pdf': ['.pdf'] }, multiple: false,
  });

  const getScoreColor = s => s >= 80 ? '#10b981' : s >= 60 ? '#eab308' : s >= 40 ? '#f97316' : '#ef4444';

  return (
    <div className="animate-fadeIn">
      <div style={{ marginBottom: '24px' }}>
        <h2 className="flex items-center gap-2" style={{ fontSize: '22px', fontWeight: 700, marginBottom: '6px' }}>
          <FileText size={24} color="#6366f1" /> Resume
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          Upload your resume (PDF) for ATS scoring, or paste your resume text below. (Weight: 10%)
        </p>
      </div>

      {/* Upload Zone */}
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`} style={{ marginBottom: '20px' }}>
        <input {...getInputProps()} />
        {fileName ? (
          <>
            <Check size={32} color="var(--success)" style={{ margin: '0 auto 12px' }} />
            <p style={{ fontWeight: 600, color: 'var(--success)' }}>✅ {fileName} uploaded</p>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>Click or drop another file to replace</p>
          </>
        ) : (
          <>
            <Upload size={32} color="var(--primary)" style={{ margin: '0 auto 12px' }} />
            <p style={{ fontWeight: 600 }}>{uploading ? '📄 Analyzing resume...' : 'Drop your resume PDF here or click to upload'}</p>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>PDF format recommended for best ATS analysis</p>
          </>
        )}
      </div>

      {/* ATS Preview */}
      {preview && preview.section_scores && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3 style={{ fontWeight: 600, fontSize: '16px', marginBottom: '16px' }}>
            ATS Analysis Preview — Score: <span style={{ color: getScoreColor(preview.score) }}>{preview.score}/100</span>
          </h3>
          <div style={{ display: 'grid', gap: '8px' }}>
            {Object.entries(preview.section_scores).map(([name, data]) => (
              <div key={name} className="flex items-center justify-between" style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
                <span style={{ fontSize: '14px' }}>{name}</span>
                <div className="flex items-center gap-3">
                  <div style={{ width: '120px', height: '6px', borderRadius: '3px', background: 'rgba(255,255,255,0.1)' }}>
                    <div style={{ width: `${data.score}%`, height: '100%', borderRadius: '3px', background: getScoreColor(data.score), transition: 'width 0.5s' }} />
                  </div>
                  <span style={{ fontSize: '13px', fontWeight: 600, color: getScoreColor(data.score), minWidth: '40px', textAlign: 'right' }}>
                    {data.score}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Manual Text Input */}
      <div className="card">
        <h3 style={{ fontWeight: 600, fontSize: '14px', marginBottom: '12px' }}>Or Paste Resume Text</h3>
        <textarea
          value={resumeText} onChange={e => onChange(e.target.value)}
          placeholder="Paste your resume content here if you don't have a PDF file..."
          rows={8}
          style={{ fontFamily: 'monospace', fontSize: '13px' }}
        />
      </div>
    </div>
  );
}
