/**
 * builder.js — Resume builder interactive functionality
 * Depends on globals: RESUME_PK, CSRF_TOKEN, INITIAL_DATA (set in template)
 */

// ── State ────────────────────────────────────────────────────────────────
let experienceData = INITIAL_DATA.experience || [];
let educationData = INITIAL_DATA.education || [];
let skillsData = INITIAL_DATA.skills || [];
let projectsData = INITIAL_DATA.projects || [];

// ── Init ─────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    renderExperience();
    renderEducation();
    renderSkills();
    renderProjects();
    initSkillInput();
});

// ═══════════════════════════════════════════════════════════════════════
// Tabs
// ═══════════════════════════════════════════════════════════════════════
function initTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            // Toggle buttons
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            // Toggle content
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            const content = document.querySelector(`[data-tab-content="${tab}"]`);
            if (content) content.classList.add('active');
        });
    });
}

// ═══════════════════════════════════════════════════════════════════════
// Experience
// ═══════════════════════════════════════════════════════════════════════
function addExperience() {
    experienceData.push({ title: '', company: '', start_date: '', end_date: '', description: '' });
    renderExperience();
}

function removeExperience(idx) {
    experienceData.splice(idx, 1);
    renderExperience();
}

function renderExperience() {
    const container = document.getElementById('experience-list');
    if (!container) return;
    container.innerHTML = experienceData.map((exp, i) => `
        <div class="entry-card" id="exp-card-${i}">
            <button type="button" class="entry-remove" onclick="removeExperience(${i})" aria-label="Remove">&times;</button>
            <div class="form-row">
                <div class="form-group">
                    <label>Job Title</label>
                    <input type="text" class="form-input" value="${esc(exp.title)}"
                           onchange="experienceData[${i}].title = this.value" placeholder="Job title">
                </div>
                <div class="form-group">
                    <label>Company</label>
                    <input type="text" class="form-input" value="${esc(exp.company)}"
                           onchange="experienceData[${i}].company = this.value" placeholder="Company name">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Start Date</label>
                    <input type="text" class="form-input" value="${esc(exp.start_date)}"
                           onchange="experienceData[${i}].start_date = this.value" placeholder="e.g. Jan 2022">
                </div>
                <div class="form-group">
                    <label>End Date</label>
                    <input type="text" class="form-input" value="${esc(exp.end_date)}"
                           onchange="experienceData[${i}].end_date = this.value" placeholder="e.g. Present">
                </div>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea class="form-input" rows="3"
                          onchange="experienceData[${i}].description = this.value"
                          placeholder="Describe your responsibilities and achievements…">${esc(exp.description)}</textarea>
                <button type="button" class="btn btn-sm btn-ai" style="margin-top:6px"
                        onclick="aiImproveExp(${i})">✨ Improve with AI</button>
            </div>
        </div>
    `).join('');

    if (experienceData.length === 0) {
        container.innerHTML = '<p style="color:var(--clr-text-muted);font-size:var(--fs-sm);margin-bottom:var(--sp-4);">No experience added yet. Click "+ Add" to begin.</p>';
    }
}

// ═══════════════════════════════════════════════════════════════════════
// Education
// ═══════════════════════════════════════════════════════════════════════
function addEducation() {
    educationData.push({ degree: '', school: '', start_date: '', end_date: '', description: '' });
    renderEducation();
}

function removeEducation(idx) {
    educationData.splice(idx, 1);
    renderEducation();
}

function renderEducation() {
    const container = document.getElementById('education-list');
    if (!container) return;
    container.innerHTML = educationData.map((edu, i) => `
        <div class="entry-card" id="edu-card-${i}">
            <button type="button" class="entry-remove" onclick="removeEducation(${i})" aria-label="Remove">&times;</button>
            <div class="form-row">
                <div class="form-group">
                    <label>Degree / Certificate</label>
                    <input type="text" class="form-input" value="${esc(edu.degree)}"
                           onchange="educationData[${i}].degree = this.value" placeholder="e.g. B.Tech Computer Science">
                </div>
                <div class="form-group">
                    <label>School / University</label>
                    <input type="text" class="form-input" value="${esc(edu.school)}"
                           onchange="educationData[${i}].school = this.value" placeholder="Institution name">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Start Date</label>
                    <input type="text" class="form-input" value="${esc(edu.start_date)}"
                           onchange="educationData[${i}].start_date = this.value" placeholder="e.g. Aug 2019">
                </div>
                <div class="form-group">
                    <label>End Date</label>
                    <input type="text" class="form-input" value="${esc(edu.end_date)}"
                           onchange="educationData[${i}].end_date = this.value" placeholder="e.g. May 2023">
                </div>
            </div>
            <div class="form-group">
                <label>Description (optional)</label>
                <textarea class="form-input" rows="2"
                          onchange="educationData[${i}].description = this.value"
                          placeholder="GPA, honors, relevant coursework…">${esc(edu.description)}</textarea>
            </div>
        </div>
    `).join('');

    if (educationData.length === 0) {
        container.innerHTML = '<p style="color:var(--clr-text-muted);font-size:var(--fs-sm);margin-bottom:var(--sp-4);">No education added yet. Click "+ Add" to begin.</p>';
    }
}

// ═══════════════════════════════════════════════════════════════════════
// Skills
// ═══════════════════════════════════════════════════════════════════════
function initSkillInput() {
    const input = document.getElementById('skill-input');
    if (!input) return;
    input.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addSkillFromInput();
        }
    });
}

function addSkillFromInput() {
    const input = document.getElementById('skill-input');
    const val = input.value.trim();
    if (val && !skillsData.includes(val)) {
        skillsData.push(val);
        renderSkills();
    }
    input.value = '';
    input.focus();
}

