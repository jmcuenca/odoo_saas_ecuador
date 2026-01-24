/**
 * SomaTech Shared Components - Modal
 * @element soma-modal
 *
 * @prop {Boolean} open - Show/hide modal
 * @prop {String} title - Modal title
 * @prop {String} size - 'sm' | 'md' | 'lg' | 'full'
 * @prop {Boolean} closeOnBackdrop - Close when clicking backdrop
 * @prop {Boolean} closeOnEscape - Close on Escape key
 */
import { LitElement, html, css } from 'lit';

export class SomaModal extends LitElement {
    static properties = {
        open: { type: Boolean, reflect: true },
        title: { type: String },
        size: { type: String },
        closeOnBackdrop: { type: Boolean, attribute: 'close-on-backdrop' },
        closeOnEscape: { type: Boolean, attribute: 'close-on-escape' },
    };

    static styles = css`
    :host {
      display: contents;
    }

    .backdrop {
      position: fixed;
      inset: 0;
      z-index: var(--z-modal-backdrop, 400);
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--space-4, 1rem);
      opacity: 0;
      visibility: hidden;
      transition: all var(--transition-base, 250ms ease);
    }

    :host([open]) .backdrop {
      opacity: 1;
      visibility: visible;
    }

    .modal {
      background: var(--color-bg-secondary, #1a1a2e);
      border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
      border-radius: var(--radius-xl, 1rem);
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
      max-height: 90vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transform: scale(0.95) translateY(20px);
      transition: transform var(--transition-base, 250ms ease);
    }

    :host([open]) .modal {
      transform: scale(1) translateY(0);
    }

    /* Sizes */
    .modal.sm { width: 100%; max-width: 400px; }
    .modal.md { width: 100%; max-width: 560px; }
    .modal.lg { width: 100%; max-width: 800px; }
    .modal.full { width: 100%; max-width: 100%; height: 100%; max-height: 100%; border-radius: 0; }

    .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: var(--space-4, 1rem) var(--space-6, 1.5rem);
      border-bottom: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
    }

    .title {
      font-size: var(--font-size-xl, 1.25rem);
      font-weight: var(--font-weight-semibold, 600);
      color: var(--color-text-primary, white);
      margin: 0;
    }

    .close-btn {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      border: 1px solid transparent;
      border-radius: var(--radius-md, 0.5rem);
      color: var(--color-text-muted, rgba(255, 255, 255, 0.5));
      font-size: 1.25rem;
      cursor: pointer;
      transition: all var(--transition-fast, 150ms ease);
    }

    .close-btn:hover {
      background: var(--glass-bg, rgba(255, 255, 255, 0.05));
      color: var(--color-text-primary, white);
    }

    .body {
      padding: var(--space-6, 1.5rem);
      overflow-y: auto;
      flex: 1;
    }

    .footer {
      padding: var(--space-4, 1rem) var(--space-6, 1.5rem);
      border-top: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
      background: rgba(0, 0, 0, 0.1);
      display: flex;
      justify-content: flex-end;
      gap: var(--space-3, 0.75rem);
    }

    /* Hide scrollbar when not needed */
    .body::-webkit-scrollbar {
      width: 6px;
    }
  `;

    constructor() {
        super();
        this.open = false;
        this.title = '';
        this.size = 'md';
        this.closeOnBackdrop = true;
        this.closeOnEscape = true;
        this._handleKeydown = this._handleKeydown.bind(this);
    }

    connectedCallback() {
        super.connectedCallback();
        document.addEventListener('keydown', this._handleKeydown);
    }

    disconnectedCallback() {
        super.disconnectedCallback();
        document.removeEventListener('keydown', this._handleKeydown);
    }

    _handleKeydown(e) {
        if (this.open && this.closeOnEscape && e.key === 'Escape') {
            this._close();
        }
    }

    _handleBackdropClick(e) {
        if (this.closeOnBackdrop && e.target === e.currentTarget) {
            this._close();
        }
    }

    _close() {
        this.open = false;
        this.dispatchEvent(new CustomEvent('close', { bubbles: true, composed: true }));
    }

    render() {
        return html`
      <div class="backdrop" @click="${this._handleBackdropClick}">
        <div class="modal ${this.size}" role="dialog" aria-modal="true" aria-labelledby="modal-title">
          ${this.title ? html`
            <header class="header">
              <h2 class="title" id="modal-title">${this.title}</h2>
              <button class="close-btn" @click="${this._close}" aria-label="Close">✕</button>
            </header>
          ` : ''}

          <div class="body">
            <slot></slot>
          </div>

          <div class="footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    `;
    }
}

customElements.define('soma-modal', SomaModal);
