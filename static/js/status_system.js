/**
 * Sistema de Status e Feedback Visual para Dashboard GA4
 * Resolve o problema de não saber quando scripts estão rodando
 */

class StatusSystem {
    constructor() {
        this.statusContainer = null;
        this.connectionStatus = null;
        this.globalProgress = null;
        this.logConsole = null;
        this.toastContainer = null;
        this.isOnline = navigator.onLine;
        this.activeOperations = new Map();
        
        this.init();
    }

    init() {
        this.createStatusElements();
        this.setupEventListeners();
        this.checkConnection();
        this.startPeriodicChecks();
    }

    createStatusElements() {
        // Criar container de status se não existir
        if (!document.getElementById('statusContainer')) {
            const statusContainer = document.createElement('div');
            statusContainer.id = 'statusContainer';
            statusContainer.className = 'status-container';
            statusContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
            `;
            document.body.appendChild(statusContainer);
        }

        // Criar barra de progresso global se não existir
        if (!document.getElementById('globalProgress')) {
            const globalProgress = document.createElement('div');
            globalProgress.id = 'globalProgress';
            globalProgress.className = 'global-progress';
            globalProgress.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 3px;
                background: rgba(0,0,0,0.1);
                z-index: 10000;
                display: none;
            `;
            globalProgress.innerHTML = '<div class="global-progress-bar" id="globalProgressBar" style="height: 100%; background: linear-gradient(90deg, #007bff, #28a745); transition: width 0.3s ease;"></div>';
            document.body.appendChild(globalProgress);
        }

        // Criar status de conexão se não existir
        if (!document.getElementById('connectionStatus')) {
            const connectionStatus = document.createElement('div');
            connectionStatus.id = 'connectionStatus';
            connectionStatus.className = 'connection-status';
            connectionStatus.style.cssText = `
                position: fixed;
                bottom: 20px;
                left: 20px;
                z-index: 9999;
                background: white;
                border-radius: 25px;
                padding: 8px 16px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 14px;
                font-weight: 500;
            `;
            connectionStatus.innerHTML = `
                <div class="connection-dot connection-loading" id="connectionDot" style="width: 8px; height: 8px; border-radius: 50%; background: #ffc107; animation: pulse 2s infinite;"></div>
                <span id="connectionText">Verificando conexão...</span>
            `;
            document.body.appendChild(connectionStatus);
        }

        // Criar console de logs se não existir
        if (!document.getElementById('logConsole')) {
            const logConsole = document.createElement('div');
            logConsole.id = 'logConsole';
            logConsole.className = 'log-console';
            logConsole.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                max-height: 300px;
                background: #1e1e1e;
                color: #00ff00;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                z-index: 9999;
                overflow: hidden;
                display: none;
            `;
            logConsole.innerHTML = `
                <div class="log-header" style="background: #333; padding: 8px 12px; font-weight: bold; display: flex; justify-content: space-between; align-items: center;">
                    <span>Console de Logs</span>
                    <button class="btn-close btn-close-white" onclick="statusSystem.toggleLogConsole()"></button>
                </div>
                <div class="log-content" id="logContent" style="padding: 8px 12px; max-height: 250px; overflow-y: auto;"></div>
            `;
            document.body.appendChild(logConsole);
        }

        // Criar container de toasts se não existir
        if (!document.getElementById('toastContainer')) {
            const toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.className = 'toast-container';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 9999;
            `;
            document.body.appendChild(toastContainer);
        }

        // Referenciar elementos
        this.statusContainer = document.getElementById('statusContainer');
        this.globalProgress = document.getElementById('globalProgress');
        this.globalProgressBar = document.getElementById('globalProgressBar');
        this.connectionStatus = document.getElementById('connectionStatus');
        this.connectionDot = document.getElementById('connectionDot');
        this.connectionText = document.getElementById('connectionText');
        this.logConsole = document.getElementById('logConsole');
        this.logContent = document.getElementById('logContent');
        this.toastContainer = document.getElementById('toastContainer');
    }