function removeSkill(idx) {
    skillsData.splice(idx, 1);
    renderSkills();
}

function addSuggestedSkill(skill) {
    if (!skillsData.includes(skill)) {
        skillsData.push(skill);
        renderSkills();
    }
}

function renderSkills() {
    const container = document.getElementById('skills-tags');
    if (!container) return;
    container.innerHTML = skillsData.map((s, i) => `
        <span class="skill-tag">
            ${esc(s)}
            <button type="button" class="remove-skill" onclick="removeSkill(${i})" aria-label="Remove">&times;</button>
        </span>
    `).join('');
}

async function suggestSkills() {
    const jobTitle = document.getElementById('suggest-job-title').value.trim();
    if (!jobTitle) { alert('Please enter a job title.'); return; }

    try {
        const res = await fetch(`/resume/${RESUME_PK}/ai-improve/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
            body: JSON.stringify({ action: 'suggest_skills', job_title: jobTitle, current_skills: skillsData }),
        });
        const data = await res.json();
        if (data.skills && data.skills.length) {
            const box = document.getElementById('suggested-skills');
            box.style.display = 'block';
            box.innerHTML = `<h4>Suggested skills for "${esc(jobTitle)}":</h4>` +
                data.skills.map(s => `<span class="skill-suggest" onclick="addSuggestedSkill('${esc(s)}')">${esc(s)}</span>`).join(' ');
        }
    } catch (err) {
        console.error('Suggest skills error:', err);
    }
}

// ═══════════════════════════════════════════════════════════════════════
// Projects
// ═══════════════════════════════════════════════════════════════════════
function addProject() {
    projectsData.push({ name: '', description: '', url: '' });
    renderProjects();
}

function removeProject(idx) {
    projectsData.splice(idx, 1);
    renderProjects();
}

function renderProjects() {
    const container = document.getElementById('projects-list');
    if (!container) return;
    container.innerHTML = projectsData.map((proj, i) => `
        <div class="entry-card" id="proj-card-${i}">
            <button type="button" class="entry-remove" onclick="removeProject(${i})" aria-label="Remove">&times;</button>
            <div class="form-row">
                <div class="form-group">
                    <label>Project Name</label>
                    <input type="text" class="form-input" value="${esc(proj.name)}"
                           onchange="projectsData[${i}].name = this.value" placeholder="Project name">
                </div>
                <div class="form-group">
                    <label>URL (optional)</label>
                    <input type="text" class="form-input" value="${esc(proj.url || '')}"
                           onchange="projectsData[${i}].url = this.value" placeholder="https://...">
                </div>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea class="form-input" rows="3"
                          onchange="projectsData[${i}].description = this.value"
                          placeholder="What does this project do? Technologies used?">${esc(proj.description)}</textarea>
            </div>
        </div>
    `).join('');

    if (projectsData.length === 0) {
        container.innerHTML = '<p style="color:var(--clr-text-muted);font-size:var(--fs-sm);margin-bottom:var(--sp-4);">No projects added yet. Click "+ Add" to begin.</p>';
    }
}

// ═══════════════════════════════════════════════════════════════════════
// Save sections (AJAX)
// ═══════════════════════════════════════════════════════════════════════
async function saveSection(section) {
    const dataMap = {
        experience: experienceData,
        education: educationData,
        skills: skillsData,
        projects: projectsData,
    };

    const btn = document.getElementById(`save-${section}`);
    const origText = btn.textContent;
    btn.textContent = 'Saving…';
    btn.disabled = true;

    try {
        const res = await fetch(`/resume/${RESUME_PK}/save-section/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
            body: JSON.stringify({ section, content: dataMap[section] }),
        });
        const data = await res.json();
        if (data.status === 'ok') {
            btn.textContent = '✓ Saved!';
            setTimeout(() => { btn.textContent = origText; btn.disabled = false; }, 2000);
        } else {
            throw new Error(data.error || 'Save failed');
        }
    } catch (err) {
        btn.textContent = 'Error – try again';
        btn.disabled = false;
        console.error('Save error:', err);
    }
}

// ═══════════════════════════════════════════════════════════════════════
// AI Improve
// ═══════════════════════════════════════════════════════════════════════
async function aiImprove(field) {
    if (field === 'summary') {
        const textarea = document.getElementById('id_summary');
        if (!textarea || !textarea.value.trim()) {
            alert('Please write a summary first.');
            return;
        }
        const btn = document.getElementById('ai-improve-summary');
        btn.textContent = 'Improving…';
        btn.disabled = true;

        try {
            const res = await fetch(`/resume/${RESUME_PK}/ai-improve/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
                body: JSON.stringify({ action: 'improve_summary', text: textarea.value }),
            });
            const data = await res.json();
            if (data.improved_text) {
                textarea.value = data.improved_text;
            }
        } catch (err) {
            console.error('AI improve error:', err);
        }
        btn.textContent = '✨ Improve with AI';
        btn.disabled = false;
    }
}

async function aiImproveExp(idx) {
    const desc = experienceData[idx].description;
    if (!desc.trim()) { alert('Please write a description first.'); return; }

    try {
        const res = await fetch(`/resume/${RESUME_PK}/ai-improve/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
            body: JSON.stringify({
                action: 'improve_experience',
                text: desc,
                job_title: experienceData[idx].title,
            }),
        });
        const data = await res.json();
        if (data.improved_text) {
            experienceData[idx].description = data.improved_text;
            renderExperience();
        }
    } catch (err) {
        console.error('AI improve error:', err);
    }
}

// ── Utility ──────────────────────────────────────────────────────────────
function esc(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
