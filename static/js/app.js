// Indian Trademark Registry Search Tool - Frontend JavaScript

class TrademarkSearchApp {
    constructor() {
        this.statusCheckInterval = null;
        this.currentStatus = 'idle';
        this.initializeEventListeners();
        this.showAlert('Application loaded successfully', 'success');
    }

    initializeEventListeners() {
        // Search form submission
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startSearch();
        });

        // CAPTCHA form submission
        document.getElementById('captchaForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitSearch();
        });

        // Reset button
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetSearch();
        });

        // Export button
        document.getElementById('exportBtn').addEventListener('click', () => {
            this.exportResults();
        });

        // New search button
        document.getElementById('newSearchBtn').addEventListener('click', () => {
            this.newSearch();
        });

        // CAPTCHA input enter key
        document.getElementById('captchaInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.submitSearch();
            }
        });
    }

    async startSearch() {
        const wordmark = document.getElementById('wordmark').value.trim();
        const trademarkClass = document.getElementById('class').value.trim();
        const filterType = document.getElementById('filter').value;

        if (!wordmark) {
            this.showAlert('Please enter a wordmark to search', 'error');
            return;
        }

        // Hide all sections except search
        this.hideAllSections();
        this.showSection('statusSection');
        
        // Show loading
        this.showLoading();
        this.updateStatus('Initializing browser...', 0);

        try {
            const response = await fetch('/start_search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    wordmark: wordmark,
                    class: trademarkClass,
                    filter: filterType
                })
            });

            const data = await response.json();
            
            if (data.success) {
                // Start polling for status updates
                this.startStatusPolling();
                this.hideLoading();
            } else {
                this.hideLoading();
                this.showAlert(data.message, 'error');
                this.hideAllSections();
            }
        } catch (error) {
            this.hideLoading();
            this.showAlert('Network error: ' + error.message, 'error');
            this.hideAllSections();
        }
    }

    startStatusPolling() {
        this.statusCheckInterval = setInterval(async () => {
            try {
                const response = await fetch('/get_status');
                const data = await response.json();
                
                this.handleStatusUpdate(data);
            } catch (error) {
                console.error('Status check error:', error);
            }
        }, 1000); // Check every second
    }

    handleStatusUpdate(data) {
        const status = data.status;

        if (status === this.currentStatus) {
            return; // No change
        }

        this.currentStatus = status;

        switch (status) {
            case 'captcha_ready':
                this.stopStatusPolling();
                this.showCaptcha(data.captcha);
                break;
            
            case 'searching':
                this.updateSearchProgress(data.progress || 0, data.message || 'Searching...');
                break;
            
            case 'complete':
                this.stopStatusPolling();
                this.showResults(data.results_count || 0);
                break;
            
            case 'error':
                this.stopStatusPolling();
                this.showAlert('Search error: ' + (data.error || 'Unknown error'), 'error');
                this.hideAllSections();
                break;
        }
    }

    showCaptcha(captchaData) {
        this.hideAllSections();
        this.showSection('captchaSection');
        
        const captchaImage = document.getElementById('captchaImage');
        captchaImage.src = 'data:image/png;base64,' + captchaData;
        
        // Focus on CAPTCHA input
        document.getElementById('captchaInput').focus();
        
        this.showAlert('Please enter the CAPTCHA to continue', 'info');
    }

    async submitSearch() {
        const captcha = document.getElementById('captchaInput').value.trim();
        
        if (!captcha) {
            this.showAlert('Please enter the CAPTCHA text', 'error');
            return;
        }

        this.showLoading();
        this.hideSection('captchaSection');
        this.showSection('statusSection');
        this.updateStatus('Submitting search...', 10);

        try {
            const response = await fetch('/submit_search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    captcha: captcha
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.hideLoading();
                this.startStatusPolling();
            } else {
                this.hideLoading();
                this.showAlert(data.message, 'error');
                // Show CAPTCHA again
                this.showSection('captchaSection');
            }
        } catch (error) {
            this.hideLoading();
            this.showAlert('Network error: ' + error.message, 'error');
            this.showSection('captchaSection');
        }
    }

    updateSearchProgress(progress, message) {
        this.updateStatus(message, progress);
        
        const progressBar = document.getElementById('progressBar');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        progressBar.style.display = 'block';
        progressFill.style.width = progress + '%';
        progressText.textContent = progress + '%';
    }

    async showResults(resultCount) {
        this.hideAllSections();
        
        if (resultCount === 0) {
            this.showAlert('No results found. Please try different search terms.', 'info');
            return;
        }

        this.showLoading();
        
        try {
            const response = await fetch('/get_results');
            const data = await response.json();
            
            if (data.success) {
                this.displayResults(data.results);
                this.showSection('resultsSection');
                document.getElementById('exportBtn').style.display = 'inline-flex';
                this.showAlert(`Found ${data.total_count} results`, 'success');
            } else {
                this.showAlert('Error loading results', 'error');
            }
        } catch (error) {
            this.showAlert('Network error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(results) {
        const tbody = document.getElementById('resultsTableBody');
        const resultCount = document.getElementById('resultCount');
        
        tbody.innerHTML = '';
        resultCount.textContent = `${results.length} results found`;
        
        results.forEach((result, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${this.escapeHtml(result.Application_Number || '')}</td>
                <td>${this.escapeHtml(result.Wordmark || '')}</td>
                <td>${this.escapeHtml(result.Proprietor || '')}</td>
                <td>${this.escapeHtml(result.Class || '')}</td>
                <td>${this.escapeHtml(result.Status || '')}</td>
                <td>
                    <span class="image-indicator ${result.has_image ? 'has-image' : 'no-image'}">
                        ${result.has_image ? '✓ Image' : '✗ No Image'}
                    </span>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    async exportResults() {
        this.showLoading();
        
        try {
            const response = await fetch('/export_excel');
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                
                // Get filename from response headers
                const contentDisposition = response.headers.get('Content-Disposition');
                let filename = 'trademark_search_results.xlsx';
                if (contentDisposition) {
                    const matches = contentDisposition.match(/filename="(.+)"/);
                    if (matches) {
                        filename = matches[1];
                    }
                }
                
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                this.showAlert('Excel file downloaded successfully', 'success');
            } else {
                this.showAlert('Export failed. Please try again.', 'error');
            }
        } catch (error) {
            this.showAlert('Export error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async resetSearch() {
        this.showLoading();
        
        try {
            const response = await fetch('/reset_search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.newSearch();
                this.showAlert('Search reset successfully', 'success');
            } else {
                this.showAlert(data.message, 'error');
            }
        } catch (error) {
            this.showAlert('Reset error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    newSearch() {
        this.stopStatusPolling();
        this.currentStatus = 'idle';
        this.hideAllSections();
        
        // Clear form
        document.getElementById('searchForm').reset();
        document.getElementById('captchaInput').value = '';
        
        // Reset display
        document.getElementById('exportBtn').style.display = 'none';
        document.getElementById('resultsTableBody').innerHTML = '';
        
        this.showAlert('Ready for new search', 'info');
    }

    // Utility methods
    hideAllSections() {
        const sections = ['statusSection', 'captchaSection', 'resultsSection'];
        sections.forEach(id => this.hideSection(id));
    }

    showSection(sectionId) {
        document.getElementById(sectionId).style.display = 'block';
    }

    hideSection(sectionId) {
        document.getElementById(sectionId).style.display = 'none';
    }

    updateStatus(message, progress = null) {
        document.getElementById('statusMessage').textContent = message;
        
        if (progress !== null) {
            const progressBar = document.getElementById('progressBar');
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            
            progressBar.style.display = 'block';
            progressFill.style.width = progress + '%';
            progressText.textContent = Math.round(progress) + '%';
        }
    }

    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alertContainer');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        
        alertContainer.appendChild(alert);
        
        // Remove alert after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alertContainer.removeChild(alert);
            }
        }, 5000);
    }

    stopStatusPolling() {
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
            this.statusCheckInterval = null;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new TrademarkSearchApp();
});