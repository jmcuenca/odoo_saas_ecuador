/**
 * SomaTech Shared Components - Button
 * @element soma-button
 *
 * @prop {String} variant - 'primary' | 'secondary' | 'ghost' | 'danger'
 * @prop {String} size - 'sm' | 'md' | 'lg'
 * @prop {Boolean} disabled - Disable button
 * @prop {Boolean} loading - Show spinner
 * @prop {Boolean} fullWidth - 100% width
 */
import { LitElement, html, css } from 'lit';

export class SomaButton extends LitElement {
  static properties = {
    variant: { type: String, reflect: true },
    size: { type: String, reflect: true },
    disabled: { type: Boolean, reflect: true },
    loading: { type: Boolean, reflect: true },
    fullWidth: { type: Boolean, attribute: 'full-width' },
    type: { type: String },
  };

  static styles = css`
    :host {
      display: inline-block;
    }

    :host([full-width]) {
      display: block;
      width: 100%;
    }

    button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2, 0.5rem);
      width: 100%;
      border: none;
      border-radius: var(--radius-md, 0.5rem);
      font-family: inherit;
      font-weight: var(--font-weight-medium, 500);
      cursor: pointer;
      transition: all var(--transition-base, 250ms ease);
      position: relative;
      overflow: hidden;
    }

    /* Sizes */
    button.sm {
      padding: var(--space-2, 0.5rem) var(--space-4, 1rem);
      font-size: var(--font-size-sm, 0.875rem);
    }

    button.md {
      padding: var(--space-3, 0.75rem) var(--space-6, 1.5rem);
      font-size: var(--font-size-base, 1rem);
    }

    button.lg {
      padding: var(--space-4, 1rem) var(--space-8, 2rem);
      font-size: var(--font-size-lg, 1.125rem);
    }

    /* Primary Variant */
    button.primary {
      background: var(--gradient-primary, linear-gradient(135deg, #1a237e, #303f9f));
      color: white;
    }

    button.primary:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 10px 30px rgba(26, 35, 126, 0.4);
    }

    button.primary:active:not(:disabled) {
      transform: translateY(0);
    }

    /* Secondary Variant */
    button.secondary {
      background: var(--gradient-secondary, linear-gradient(135deg, #ffb300, #ffc107));
      color: var(--color-bg-primary, #0f0f23);
    }

    button.secondary:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 10px 30px rgba(255, 179, 0, 0.4);
    }

    /* Ghost Variant */
    button.ghost {
      background: transparent;
      color: var(--color-text-primary, white);
      border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
    }

    button.ghost:hover:not(:disabled) {
      background: var(--glass-bg, rgba(255, 255, 255, 0.05));
      border-color: var(--color-border-hover, rgba(255, 255, 255, 0.2));
    }

    /* Danger Variant */
    button.danger {
      background: linear-gradient(135deg, #f44336, #e53935);
      color: white;
    }

    button.danger:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 10px 30px rgba(244, 67, 54, 0.4);
    }

    /* Disabled State */
    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    /* Loading State */
    button.loading {
      color: transparent;
    }

    .spinner {
      position: absolute;
      width: 1.25em;
      height: 1.25em;
      border: 2px solid currentColor;
      border-right-color: transparent;
      border-radius: 50%;
      animation: spin 0.75s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* Slotted icon sizing */
    ::slotted(svg),
    ::slotted(img) {
      width: 1.25em;
      height: 1.25em;
    }
  `;

  constructor() {
    super();
    this.variant = 'primary';
    this.size = 'md';
    this.disabled = false;
    this.loading = false;
    this.fullWidth = false;
    this.type = 'button';
  }

  render() {
    const classes = `${this.variant} ${this.size} ${this.loading ? 'loading' : ''}`;

    return html`
      <button
        type="${this.type}"
        class="${classes}"
        ?disabled="${this.disabled || this.loading}"
        part="button"
      >
        ${this.loading ? html`<span class="spinner"></span>` : ''}
        <slot></slot>
      </button>
    `;
  }
}

customElements.define('soma-button', SomaButton);
