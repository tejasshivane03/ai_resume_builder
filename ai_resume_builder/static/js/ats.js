/**
 * ats.js — ATS checker page interactivity
 */
document.addEventListener('DOMContentLoaded', () => {
    initSourceTabs();
    initFileUpload();
});

// ── Source tabs (paste / upload / existing) ──────────────────────────
function initSourceTabs() {
    document.querySelectorAll('.source-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const source = tab.dataset.source;

            // Activate tab
            document.querySelectorAll('.source-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Show matching content
            document.querySelectorAll('.ats-source-content').forEach(c => c.classList.remove('active'));
            const content = document.querySelector(`[data-source-content="${source}"]`);
            if (content) content.classList.add('active');

            // Update hidden input
            document.getElementById('source-value').value = source;
        });
    });
}

// ── File upload drag & drop ─────────────────────────────────────────
function initFileUpload() {
    const area = document.getElementById('file-upload-area');
    if (!area) return;

    const input = document.getElementById('resume_file');

    area.addEventListener('dragover', e => {
        e.preventDefault();
        area.classList.add('dragover');
    });
    area.addEventListener('dragleave', () => {
        area.classList.remove('dragover');
    });
    area.addEventListener('drop', e => {
        e.preventDefault();
        area.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;
            updateFileLabel(e.dataTransfer.files[0].name);
        }
    });
    input.addEventListener('change', () => {
        if (input.files.length) {
            updateFileLabel(input.files[0].name);
        }
    });
}

function updateFileLabel(name) {
    const label = document.querySelector('.file-upload-label');
    if (label) {
        label.innerHTML = `
            <span class="file-icon">✅</span>
            <span><strong>${name}</strong> selected</span>
        `;
    }
}
