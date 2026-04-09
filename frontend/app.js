/**
 * CodeLite++ AI Engine - Frontend Logic
 * Connects the UI to the FastAPI backend.
 */

// --- Global Utilities ---

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach((t, i) => {
        t.classList.toggle('active', i === (tab === 'plagiarism' ? 0 : 1));
    });
    document.getElementById('pPanel').classList.toggle('active', tab === 'plagiarism');
    document.getElementById('oPanel').classList.toggle('active', tab === 'optimizer');
}

function setLoading(btnId, loading) {
    const btn = document.getElementById(btnId);
    if (loading) {
        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div><span>Running...</span>';
    } else {
        btn.disabled = false;
        btn.innerHTML = btnId === 'pBtn' ? '<span>Check plagiarism</span>' : '<span>Optimize code</span>';
    }
}

function showError(id, msg) {
    const el = document.getElementById(id);
    el.textContent = msg;
    el.classList.add('show');
}

function hideError(id) {
    document.getElementById(id).classList.remove('show');
}

// --- Plagiarism Service ---

async function runPlagiarism() {
    const c1 = document.getElementById('code1').value.trim();
    const c2 = document.getElementById('code2').value.trim();
    
    if (!c1 || !c2) {
        showError('pErr', 'Please enter code in both panels.');
        return;
    }

    hideError('pErr');
    document.getElementById('pResults').classList.remove('show');
    setLoading('pBtn', true);

    try {
        const base = document.getElementById('apiBase').value.replace(/\/$/, '');
        const res = await fetch(`${base}/plagiarism-check`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code1: c1, code2: c2 })
        });

        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        
        const d = await res.json();
        if (d.error) throw new Error(d.error);
        
        renderPlagiarism(d);
    } catch (e) {
        showError('pErr', e.message);
    } finally {
        setLoading('pBtn', false);
    }
}

function renderPlagiarism(d) {
    // Final Score & Confidence
    document.getElementById('finalScore').textContent = d.final_score.toFixed(1) + '%';
    const cb = document.getElementById('confBadge');
    cb.textContent = d.confidence + ' confidence';
    cb.className = `confidence conf-${d.confidence}`;

    // Breakdown Bars
    const b = d.breakdown;
    const mappings = [
        ['barAst',     'valAst',     b.ast],
        ['barToken',   'valToken',   b.token],
        ['barPattern', 'valPattern', b.pattern],
        ['barFunc',    'valFunc',    b.function]
    ];

    mappings.forEach(([bar, val, v]) => {
        document.getElementById(bar).style.width = Math.min(v || 0, 100) + '%';
        document.getElementById(val).textContent = (v || 0).toFixed(1) + '%';
    });

    // Verdict Logic
    const vEl = document.getElementById('verdict');
    const vTxt = document.getElementById('verdictText');
    const score = d.final_score;

    if (score >= 70) {
        vEl.className = 'verdict high';
        vTxt.textContent = 'High similarity detected — likely plagiarism.';
    } else if (score >= 40) {
        vEl.className = 'verdict medium';
        vTxt.textContent = 'Moderate similarity — review manually.';
    } else {
        vEl.className = 'verdict low';
        vTxt.textContent = 'Low similarity — likely original work.';
    }

    document.getElementById('pResults').classList.add('show');
}

// --- Optimizer Service ---

async function runOptimizer() {
    const code = document.getElementById('codeOpt').value.trim();
    
    if (!code) {
        showError('oErr', 'Please enter CodeLite++ code to optimize.');
        return;
    }

    hideError('oErr');
    document.getElementById('oResults').classList.remove('show');
    setLoading('oBtn', true);

    try {
        const base = document.getElementById('apiBase').value.replace(/\/$/, '');
        const res = await fetch(`${base}/optimize-code`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });

        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        
        const d = await res.json();
        if (d.error) throw new Error(d.error);
        
        renderOptimizer(d);
    } catch (e) {
        showError('oErr', e.message);
    } finally {
        setLoading('oBtn', false);
    }
}

function renderOptimizer(d) {
    // Code Output
    document.getElementById('optCode').textContent = d.optimized_code || '(no output)';

    // Optimization List
    const list = document.getElementById('optList');
    if (!d.optimizations || d.optimizations.length === 0) {
        list.innerHTML = '<div class="opt-item"><span style="color:var(--text-muted)">No optimizations applied.</span></div>';
    } else {
        list.innerHTML = d.optimizations
            .map(o => `<div class="opt-item"><div class="opt-dot"></div><span>${o}</span></div>`)
            .join('');
    }

    document.getElementById('oResults').classList.add('show');
}