import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, RadialBarChart, RadialBar, Legend } from 'recharts';
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle2, Lightbulb, Target, ArrowUp, RotateCcw } from 'lucide-react';

const COLORS = { skills: '#6366f1', certifications: '#06b6d4', projects: '#10b981', internships: '#f59e0b', resume: '#ec4899' };
const LABELS = { skills: 'Skills', certifications: 'Certifications', projects: 'Projects', internships: 'Internships', resume: 'Resume' };
const WEIGHTS = { skills: 30, certifications: 15, projects: 25, internships: 20, resume: 10 };

const getColor = s => s >= 80 ? '#10b981' : s >= 60 ? '#eab308' : s >= 40 ? '#f97316' : '#ef4444';

function ScoreGauge({ score, size = 200 }) {
    const r = (size - 20) / 2;
    const circ = 2 * Math.PI * r;
    const pct = Math.min(score, 100) / 100;
    const offset = circ * (1 - pct);
    const color = getColor(score);

    return (
        <div style={{ position: 'relative', width: size, height: size, margin: '0 auto' }}>
            <svg width={size} height={size} className="progress-ring">
                <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="12" />
                <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth="12"
                    strokeDasharray={circ} strokeDashoffset={offset}
                    strokeLinecap="round" style={{ transition: 'stroke-dashoffset 1.5s ease-out' }} />
            </svg>
            <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center' }}>
                <div style={{ fontSize: size / 4, fontWeight: 800, color, lineHeight: 1 }}>{Math.round(score)}</div>
                <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>/ 100</div>
            </div>
        </div>
    );
}

