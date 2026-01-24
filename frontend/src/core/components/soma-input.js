/**
 * SomaTech Shared Components - Input
 * @element soma-input
 *
 * @prop {String} type - 'text' | 'email' | 'password' | 'number' | 'tel'
 * @prop {String} label - Input label
 * @prop {String} placeholder - Placeholder text
 * @prop {String} value - Current value
 * @prop {String} error - Error message
 * @prop {Boolean} required - Required field
 * @prop {Boolean} disabled - Disabled state
 */
import { LitElement, html, css } from 'lit';

export class SomaInput extends LitElement {
    static properties = {
        type: { type: String },
        label: { type: String },
        placeholder: { type: String },
        value: { type: String },
        error: { type: String },
        required: { type: Boolean },
        disabled: { type: Boolean },
        name: { type: String },
    };

    static styles = css`
    :host {
      display: block;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: var(--space-2, 0.5rem);
    }

    label {
      font-size: var(--font-size-sm, 0.875rem);
      font-weight: var(--font-weight-medium, 500);
      color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
    }

    label .required {
      color: var(--color-danger, #f44336);
      margin-left: 2px;
    }

    .input-wrapper {
      position: relative;
    }

    input {
      width: 100%;
      padding: var(--space-3, 0.75rem) var(--space-4, 1rem);
      background: var(--glass-bg, rgba(255, 255, 255, 0.05));
      border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
      border-radius: var(--radius-md, 0.5rem);
      font-family: inherit;
      font-size: var(--font-size-base, 1rem);
      color: var(--color-text-primary, white);
      transition: all var(--transition-fast, 150ms ease);
    }

    input::placeholder {
      color: var(--color-text-muted, rgba(255, 255, 255, 0.5));
    }

    input:hover:not(:disabled) {
      border-color: var(--color-border-hover, rgba(255, 255, 255, 0.2));
    }

    input:focus {
      border-color: var(--color-secondary, #ffb300);
      box-shadow: 0 0 0 3px rgba(255, 179, 0, 0.15);
    }

    input:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    /* Error state */
    :host([error]) input {
      border-color: var(--color-danger, #f44336);
    }

    :host([error]) input:focus {
      box-shadow: 0 0 0 3px rgba(244, 67, 54, 0.15);
    }

    .error-message {
      font-size: var(--font-size-sm, 0.875rem);
      color: var(--color-danger, #f44336);
      display: flex;
      align-items: center;
      gap: var(--space-1, 0.25rem);
    }

    /* Icons slot */
    ::slotted([slot="prefix"]),
    ::slotted([slot="suffix"]) {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      color: var(--color-text-muted, rgba(255, 255, 255, 0.5));
    }

    ::slotted([slot="prefix"]) {
      left: var(--space-3, 0.75rem);
    }

    ::slotted([slot="suffix"]) {
      right: var(--space-3, 0.75rem);
    }
  `;

    constructor() {
        super();
        this.type = 'text';
        this.label = '';
        this.placeholder = '';
        this.value = '';
        this.error = '';
        this.required = false;
        this.disabled = false;
        this.name = '';
    }

    _handleInput(e) {
        this.value = e.target.value;
        this.dispatchEvent(new CustomEvent('input', {
            detail: { value: this.value },
            bubbles: true,
            composed: true,
        }));
    }

    _handleChange(e) {
        this.dispatchEvent(new CustomEvent('change', {
            detail: { value: e.target.value },
            bubbles: true,
            composed: true,
        }));
    }

    render() {
        return html`
      <div class="field">
        ${this.label ? html`
          <label for="input">
            ${this.label}
            ${this.required ? html`<span class="required">*</span>` : ''}
          </label>
        ` : ''}

        <div class="input-wrapper">
          <slot name="prefix"></slot>
          <input
            id="input"
            type="${this.type}"
            name="${this.name}"
            placeholder="${this.placeholder}"
            .value="${this.value}"
            ?required="${this.required}"
            ?disabled="${this.disabled}"
            @input="${this._handleInput}"
            @change="${this._handleChange}"
            part="input"
          />
          <slot name="suffix"></slot>
        </div>

        ${this.error ? html`
          <span class="error-message">⚠️ ${this.error}</span>
        ` : ''}
      </div>
    `;
    }
}

customElements.define('soma-input', SomaInput);
