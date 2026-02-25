import { useState } from 'react';
import { Briefcase, Plus, Trash2, CheckCircle } from 'lucide-react';

export default function InternshipsForm({ internships, onChange }) {
  const [form, setForm] = useState({ company: '', role: '', durationMonths: 3, achievements: '', hasCertificate: false });

  const addInternship = () => {
    if (!form.company.trim()) return;
    onChange([...internships, { ...form, company: form.company.trim(), role: form.role.trim(), achievements: form.achievements.trim() }]);
    setForm({ company: '', role: '', durationMonths: 3, achievements: '', hasCertificate: false });
  };

  const removeInternship = idx => onChange(internships.filter((_, i) => i !== idx));

  return (
    <div className="animate-fadeIn">
      <div style={{ marginBottom: '24px' }}>
        <h2 className="flex items-center gap-2" style={{ fontSize: '22px', fontWeight: 700, marginBottom: '6px' }}>
          <Briefcase size={24} color="#6366f1" /> Internships
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          Add your internship experiences. Company tier and achievements are scored. (Weight: 20%)
        </p>
      </div>

      {/* Add Form */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3 style={{ fontWeight: 600, fontSize: '14px', marginBottom: '16px' }}>Add Internship</h3>
        <div style={{ display: 'grid', gap: '14px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div>
              <label>Company Name *</label>
              <input value={form.company} onChange={e => setForm({ ...form, company: e.target.value })}
                placeholder="e.g., Google, Microsoft, Infosys" />
            </div>
            <div>
              <label>Role / Position</label>
              <input value={form.role} onChange={e => setForm({ ...form, role: e.target.value })}
                placeholder="e.g., Software Engineer Intern" />
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div>
              <label>Duration (Months)</label>
              <input type="number" min="1" max="24" value={form.durationMonths}
                onChange={e => setForm({ ...form, durationMonths: parseInt(e.target.value) || 1 })} />
            </div>
            <div style={{ display: 'flex', alignItems: 'end', gap: '8px', paddingBottom: '8px' }}>
              <label className="flex items-center gap-2" style={{ cursor: 'pointer', marginBottom: 0 }}>
                <input type="checkbox" checked={form.hasCertificate}
                  onChange={e => setForm({ ...form, hasCertificate: e.target.checked })}
                  style={{ width: 'auto', accentColor: 'var(--primary)' }} />
                <span style={{ fontSize: '14px', color: 'var(--text-primary)' }}>Has Completion Certificate</span>
              </label>
            </div>
          </div>
          <div>
            <label>Key Achievements</label>
            <textarea value={form.achievements} onChange={e => setForm({ ...form, achievements: e.target.value })}
              placeholder="Describe your key achievements, contributions, and impact during the internship..." rows={3} />
          </div>
          <button className="btn-primary" onClick={addInternship} disabled={!form.company.trim()} style={{ justifySelf: 'end' }}>
            <Plus size={18} /> Add Internship
          </button>
        </div>
      </div>

      {/* Listed Internships */}
      {internships.length > 0 ? (
        <div style={{ display: 'grid', gap: '12px' }}>
          {internships.map((intern, i) => (
            <div key={i} className="card" style={{ padding: '18px 20px' }}>
              <div className="flex items-start justify-between" style={{ marginBottom: '8px' }}>
                <div>
                  <h4 style={{ fontWeight: 600, fontSize: '16px', marginBottom: '2px' }}>{intern.role || 'Intern'}</h4>
                  <p style={{ color: 'var(--accent)', fontSize: '14px' }}>{intern.company}</p>
                </div>
                <div className="flex items-center gap-3">
                  <span style={{ fontSize: '13px', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.05)', padding: '4px 10px', borderRadius: '8px' }}>
                    {intern.durationMonths} month{intern.durationMonths !== 1 ? 's' : ''}
                  </span>
                  {intern.hasCertificate && <CheckCircle size={18} color="var(--success)" />}
                  <button onClick={() => removeInternship(i)} style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }}>
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
              {intern.achievements && (
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{intern.achievements}</p>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center" style={{ padding: '40px', color: 'var(--text-secondary)' }}>
          <Briefcase size={40} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
          <p>No internships added yet. Add your work experience above.</p>
        </div>
      )}
    </div>
  );
}
