/**
 * SomaTech Catalog - Product Card
 * @element product-card
 */
import { LitElement, html, css } from 'lit';
import { CartController } from '../../core/controllers/cart.controller.js';
import { formatCurrency } from '../../utils/format.js';

export class ProductCard extends LitElement {
    static properties = {
        product: { type: Object },
        adding: { type: Boolean, state: true },
    };

    cart = new CartController(this);

    static styles = css`
    :host {
      display: block;
    }

    .card {
      height: 100%;
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-xl);
      overflow: hidden;
      transition: all var(--transition-base);
      display: flex;
      flex-direction: column;
    }

    .card:hover {
      transform: translateY(-8px);
      border-color: rgba(255, 179, 0, 0.3);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .image-container {
      position: relative;
      height: 200px;
      background: var(--gradient-card);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    .image-container img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      transition: transform var(--transition-base);
    }

    .card:hover .image-container img {
      transform: scale(1.05);
    }

    .placeholder-icon {
      font-size: 4rem;
      opacity: 0.3;
    }

    .badge {
      position: absolute;
      top: var(--space-3);
      left: var(--space-3);
      padding: var(--space-1) var(--space-3);
      background: var(--color-success);
      border-radius: var(--radius-full);
      font-size: var(--font-size-xs);
      font-weight: var(--font-weight-semibold);
      color: white;
    }

    .badge.out-of-stock {
      background: var(--color-danger);
    }

    .content {
      padding: var(--space-5);
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .name {
      font-size: var(--font-size-base);
      font-weight: var(--font-weight-semibold);
      margin-bottom: var(--space-2);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .sku {
      font-size: var(--font-size-xs);
      color: var(--color-text-muted);
      margin-bottom: var(--space-3);
    }

    .price-row {
      margin-top: auto;
      padding-top: var(--space-4);
    }

    .price {
      font-size: var(--font-size-2xl);
      font-weight: var(--font-weight-bold);
      color: var(--color-secondary);
    }

    .tax-note {
      font-size: var(--font-size-xs);
      color: var(--color-text-muted);
      margin-top: var(--space-1);
    }

    .add-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      width: 100%;
      margin-top: var(--space-4);
      padding: var(--space-3) var(--space-4);
      background: var(--gradient-primary);
      border: none;
      border-radius: var(--radius-md);
      color: white;
      font-family: inherit;
      font-size: var(--font-size-sm);
      font-weight: var(--font-weight-medium);
      cursor: pointer;
      transition: all var(--transition-base);
    }

    .add-btn:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: var(--shadow-glow-primary);
    }

    .add-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .add-btn.success {
      background: linear-gradient(135deg, var(--color-success), #66bb6a);
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.6; }
    }

    .adding {
      animation: pulse 1s infinite;
    }
  `;

    constructor() {
        super();
        this.product = {};
        this.adding = false;
    }

    async _addToCart() {
        this.adding = true;
        const success = await this.cart.addItem(this.product.id, 1);
        this.adding = false;

        if (success) {
            const btn = this.shadowRoot.querySelector('.add-btn');
            btn.classList.add('success');
            btn.textContent = '✓ Agregado';
            setTimeout(() => {
                btn.classList.remove('success');
                this.requestUpdate();
            }, 2000);
        }
    }

    render() {
        const { name, default_code, list_price, image_url, qty_available } = this.product;
        const inStock = qty_available === undefined || qty_available > 0;

        return html`
      <article class="card">
        <div class="image-container">
          ${image_url ? html`
            <img src="${image_url}" alt="${name}" loading="lazy">
          ` : html`
            <span class="placeholder-icon">📦</span>
          `}
          ${inStock ? html`
            <span class="badge">En Stock</span>
          ` : html`
            <span class="badge out-of-stock">Agotado</span>
          `}
        </div>

        <div class="content">
          <h3 class="name">${name || 'Producto'}</h3>
          ${default_code ? html`<p class="sku">SKU: ${default_code}</p>` : ''}

          <div class="price-row">
            <span class="price">${formatCurrency(list_price)}</span>
            <p class="tax-note">IVA 15% incluido</p>
          </div>

          <button
            class="add-btn ${this.adding ? 'adding' : ''}"
            ?disabled=${this.adding || !inStock}
            @click=${this._addToCart}
          >
            ${this.adding ? '⏳ Agregando...' : '🛒 Agregar al Carrito'}
          </button>
        </div>
      </article>
    `;
    }
}

customElements.define('product-card', ProductCard);
