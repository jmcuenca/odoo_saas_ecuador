/**
 * SomaTech Catalog - Product Grid
 * @element product-grid
 */
import { LitElement, html, css } from 'lit';
import { productsService } from '../../core/services/products.service.js';

export class ProductGrid extends LitElement {
    static properties = {
        products: { type: Array, state: true },
        loading: { type: Boolean, state: true },
        error: { type: String, state: true },
    };

    static styles = css`
    :host {
      display: block;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: var(--space-6);
    }

    /* Skeleton Grid */
    .skeleton-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: var(--space-6);
    }

    .skeleton-card {
      height: 380px;
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-xl);
      overflow: hidden;
    }

    .skeleton-image {
      height: 200px;
      background: linear-gradient(90deg,
        rgba(255, 255, 255, 0.03) 25%,
        rgba(255, 255, 255, 0.08) 50%,
        rgba(255, 255, 255, 0.03) 75%
      );
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
    }

    .skeleton-content {
      padding: var(--space-5);
    }

    .skeleton-line {
      height: 1rem;
      margin-bottom: var(--space-3);
      background: linear-gradient(90deg,
        rgba(255, 255, 255, 0.03) 25%,
        rgba(255, 255, 255, 0.08) 50%,
        rgba(255, 255, 255, 0.03) 75%
      );
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
      border-radius: var(--radius-sm);
    }

    .skeleton-line.short { width: 60%; }
    .skeleton-line.btn { height: 2.5rem; margin-top: var(--space-4); }

    @keyframes shimmer {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }

    /* Error State */
    .error {
      text-align: center;
      padding: var(--space-10);
      background: rgba(244, 67, 54, 0.1);
      border: 1px solid rgba(244, 67, 54, 0.3);
      border-radius: var(--radius-xl);
    }

    .error h3 {
      color: var(--color-danger);
      margin-bottom: var(--space-2);
    }

    .error p {
      color: var(--color-text-secondary);
    }

    /* Empty State */
    .empty {
      text-align: center;
      padding: var(--space-12);
      color: var(--color-text-muted);
    }

    .empty .icon {
      font-size: 4rem;
      margin-bottom: var(--space-4);
      opacity: 0.5;
    }
  `;

    constructor() {
        super();
        this.products = [];
        this.loading = true;
        this.error = null;
    }

    connectedCallback() {
        super.connectedCallback();
        this._loadProducts();
    }

    async _loadProducts() {
        this.loading = true;
        this.error = null;

        try {
            this.products = await productsService.getAll();
        } catch (err) {
            this.error = err.message || 'Error al cargar productos';
            console.error('Product load error:', err);
        } finally {
            this.loading = false;
        }
    }

    _renderSkeletons() {
        return html`
      <div class="skeleton-grid">
        ${Array(6).fill(0).map(() => html`
          <div class="skeleton-card">
            <div class="skeleton-image"></div>
            <div class="skeleton-content">
              <div class="skeleton-line"></div>
              <div class="skeleton-line short"></div>
              <div class="skeleton-line btn"></div>
            </div>
          </div>
        `)}
      </div>
    `;
    }

    render() {
        if (this.loading) {
            return this._renderSkeletons();
        }

        if (this.error) {
            return html`
        <div class="error">
          <h3>⚠️ Error</h3>
          <p>${this.error}</p>
          <p>Verifica que el servidor Django esté corriendo en el puerto 24502.</p>
        </div>
      `;
        }

        if (this.products.length === 0) {
            return html`
        <div class="empty">
          <div class="icon">📦</div>
          <h3>No hay productos</h3>
          <p>Pronto agregaremos más productos al catálogo.</p>
        </div>
      `;
        }

        return html`
      <div class="grid">
        ${this.products.map(product => html`
          <product-card .product=${product}></product-card>
        `)}
      </div>
    `;
    }
}

customElements.define('product-grid', ProductGrid);