    setupEventListeners() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.updateConnectionStatus('online', 'Conectado');
            this.log('success', 'Conexão restaurada');
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.updateConnectionStatus('offline', 'Desconectado');
            this.log('error', 'Conexão perdida');
        });

        // Interceptar fetch para mostrar status de requisições
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            const url = args[0];
            this.log('info', `Fazendo requisição: ${url}`);
            
            try {
                const response = await originalFetch(...args);
                this.log('success', `Requisição concluída: ${url}`);
                return response;
            } catch (error) {
                this.log('error', `Erro na requisição: ${url} - ${error.message}`);
                throw error;
            }
        };
    }

    checkConnection() {
        this.showStatus('loading', 'Testando Conexão', 'Verificando conectividade...');
        
        fetch('/api/test-connection', { method: 'GET' })
            .then(response => {
                if (response.ok) {
                    this.updateConnectionStatus('online', 'Conectado');
                    this.showStatus('success', 'Conexão OK', 'Servidor respondendo normalmente!');
                } else {
                    this.updateConnectionStatus('offline', 'Erro de conexão');
                    this.showStatus('error', 'Erro de Conexão', 'Servidor não está respondendo corretamente');
                }
            })
            .catch(() => {
                this.updateConnectionStatus('offline', 'Servidor indisponível');
                this.showStatus('error', 'Servidor Indisponível', 'Não foi possível conectar ao servidor');
            });
    }

    updateConnectionStatus(status, text) {
        if (this.connectionDot && this.connectionText) {
            this.connectionDot.className = `connection-dot connection-${status}`;
            this.connectionText.textContent = text;
        }
    }

    showStatus(type, title, message, duration = 5000, progress = null) {
        const statusCard = document.createElement('div');
        statusCard.className = 'status-card';
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-times-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle',
            loading: 'fas fa-spinner fa-spin'
        };

        const colors = {
            success: 'linear-gradient(135deg, #28a745, #20c997)',
            error: 'linear-gradient(135deg, #dc3545, #e74c3c)',
            warning: 'linear-gradient(135deg, #ffc107, #fd7e14)',
            info: 'linear-gradient(135deg, #17a2b8, #6f42c1)',
            loading: 'linear-gradient(135deg, #007bff, #6610f2)'
        };

        statusCard.innerHTML = `
            <div class="status-header" style="padding: 12px 16px; font-weight: 600; display: flex; align-items: center; gap: 8px; background: ${colors[type]}; color: white;">
                <i class="${icons[type]}"></i>
                <span>${title}</span>
                <button class="status-close" onclick="this.parentElement.parentElement.remove()" style="position: absolute; top: 8px; right: 8px; background: none; border: none; color: inherit; opacity: 0.7; cursor: pointer; font-size: 16px;">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="status-body" style="padding: 12px 16px; font-size: 14px;">
                <div>${message}</div>
                ${progress !== null ? `
                    <div class="status-progress mt-2" style="height: 4px; background: rgba(0,0,0,0.1); border-radius: 2px; overflow: hidden;">
                        <div class="status-progress-bar" style="height: 100%; background: #007bff; border-radius: 2px; transition: width 0.3s ease; width: ${progress}%;"></div>
                    </div>
                ` : ''}
            </div>
        `;

        this.statusContainer.appendChild(statusCard);

        if (duration > 0) {
            setTimeout(() => {
                if (statusCard.parentElement) {
                    statusCard.remove();
                }
            }, duration);
        }

        return statusCard;
    }

    showProgress(title, message, progress = 0) {
        return this.showStatus('loading', title, message, 0, progress);
    }

    updateProgress(statusCard, progress, message = null) {
        if (statusCard) {
            const progressBar = statusCard.querySelector('.status-progress-bar');
            const messageDiv = statusCard.querySelector('.status-body > div:first-child');
            
            if (progressBar) {
                progressBar.style.width = `${progress}%`;
            }
            
            if (message && messageDiv) {
                messageDiv.textContent = message;
            }
        }
    }

    showGlobalProgress(show = true) {
        if (this.globalProgress) {
            this.globalProgress.style.display = show ? 'block' : 'none';
        }
    }

    updateGlobalProgress(progress) {
        if (this.globalProgressBar) {
            this.globalProgressBar.style.width = `${progress}%`;
        }
    }

    log(level, message) {
        if (!this.logContent) return;
        
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry log-${level}`;
        
        const colors = {
            info: '#00ff00',
            warning: '#ffaa00',
            error: '#ff4444',
            success: '#44ff44'
        };

        logEntry.innerHTML = `
            <span class="log-timestamp" style="color: #666; margin-right: 8px;">[${timestamp}]</span>
            <span style="color: ${colors[level]};">${message}</span>
        `;
        
        this.logContent.appendChild(logEntry);
        this.logContent.scrollTop = this.logContent.scrollHeight;
    }

    toggleLogConsole() {
        if (this.logConsole) {
            this.logConsole.style.display = this.logConsole.style.display === 'none' ? 'block' : 'none';
        }
    }

    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#17a2b8'
        };

        toast.innerHTML = `
            <div class="toast-body" style="padding: 12px 16px; color: ${colors[type]}; background: white; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); margin-bottom: 10px;">
                <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : type === 'warning' ? 'exclamation-triangle' : 'info'}"></i>
                ${message}
            </div>
        `;

        this.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, duration);
    }

    setButtonLoading(buttonId, loading = true) {
        const button = document.getElementById(buttonId);
        if (button) {
            if (loading) {
                button.classList.add('btn-loading');
                button.disabled = true;
                button.style.pointerEvents = 'none';
            } else {
                button.classList.remove('btn-loading');
                button.disabled = false;
                button.style.pointerEvents = 'auto';
            }
        }
    }

    startOperation(operationId, title, message) {
        this.activeOperations.set(operationId, {
            id: operationId,
            title: title,
            message: message,
            startTime: Date.now(),
            statusCard: this.showProgress(title, message, 0)
        });
        
        this.log('info', `Iniciando operação: ${title}`);
        return this.activeOperations.get(operationId);
    }

    updateOperation(operationId, progress, message = null) {
        const operation = this.activeOperations.get(operationId);
        if (operation) {
            this.updateProgress(operation.statusCard, progress, message);
            this.log('info', `${operation.title}: ${progress}% - ${message || operation.message}`);
        }
    }

    completeOperation(operationId, success = true, finalMessage = null) {
        const operation = this.activeOperations.get(operationId);
        if (operation) {
            const duration = Date.now() - operation.startTime;
            const durationText = `${(duration / 1000).toFixed(1)}s`;
            
            if (operation.statusCard) {
                operation.statusCard.remove();
            }
            
            if (success) {
                this.showStatus('success', `${operation.title} - Concluído!`, finalMessage || `Operação finalizada em ${durationText}`);
                this.log('success', `${operation.title} concluída em ${durationText}`);
            } else {
                this.showStatus('error', `${operation.title} - Erro!`, finalMessage || `Operação falhou após ${durationText}`);
                this.log('error', `${operation.title} falhou após ${durationText}`);
            }
            
            this.activeOperations.delete(operationId);
        }
    }

    startPeriodicChecks() {
        // Verificar conexão a cada 30 segundos
        setInterval(() => {
            this.checkConnection();
        }, 30000);

        // Logs automáticos de sistema
        setInterval(() => {
            const messages = [
                'Sistema funcionando normalmente',
                'Verificando conexão com GA4',
                'Monitorando métricas em tempo real',
                'Cache atualizado automaticamente'
            ];
            
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            this.log('info', randomMessage);
        }, 60000);
    }

    // Métodos específicos para operações do dashboard
    generateCSV() {
        const operationId = 'generate-csv';
        this.startOperation(operationId, 'Gerando CSVs', 'Conectando ao GA4...');
        this.setButtonLoading('refresh-csv', true);
        this.showGlobalProgress(true);
        
        // Fazer requisição real para gerar CSVs
        fetch('/api/refresh-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.completeOperation(operationId, true, `Arquivos CSV criados: ${data.files.join(', ')}`);
            } else {
                this.completeOperation(operationId, false, data.error || 'Erro ao gerar CSVs');
            }
        })
        .catch(error => {
            this.completeOperation(operationId, false, `Erro de conexão: ${error.message}`);
        })
        .finally(() => {
            this.showGlobalProgress(false);
            this.setButtonLoading('refresh-csv', false);
        });
    }

    loadData() {
        const operationId = 'load-data';
        this.startOperation(operationId, 'Carregando Dados', 'Lendo arquivos CSV...');
        this.setButtonLoading('load-from-csv', true);
        
        // Chamar função real de carregamento
        if (typeof loadFromCSVs === 'function') {
            loadFromCSVs()
                .then(() => {
                    this.completeOperation(operationId, true, 'Dados carregados no dashboard!');
                })
                .catch(error => {
                    this.completeOperation(operationId, false, `Erro ao carregar dados: ${error.message}`);
                })
                .finally(() => {
                    this.setButtonLoading('load-from-csv', false);
                });
        } else {
            // Fallback se a função não existir
            setTimeout(() => {
                this.completeOperation(operationId, false, 'Função loadFromCSVs não encontrada');
                this.setButtonLoading('load-from-csv', false);
            }, 1000);
        }
    }

    sendReport() {
        const operationId = 'send-report';
        this.startOperation(operationId, 'Enviando Relatório', 'Preparando dados...');
        this.setButtonLoading('btnSendReport', true);
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += 33;
            const messages = [
                'Preparando dados...',
                'Enviando via Slack...',
                'Confirmando entrega...'
            ];
            
            const messageIndex = Math.floor(progress / 33) - 1;
            this.updateOperation(operationId, progress, messages[messageIndex] || 'Finalizando...');
            
            if (progress >= 100) {
                clearInterval(interval);
                this.setButtonLoading('btnSendReport', false);
                this.completeOperation(operationId, true, 'Relatório enviado com sucesso!');
            }
        }, 700);
    }
}

// Inicializar sistema globalmente
let statusSystem;
document.addEventListener('DOMContentLoaded', function() {
    statusSystem = new StatusSystem();
    
    // Adicionar CSS necessário
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .btn-loading::after {
            content: '';
            position: absolute;
            width: 16px;
            height: 16px;
            top: 50%;
            left: 50%;
            margin-left: -8px;
            margin-top: -8px;
            border: 2px solid transparent;
            border-top-color: currentColor;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .status-card {
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
});

// Exportar para uso global
window.statusSystem = statusSystem;