export default function ResultsDashboard({ results }) {
    if (!results) return (
        <div className="card text-center" style={{ padding: '60px' }}>
            <Target size={48} style={{ margin: '0 auto 16px', opacity: 0.3 }} />
            <p style={{ color: 'var(--text-secondary)' }}>Complete all sections and calculate to see results.</p>
        </div>
    );

    const { final, components, suggestions } = results;
    const { final_score, overall_grade, component_breakdown, strongest_areas, weakest_areas } = final;

    const barData = Object.entries(component_breakdown).map(([key, val]) => ({
        name: LABELS[key] || key, score: val.raw_score, weight: val.weight,
        weighted: val.weighted_score, fill: COLORS[key] || '#6366f1',
    }));

    const radarData = Object.entries(component_breakdown).map(([key, val]) => ({
        subject: LABELS[key], A: val.raw_score, fullMark: 100, fill: COLORS[key],
    }));

    return (
        <div className="animate-slideUp">
            {/* Hero Score */}
            <div className="glass-strong text-center" style={{ padding: '40px 24px', marginBottom: '24px' }}>
                <h2 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '20px' }}>
                    Your Career Readiness Score
                </h2>
                <ScoreGauge score={final_score} size={220} />
                <div style={{ marginTop: '16px' }}>
                    <span style={{
                        fontSize: '24px', fontWeight: 800, color: overall_grade.color, padding: '6px 20px',
                        borderRadius: '12px', background: `${overall_grade.color}15`, border: `1px solid ${overall_grade.color}30`
                    }}>
                        {overall_grade.grade} — {overall_grade.label}
                    </span>
                </div>
            </div>

            {/* Component Cards Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '14px', marginBottom: '24px' }}>
                {Object.entries(component_breakdown).map(([key, data]) => (
                    <div key={key} className="card" style={{ padding: '18px' }}>
                        <div className="flex items-center justify-between" style={{ marginBottom: '12px' }}>
                            <span style={{ fontWeight: 600, fontSize: '14px', color: COLORS[key] }}>{LABELS[key]}</span>
                            <span style={{
                                fontSize: '11px', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.05)',
                                padding: '2px 8px', borderRadius: '6px'
                            }}>Weight: {data.weight}%</span>
                        </div>
                        <div className="flex items-end gap-3">
                            <span style={{ fontSize: '32px', fontWeight: 800, color: data.grade.color, lineHeight: 1 }}>
                                {Math.round(data.raw_score)}
                            </span>
                            <span style={{ fontSize: '12px', color: data.grade.color, fontWeight: 600, paddingBottom: '4px' }}>
                                {data.grade.grade}
                            </span>
                        </div>
                        <div style={{ marginTop: '10px', height: '6px', borderRadius: '3px', background: 'rgba(255,255,255,0.06)' }}>
                            <div style={{
                                width: `${data.raw_score}%`, height: '100%', borderRadius: '3px',
                                background: `linear-gradient(90deg, ${COLORS[key]}, ${data.grade.color})`,
                                transition: 'width 1s ease-out'
                            }} />
                        </div>
                        <div style={{ marginTop: '6px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                            Contributes {data.weighted_score.toFixed(1)} pts to final score
                        </div>
                    </div>
                ))}
            </div>

            {/* Bar Chart */}
            <div className="card" style={{ marginBottom: '24px' }}>
                <h3 style={{ fontWeight: 600, fontSize: '16px', marginBottom: '16px' }}>Category Breakdown</h3>
                <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={barData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                        <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
                        <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} domain={[0, 100]} />
                        <Tooltip contentStyle={{ background: '#1a1a2e', border: '1px solid #334155', borderRadius: '8px', color: '#e2e8f0' }}
                            formatter={(val, name) => [`${val}`, name === 'score' ? 'Raw Score' : 'Weighted']} />
                        <Bar dataKey="score" radius={[6, 6, 0, 0]}>
                            {barData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Strengths & Weaknesses */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '24px' }}>
                <div className="card" style={{ borderColor: 'rgba(16,185,129,0.3)' }}>
                    <h3 className="flex items-center gap-2" style={{ fontWeight: 600, fontSize: '14px', marginBottom: '14px', color: '#10b981' }}>
                        <TrendingUp size={18} /> Strongest Areas
                    </h3>
                    {strongest_areas?.map((a, i) => (
                        <div key={i} className="flex items-center justify-between" style={{ padding: '8px 0', borderBottom: i < strongest_areas.length - 1 ? '1px solid var(--border)' : 'none' }}>
                            <span style={{ fontSize: '14px' }}>{LABELS[a.name] || a.name}</span>
                            <span style={{ fontWeight: 700, color: getColor(a.score) }}>{Math.round(a.score)}</span>
                        </div>
                    ))}
                </div>
                <div className="card" style={{ borderColor: 'rgba(239,68,68,0.3)' }}>
                    <h3 className="flex items-center gap-2" style={{ fontWeight: 600, fontSize: '14px', marginBottom: '14px', color: '#ef4444' }}>
                        <TrendingDown size={18} /> Areas to Improve
                    </h3>
                    {weakest_areas?.map((a, i) => (
                        <div key={i} className="flex items-center justify-between" style={{ padding: '8px 0', borderBottom: i < weakest_areas.length - 1 ? '1px solid var(--border)' : 'none' }}>
                            <span style={{ fontSize: '14px' }}>{LABELS[a.name] || a.name}</span>
                            <span style={{ fontWeight: 700, color: getColor(a.score) }}>{Math.round(a.score)}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Resume ATS Breakdown */}
            {components?.resume?.section_scores && Object.keys(components.resume.section_scores).length > 0 && (
                <div className="card" style={{ marginBottom: '24px' }}>
                    <h3 className="flex items-center gap-2" style={{ fontWeight: 600, fontSize: '16px', marginBottom: '16px' }}>
                        📄 Resume ATS Score Breakdown
                    </h3>
                    <div style={{ display: 'grid', gap: '8px' }}>
                        {Object.entries(components.resume.section_scores).map(([name, data]) => (
                            <div key={name} className="flex items-center justify-between" style={{ padding: '10px 14px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                                <div className="flex items-center gap-2">
                                    <span style={{ fontSize: '14px' }}>{name}</span>
                                    <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>({data.weight}%)</span>
                                </div>
                                <div className="flex items-center gap-3">
                                    <div style={{ width: '100px', height: '6px', borderRadius: '3px', background: 'rgba(255,255,255,0.06)' }}>
                                        <div style={{ width: `${data.score}%`, height: '100%', borderRadius: '3px', background: getColor(data.score) }} />
                                    </div>
                                    <span style={{ fontSize: '14px', fontWeight: 700, color: getColor(data.score), minWidth: '40px', textAlign: 'right' }}>
                                        {Math.round(data.score)}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Improvement Suggestions */}
            {suggestions && (
                <div className="card" style={{ borderColor: 'rgba(99,102,241,0.3)' }}>
                    <h3 className="flex items-center gap-2" style={{ fontWeight: 600, fontSize: '16px', marginBottom: '16px' }}>
                        <Lightbulb size={20} color="#fbbf24" /> Improvement Suggestions
                    </h3>
                    {suggestions.top_priority_actions?.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            <h4 className="flex items-center gap-2" style={{ fontSize: '13px', fontWeight: 600, color: '#ef4444', marginBottom: '10px' }}>
                                <ArrowUp size={14} /> Top Priority Actions
                            </h4>
                            <div style={{ display: 'grid', gap: '8px' }}>
                                {suggestions.top_priority_actions.map((s, i) => (
                                    <div key={i} className="flex items-start gap-3" style={{ padding: '10px 14px', background: 'rgba(239,68,68,0.05)', borderRadius: '8px', border: '1px solid rgba(239,68,68,0.15)' }}>
                                        <AlertTriangle size={16} color="#ef4444" style={{ flexShrink: 0, marginTop: '2px' }} />
                                        <div>
                                            <span style={{ fontSize: '13px', lineHeight: 1.5 }}>{s.text}</span>
                                            <span style={{ fontSize: '11px', color: COLORS[s.component], marginLeft: '8px', fontWeight: 500 }}>
                                                [{LABELS[s.component]}]
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                    {suggestions.all_suggestions?.length > 0 && (
                        <div>
                            <h4 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '10px' }}>
                                All Recommendations ({suggestions.total_suggestions})
                            </h4>
                            <div style={{ display: 'grid', gap: '6px', maxHeight: '300px', overflowY: 'auto' }}>
                                {suggestions.all_suggestions.map((s, i) => (
                                    <div key={i} className="flex items-start gap-3" style={{ padding: '8px 12px', borderRadius: '6px', background: 'rgba(255,255,255,0.02)' }}>
                                        <CheckCircle2 size={14} color={s.impact === 'high' ? '#ef4444' : s.impact === 'medium' ? '#eab308' : '#10b981'}
                                            style={{ flexShrink: 0, marginTop: '3px' }} />
                                        <span style={{ fontSize: '13px', lineHeight: 1.5, color: 'var(--text-secondary)' }}>
                                            {s.text}
                                            <span style={{ color: COLORS[s.component], marginLeft: '6px', fontSize: '11px' }}>
                                                [{LABELS[s.component]} — {s.score}/100]
                                            </span>
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Try Again */}
            <div className="text-center" style={{ marginTop: '32px', paddingBottom: '40px' }}>
                <button className="btn-secondary" onClick={() => window.location.reload()}
                    style={{ padding: '14px 32px', fontSize: '15px' }}>
                    <RotateCcw size={18} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '8px' }} />
                    Start New Assessment
                </button>
            </div>
        </div>
    );
}
