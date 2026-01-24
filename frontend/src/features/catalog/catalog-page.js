/**
 * SomaTech Catalog - Page
 * @element catalog-page
 */
import { LitElement, html, css } from 'lit';

export class CatalogPage extends LitElement {
    static styles = css`
    :host {
      display: block;
    }

    .hero {
      text-align: center;
      padding: var(--space-12) var(--space-6);
      background: var(--gradient-card);
      border-radius: var(--radius-2xl);
      margin-bottom: var(--space-10);
      border: 1px solid var(--glass-border);
    }

    .hero h1 {
      font-size: var(--font-size-4xl);
      font-weight: var(--font-weight-bold);
      margin-bottom: var(--space-4);
      background: linear-gradient(135deg, #ffffff 0%, var(--color-secondary) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .hero p {
      font-size: var(--font-size-lg);
      color: var(--color-text-secondary);
      max-width: 600px;
      margin: 0 auto;
    }

    .section-title {
      font-size: var(--font-size-2xl);
      font-weight: var(--font-weight-semibold);
      margin-bottom: var(--space-6);
      display: flex;
      align-items: center;
      gap: var(--space-3);
    }

    .section-title::before {
      content: '';
      width: 4px;
      height: 28px;
      background: linear-gradient(180deg, var(--color-secondary), var(--color-primary));
      border-radius: 2px;
    }

    @media (max-width: 640px) {
      .hero { padding: var(--space-8) var(--space-4); }
      .hero h1 { font-size: var(--font-size-3xl); }
    }
  `;

    render() {
        return html`
      <section class="hero">
        <h1>SomaTech Ecuador</h1>
        <p>Tecnología premium con facturación electrónica SRI. Compra seguro con garantía local y envío a todo el país.</p>
      </section>

      <h2 class="section-title">Nuestros Productos</h2>
      <product-grid></product-grid>
    `;
    }
}

customElements.define('catalog-page', CatalogPage);
