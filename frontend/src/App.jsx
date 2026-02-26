import { useState } from 'react';
import { apiUrl } from './api';
import { Zap, Award, FolderGit2, Briefcase, FileText, BarChart3, ChevronRight, ChevronLeft, Sparkles } from 'lucide-react';
import SkillsForm from './components/SkillsForm';
import CertificationsForm from './components/CertificationsForm';
import ProjectsForm from './components/ProjectsForm';
import InternshipsForm from './components/InternshipsForm';
import ResumeUpload from './components/ResumeUpload';
import ResultsDashboard from './components/ResultsDashboard';

const STEPS = [
  { id: 0, label: 'Skills', icon: Zap, weight: 30 },
  { id: 1, label: 'Certifications', icon: Award, weight: 15 },
  { id: 2, label: 'Projects', icon: FolderGit2, weight: 25 },
  { id: 3, label: 'Internships', icon: Briefcase, weight: 20 },
  { id: 4, label: 'Resume', icon: FileText, weight: 10 },
  { id: 5, label: 'Results', icon: BarChart3, weight: null },
];

export default function App() {
  const [step, setStep] = useState(0);
  const [data, setData] = useState({
    skills: [],
    certifications: [],
    projects: [],
    internships: [],
    resumeText: '',
    resumeFile: null,
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const updateData = (key, value) => setData(prev => ({ ...prev, [key]: value }));

  const calculateScore = async () => {
    setLoading(true);
    try {
      const payload = {
        skills: data.skills,
        certifications: data.certifications.map(c => ({
          name: c.name, issuer: c.issuer || '', year: c.year || 2024
        })),
        projects: data.projects.map(p => ({
          title: p.title, description: p.description || '',
          tech_stack: p.techStack || [], github_url: p.githubUrl || ''
        })),
        internships: data.internships.map(i => ({
          company: i.company, role: i.role || '',
          duration_months: i.durationMonths || 1,
          achievements: i.achievements || '',
          has_certificate: i.hasCertificate || false
        })),
        resume_text: data.resumeText || '',
      };

      const res = await fetch(apiUrl('/api/score/calculate'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const result = await res.json();
      setResults(result);
      setStep(5);
    } catch (err) {
      console.error('Error calculating score:', err);
      alert('Error connecting to backend. Make sure the FastAPI server is running on port 8000.');
    }
    setLoading(false);
  };

  const renderStep = () => {
    switch (step) {
      case 0: return <SkillsForm skills={data.skills} onChange={v => updateData('skills', v)} />;
      case 1: return <CertificationsForm certs={data.certifications} onChange={v => updateData('certifications', v)} />;
      case 2: return <ProjectsForm projects={data.projects} onChange={v => updateData('projects', v)} />;
      case 3: return <InternshipsForm internships={data.internships} onChange={v => updateData('internships', v)} />;
      case 4: return <ResumeUpload resumeText={data.resumeText} onChange={v => updateData('resumeText', v)} />;
      case 5: return <ResultsDashboard results={results} />;
      default: return null;
    }
  };

  return (
    <div className="min-h-screen" style={{ padding: '20px' }}>
      {/* Header */}
      <header className="text-center" style={{ marginBottom: '32px', paddingTop: '20px' }}>
        <div className="flex items-center justify-center gap-3" style={{ marginBottom: '8px' }}>
          <Sparkles size={32} color="#6366f1" />
          <h1 style={{ fontSize: '32px', fontWeight: 800, background: 'linear-gradient(135deg, #6366f1, #06b6d4)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Career Readiness Score
          </h1>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
          AI-powered career assessment across Skills, Certifications, Projects, Internships & Resume
        </p>
      </header>

      {/* Stepper */}
      <nav className="glass" style={{ maxWidth: '900px', margin: '0 auto 32px', padding: '16px 24px' }}>
        <div className="flex items-center justify-between" style={{ gap: '4px' }}>
          {STEPS.map((s, i) => {
            const Icon = s.icon;
            const isActive = i === step;
            const isDone = i < step;
            return (
              <button
                key={s.id}
                onClick={() => { if (i <= step || isDone) setStep(i); }}
                className="flex items-center gap-2"
                style={{
                  padding: '10px 16px',
                  borderRadius: '10px',
                  border: 'none',
                  cursor: i <= step ? 'pointer' : 'default',
                  background: isActive ? 'rgba(99,102,241,0.2)' : 'transparent',
                  color: isActive ? '#818cf8' : isDone ? '#10b981' : 'var(--text-secondary)',
                  fontWeight: isActive ? 600 : 400,
                  fontSize: '13px',
                  transition: 'all 0.3s',
                  flex: 1,
                  justifyContent: 'center',
                }}
              >
                <Icon size={18} />
                <span className="hidden sm:inline">{s.label}</span>
                {s.weight && <span style={{ fontSize: '11px', opacity: 0.6 }}>({s.weight}%)</span>}
              </button>
            );
          })}
        </div>
      </nav>

      {/* Content */}
      <main className="animate-fadeIn" key={step} style={{ maxWidth: '900px', margin: '0 auto' }}>
        {renderStep()}
      </main>

      {/* Navigation Buttons */}
      {step < 5 && (
        <div className="flex justify-between" style={{ maxWidth: '900px', margin: '24px auto 40px', gap: '16px' }}>
          <button className="btn-secondary" onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0}
            style={{ opacity: step === 0 ? 0.3 : 1 }}>
            <ChevronLeft size={18} style={{ display: 'inline', verticalAlign: 'middle' }} /> Previous
          </button>
          {step < 4 ? (
            <button className="btn-primary" onClick={() => setStep(step + 1)}>
              Next <ChevronRight size={18} />
            </button>
          ) : (
            <button className="btn-primary" onClick={calculateScore} disabled={loading}
              style={loading ? {} : { background: 'linear-gradient(135deg, #10b981, #059669)' }}>
              {loading ? '⏳ Calculating...' : '🚀 Calculate Career Score'}
            </button>
          )}
        </div>
      )}
    </div>
  );
}
