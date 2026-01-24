/**
 * SomaTech Shared Components - Toast Notifications
 * @element soma-toast
 *
 * Usage: SomaToast.show('Mensaje', 'success')
 */
import { LitElement, html, css } from 'lit';

export class SomaToast extends LitElement {
    static properties = {
        _toasts: { type: Array, state: true },
    };

    static styles = css`
    :host {
      position: fixed;
      top: var(--space-4, 1rem);
      right: var(--space-4, 1rem);
      z-index: var(--z-toast, 600);
      display: flex;
      flex-direction: column;
      gap: var(--space-3, 0.75rem);
      pointer-events: none;
    }

    .toast {
      display: flex;
      align-items: center;
      gap: var(--space-3, 0.75rem);
      padding: var(--space-4, 1rem) var(--space-5, 1.25rem);
      background: var(--color-bg-secondary, #1a1a2e);
      border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
      border-radius: var(--radius-lg, 0.75rem);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
      color: var(--color-text-primary, white);
      font-size: var(--font-size-sm, 0.875rem);
      pointer-events: auto;
      animation: slideIn 0.3s ease forwards;
      max-width: 380px;
    }

    .toast.exiting {
      animation: slideOut 0.3s ease forwards;
    }

    .toast.success {
      border-left: 4px solid var(--color-success, #4caf50);
    }

    .toast.error {
      border-left: 4px solid var(--color-danger, #f44336);
    }

    .toast.warning {
      border-left: 4px solid var(--color-warning, #ff9800);
    }

    .toast.info {
      border-left: 4px solid var(--color-info, #2196f3);
    }

    .icon {
      font-size: 1.25rem;
      flex-shrink: 0;
    }

    .message {
      flex: 1;
    }

    .close-btn {
      padding: var(--space-1, 0.25rem);
      background: none;
      border: none;
      color: var(--color-text-muted, rgba(255, 255, 255, 0.5));
      cursor: pointer;
      opacity: 0.7;
      transition: opacity var(--transition-fast, 150ms ease);
    }

    .close-btn:hover {
      opacity: 1;
    }

    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateX(100%);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes slideOut {
      from {
        opacity: 1;
        transform: translateX(0);
      }
      to {
        opacity: 0;
        transform: translateX(100%);
      }
    }
  `;

    static _instance = null;

    static get instance() {
        if (!SomaToast._instance) {
            SomaToast._instance = document.createElement('soma-toast');
            document.body.appendChild(SomaToast._instance);
        }
        return SomaToast._instance;
    }

    static show(message, type = 'info', duration = 4000) {
        SomaToast.instance._addToast(message, type, duration);
    }

    static success(message) { SomaToast.show(message, 'success'); }
    static error(message) { SomaToast.show(message, 'error'); }
    static warning(message) { SomaToast.show(message, 'warning'); }
    static info(message) { SomaToast.show(message, 'info'); }

    constructor() {
        super();
        this._toasts = [];
    }

    _addToast(message, type, duration) {
        const id = Date.now();
        this._toasts = [...this._toasts, { id, message, type, exiting: false }];

        if (duration > 0) {
            setTimeout(() => this._removeToast(id), duration);
        }
    }

    _removeToast(id) {
        const toast = this._toasts.find(t => t.id === id);
        if (toast) {
            toast.exiting = true;
            this.requestUpdate();
            setTimeout(() => {
                this._toasts = this._toasts.filter(t => t.id !== id);
            }, 300);
        }
    }

    _getIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ',
        };
        return icons[type] || icons.info;
    }

    render() {
        return html`
      ${this._toasts.map(toast => html`
        <div class="toast ${toast.type} ${toast.exiting ? 'exiting' : ''}">
          <span class="icon">${this._getIcon(toast.type)}</span>
          <span class="message">${toast.message}</span>
          <button class="close-btn" @click="${() => this._removeToast(toast.id)}">✕</button>
        </div>
      `)}
    `;
    }
}

customElements.define('soma-toast', SomaToast);
