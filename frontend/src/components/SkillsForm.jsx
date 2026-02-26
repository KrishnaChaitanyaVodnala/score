import { useState, useEffect } from 'react';
import { Search, X, ChevronDown, ChevronUp, Zap } from 'lucide-react';
import { apiUrl } from '../api';

export default function SkillsForm({ skills, onChange }) {
  const [allSkills, setAllSkills] = useState({});
  const [search, setSearch] = useState('');
  const [expanded, setExpanded] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(apiUrl('/api/skills'))
      .then(r => r.json())
      .then(data => { setAllSkills(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const toggleCategory = cat => setExpanded(p => ({ ...p, [cat]: !p[cat] }));

  const addSkill = skill => {
    if (!skills.includes(skill)) onChange([...skills, skill]);
  };

  const removeSkill = skill => onChange(skills.filter(s => s !== skill));

  const filteredCategories = Object.entries(allSkills).map(([cat, info]) => {
    const filtered = info.skills.filter(s =>
      s.toLowerCase().includes(search.toLowerCase()) && !skills.includes(s)
    );
    return { cat, icon: info.icon, skills: filtered, total: info.skills.length };
  }).filter(c => c.skills.length > 0 || search === '');

  if (loading) return (
    <div className="card text-center" style={{ padding: '60px' }}>
      <div style={{ fontSize: '40px', marginBottom: '16px' }}>⏳</div>
      <p style={{ color: 'var(--text-secondary)' }}>Loading skills database...</p>
    </div>
  );

  return (
    <div className="animate-fadeIn">
      <div style={{ marginBottom: '24px' }}>
        <h2 className="flex items-center gap-2" style={{ fontSize: '22px', fontWeight: 700, marginBottom: '6px' }}>
          <Zap size={24} color="#6366f1" /> Technical Skills
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          Select your skills from categorized lists. Skills are weighted by market demand. (Weight: 30%)
        </p>
      </div>

      {/* Selected Skills */}
      {skills.length > 0 && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <div className="flex items-center justify-between" style={{ marginBottom: '12px' }}>
            <span style={{ fontWeight: 600, fontSize: '14px' }}>Selected Skills ({skills.length})</span>
            <button onClick={() => onChange([])} style={{ color: 'var(--danger)', background: 'none', border: 'none', cursor: 'pointer', fontSize: '13px' }}>Clear All</button>
          </div>
          <div className="flex flex-wrap" style={{ gap: '8px' }}>
            {skills.map(s => (
              <span key={s} className="tag">
                {s} <button onClick={() => removeSkill(s)}>×</button>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Search */}
      <div style={{ position: 'relative', marginBottom: '20px' }}>
        <Search size={18} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
        <input
          value={search} onChange={e => setSearch(e.target.value)}
          placeholder="Search skills across all categories..."
          style={{ paddingLeft: '42px' }}
        />
        {search && (
          <button onClick={() => setSearch('')} style={{ position: 'absolute', right: '14px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}>
            <X size={16} />
          </button>
        )}
      </div>

      {/* Categories */}
      <div style={{ display: 'grid', gap: '12px' }}>
        {filteredCategories.map(({ cat, icon, skills: catSkills, total }) => (
          <div key={cat} className="card" style={{ padding: '0', overflow: 'hidden' }}>
            <button
              onClick={() => toggleCategory(cat)}
              className="flex items-center justify-between w-full"
              style={{ padding: '16px 20px', background: 'none', border: 'none', color: 'var(--text-primary)', cursor: 'pointer', width: '100%', textAlign: 'left' }}
            >
              <span className="flex items-center gap-2" style={{ fontWeight: 600, fontSize: '15px' }}>
                <span style={{ fontSize: '20px' }}>{icon}</span> {cat}
                <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 400 }}>({total} skills)</span>
              </span>
              {expanded[cat] ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
            </button>
            {expanded[cat] && (
              <div style={{ padding: '0 20px 16px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {catSkills.length > 0 ? catSkills.map(s => (
                  <button key={s} onClick={() => addSkill(s)}
                    style={{ padding: '6px 14px', borderRadius: '20px', fontSize: '13px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', color: 'var(--text-primary)', cursor: 'pointer', transition: 'all 0.2s' }}
                    onMouseEnter={e => { e.target.style.borderColor = 'var(--primary)'; e.target.style.background = 'rgba(99,102,241,0.1)'; }}
                    onMouseLeave={e => { e.target.style.borderColor = 'var(--border)'; e.target.style.background = 'rgba(255,255,255,0.05)'; }}
                  >
                    + {s}
                  </button>
                )) : (
                  <span style={{ color: 'var(--text-secondary)', fontSize: '13px', padding: '8px 0' }}>
                    All skills in this category have been selected ✓
                  </span>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
