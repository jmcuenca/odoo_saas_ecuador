/**
 * SomaTech Shared Components - Card
 * @element soma-card
 *
 * @prop {Boolean} hoverable - Add hover lift effect
 * @prop {Boolean} clickable - Add cursor pointer
 * @prop {String} padding - 'none' | 'sm' | 'md' | 'lg'
 */
import { LitElement, html, css } from 'lit';

export class SomaCard extends LitElement {
    static properties = {
        hoverable: { type: Boolean, reflect: true },
        clickable: { type: Boolean, reflect: true },
        padding: { type: String },
    };

    static styles = css`
    :host {
      display: block;
    }

    .card {
      background: var(--glass-bg, rgba(255, 255, 255, 0.05));
      border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
      border-radius: var(--radius-xl, 1rem);
      overflow: hidden;
      transition: all var(--transition-base, 250ms ease);
    }

    /* Padding variants */
    .card.pad-none { padding: 0; }
    .card.pad-sm { padding: var(--space-3, 0.75rem); }
    .card.pad-md { padding: var(--space-6, 1.5rem); }
    .card.pad-lg { padding: var(--space-8, 2rem); }

    /* Hoverable */
    :host([hoverable]) .card:hover {
      transform: translateY(-8px);
      border-color: rgba(255, 179, 0, 0.3);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    /* Clickable */
    :host([clickable]) .card {
      cursor: pointer;
    }

    /* Slots */
    ::slotted([slot="header"]) {
      padding: var(--space-4, 1rem) var(--space-6, 1.5rem);
      border-bottom: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
      font-weight: var(--font-weight-semibold, 600);
    }

    ::slotted([slot="footer"]) {
      padding: var(--space-4, 1rem) var(--space-6, 1.5rem);
      border-top: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
      background: rgba(0, 0, 0, 0.1);
    }

    ::slotted([slot="media"]) {
      width: 100%;
      display: block;
    }
  `;

    constructor() {
        super();
        this.hoverable = false;
        this.clickable = false;
        this.padding = 'none';
    }

    render() {
        return html`
      <div class="card pad-${this.padding}" part="card">
        <slot name="media"></slot>
        <slot name="header"></slot>
        <slot></slot>
        <slot name="footer"></slot>
      </div>
    `;
    }
}

customElements.define('soma-card', SomaCard);
