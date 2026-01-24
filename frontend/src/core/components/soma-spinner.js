/**
 * SomaTech Shared Components - Spinner
 * @element soma-spinner
 *
 * @prop {String} size - 'sm' | 'md' | 'lg'
 * @prop {String} color - CSS color value
 */
import { LitElement, html, css } from 'lit';

export class SomaSpinner extends LitElement {
    static properties = {
        size: { type: String },
        color: { type: String },
    };

    static styles = css`
    :host {
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    .spinner {
      border-radius: 50%;
      border-style: solid;
      border-color: currentColor;
      border-right-color: transparent;
      animation: spin 0.75s linear infinite;
    }

    .sm {
      width: 16px;
      height: 16px;
      border-width: 2px;
    }

    .md {
      width: 24px;
      height: 24px;
      border-width: 3px;
    }

    .lg {
      width: 40px;
      height: 40px;
      border-width: 4px;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  `;

    constructor() {
        super();
        this.size = 'md';
        this.color = 'var(--color-secondary, #ffb300)';
    }

    render() {
        return html`
      <span
        class="spinner ${this.size}"
        style="color: ${this.color}"
        role="status"
        aria-label="Loading"
      ></span>
    `;
    }
}

customElements.define('soma-spinner', SomaSpinner);
