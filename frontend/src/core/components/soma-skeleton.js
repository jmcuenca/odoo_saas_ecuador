/**
 * SomaTech Shared Components - Skeleton
 * @element soma-skeleton
 *
 * @prop {String} variant - 'text' | 'circle' | 'rect'
 * @prop {String} width - CSS width
 * @prop {String} height - CSS height
 */
import { LitElement, html, css } from 'lit';

export class SomaSkeleton extends LitElement {
    static properties = {
        variant: { type: String },
        width: { type: String },
        height: { type: String },
    };

    static styles = css`
    :host {
      display: block;
    }

    .skeleton {
      background: linear-gradient(90deg,
        rgba(255, 255, 255, 0.03) 25%,
        rgba(255, 255, 255, 0.08) 50%,
        rgba(255, 255, 255, 0.03) 75%
      );
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
    }

    .text {
      height: 1rem;
      border-radius: var(--radius-sm, 0.25rem);
    }

    .circle {
      border-radius: 50%;
    }

    .rect {
      border-radius: var(--radius-md, 0.5rem);
    }

    @keyframes shimmer {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }
  `;

    constructor() {
        super();
        this.variant = 'text';
        this.width = '100%';
        this.height = '';
    }

    render() {
        const style = `
      width: ${this.width};
      height: ${this.height || (this.variant === 'text' ? '1rem' : this.width)};
    `;

        return html`
      <div class="skeleton ${this.variant}" style="${style}"></div>
    `;
    }
}

customElements.define('soma-skeleton', SomaSkeleton);
