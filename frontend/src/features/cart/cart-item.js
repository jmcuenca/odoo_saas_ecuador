/**
 * SomaTech Cart - Cart Item
 * @element cart-item
 */
import { LitElement, html, css } from 'lit';
import { formatCurrency } from '../../utils/format.js';

export class CartItem extends LitElement {
    static properties = {
        item: { type: Object },
    };

    static styles = css`
    :host {
      display: block;
    }

    .item {
      display: flex;
      gap: var(--space-4);
      padding: var(--space-4);
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-lg);
      transition: border-color var(--transition-fast);
    }

    .item:hover {
      border-color: var(--color-border-hover);
    }

    .image {
      width: 100px;
      height: 100px;
      background: var(--gradient-card);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      overflow: hidden;
    }

    .image img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }

    .placeholder {
      font-size: 2.5rem;
      opacity: 0.3;
    }

    .details {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .name {
      font-weight: var(--font-weight-semibold);
      margin-bottom: var(--space-1);
    }

    .sku {
      font-size: var(--font-size-xs);
      color: var(--color-text-muted);
    }

    .quantity {
      display: flex;
      align-items: center;
      gap: var(--space-2);
      margin-top: var(--space-3);
    }

    .qty-label {
      font-size: var(--font-size-sm);
      color: var(--color-text-secondary);
    }

    .qty-value {
      font-weight: var(--font-weight-semibold);
      color: var(--color-secondary);
    }

    .actions {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      justify-content: space-between;
    }

    .price {
      font-size: var(--font-size-lg);
      font-weight: var(--font-weight-bold);
      color: var(--color-secondary);
    }

    .remove-btn {
      padding: var(--space-2);
      background: transparent;
      border: 1px solid transparent;
      border-radius: var(--radius-sm);
      color: var(--color-text-muted);
      font-size: var(--font-size-sm);
      cursor: pointer;
      transition: all var(--transition-fast);
    }

    .remove-btn:hover {
      background: rgba(244, 67, 54, 0.1);
      border-color: rgba(244, 67, 54, 0.3);
      color: var(--color-danger);
    }

    @media (max-width: 640px) {
      .item { flex-wrap: wrap; }
      .image { width: 80px; height: 80px; }
      .actions {
        flex-direction: row;
        width: 100%;
        margin-top: var(--space-3);
        padding-top: var(--space-3);
        border-top: 1px solid var(--glass-border);
      }
    }
  `;

    constructor() {
        super();
        this.item = {};
    }

    _remove() {
        this.dispatchEvent(new CustomEvent('remove', { bubbles: true, composed: true }));
    }

    render() {
        const { product_name, product_default_code, product_uom_qty, price_subtotal, product_image_url } = this.item;

        return html`
      <div class="item">
        <div class="image">
          ${product_image_url ? html`
            <img src="${product_image_url}" alt="${product_name}">
          ` : html`
            <span class="placeholder">📦</span>
          `}
        </div>

        <div class="details">
          <span class="name">${product_name || 'Producto'}</span>
          ${product_default_code ? html`<span class="sku">SKU: ${product_default_code}</span>` : ''}
          <div class="quantity">
            <span class="qty-label">Cantidad:</span>
            <span class="qty-value">${product_uom_qty || 1}</span>
          </div>
        </div>

        <div class="actions">
          <span class="price">${formatCurrency(price_subtotal)}</span>
          <button class="remove-btn" @click=${this._remove}>
            🗑️ Eliminar
          </button>
        </div>
      </div>
    `;
    }
}

customElements.define('cart-item', CartItem);
