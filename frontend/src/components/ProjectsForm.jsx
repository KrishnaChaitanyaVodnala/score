import { useState } from 'react';
import { FolderGit2, Plus, X, Github, Trash2 } from 'lucide-react';

export default function ProjectsForm({ projects, onChange }) {
    const [form, setForm] = useState({ title: '', description: '', techStack: '', githubUrl: '' });

    const addProject = () => {
        if (!form.title.trim()) return;
        onChange([...projects, {
            title: form.title.trim(),
            description: form.description.trim(),
            techStack: form.techStack.split(',').map(s => s.trim()).filter(Boolean),
            githubUrl: form.githubUrl.trim(),
        }]);
        setForm({ title: '', description: '', techStack: '', githubUrl: '' });
    };

    const removeProject = idx => onChange(projects.filter((_, i) => i !== idx));

    return (
        <div className="animate-fadeIn">
            <div style={{ marginBottom: '24px' }}>
                <h2 className="flex items-center gap-2" style={{ fontSize: '22px', fontWeight: 700, marginBottom: '6px' }}>
                    <FolderGit2 size={24} color="#6366f1" /> Projects
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
                    Add your projects with descriptions and GitHub links. Technical depth is analyzed via NLP. (Weight: 25%)
                </p>
            </div>

            {/* Add Project Form */}
            <div className="card" style={{ marginBottom: '20px' }}>
                <h3 style={{ fontWeight: 600, fontSize: '14px', marginBottom: '16px' }}>Add New Project</h3>
                <div style={{ display: 'grid', gap: '14px' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
                        <div>
                            <label>Project Title *</label>
                            <input value={form.title} onChange={e => setForm({ ...form, title: e.target.value })}
                                placeholder="e.g., E-Commerce Microservices Platform" />
                        </div>
                        <div>
                            <label>GitHub URL</label>
                            <div className="flex items-center gap-2">
                                <Github size={16} color="var(--text-secondary)" style={{ flexShrink: 0 }} />
                                <input value={form.githubUrl} onChange={e => setForm({ ...form, githubUrl: e.target.value })}
                                    placeholder="https://github.com/username/repo" />
                            </div>
                        </div>
                    </div>
                    <div>
                        <label>Tech Stack (comma-separated)</label>
                        <input value={form.techStack} onChange={e => setForm({ ...form, techStack: e.target.value })}
                            placeholder="e.g., React, Node.js, PostgreSQL, Docker, AWS" />
                    </div>
                    <div>
                        <label>Project Description</label>
                        <textarea value={form.description} onChange={e => setForm({ ...form, description: e.target.value })}
                            placeholder="Describe what the project does, technologies used, architecture patterns, key features..." rows={4} />
                    </div>
                    <button className="btn-primary" onClick={addProject} disabled={!form.title.trim()} style={{ justifySelf: 'end' }}>
                        <Plus size={18} /> Add Project
                    </button>
                </div>
            </div>

            {/* Listed Projects */}
            {projects.length > 0 ? (
                <div style={{ display: 'grid', gap: '12px' }}>
                    {projects.map((p, i) => (
                        <div key={i} className="card" style={{ padding: '18px 20px' }}>
                            <div className="flex items-start justify-between" style={{ marginBottom: '10px' }}>
                                <div>
                                    <h4 style={{ fontWeight: 600, fontSize: '16px', marginBottom: '4px' }}>{p.title}</h4>
                                    {p.githubUrl && (
                                        <a href={p.githubUrl} target="_blank" rel="noopener" className="flex items-center gap-1"
                                            style={{ color: 'var(--accent)', fontSize: '13px', textDecoration: 'none' }}>
                                            <Github size={14} /> {p.githubUrl}
                                        </a>
                                    )}
                                </div>
                                <button onClick={() => removeProject(i)} style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }}>
                                    <Trash2 size={18} />
                                </button>
                            </div>
                            {p.techStack?.length > 0 && (
                                <div className="flex flex-wrap" style={{ gap: '6px', marginBottom: '8px' }}>
                                    {p.techStack.map((t, j) => (
                                        <span key={j} style={{
                                            padding: '3px 10px', borderRadius: '12px', fontSize: '12px',
                                            background: 'rgba(6,182,212,0.15)', color: 'var(--accent-light)', border: '1px solid rgba(6,182,212,0.3)'
                                        }}>
                                            {t}
                                        </span>
                                    ))}
                                </div>
                            )}
                            {p.description && <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{p.description}</p>}
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center" style={{ padding: '40px', color: 'var(--text-secondary)' }}>
                    <FolderGit2 size={40} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
                    <p>No projects added yet. Showcase your best work!</p>
                </div>
            )}
        </div>
    );
}
