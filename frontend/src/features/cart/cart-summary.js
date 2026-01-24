/**
 * SomaTech Cart - Summary
 * @element cart-summary
 */
import { LitElement, html, css } from 'lit';
import { formatCurrency } from '../../utils/format.js';

export class CartSummary extends LitElement {
    static properties = {
        total: { type: Number },
        itemCount: { type: Number },
        processing: { type: Boolean, state: true },
    };

    static styles = css`
    :host {
      display: block;
    }

    .summary {
      position: sticky;
      top: calc(var(--header-height) + var(--space-6));
      padding: var(--space-6);
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-xl);
    }

    .title {
      font-size: var(--font-size-lg);
      font-weight: var(--font-weight-semibold);
      margin-bottom: var(--space-6);
      padding-bottom: var(--space-4);
      border-bottom: 1px solid var(--glass-border);
    }

    .row {
      display: flex;
      justify-content: space-between;
      margin-bottom: var(--space-3);
      font-size: var(--font-size-sm);
      color: var(--color-text-secondary);
    }

    .row.total {
      font-size: var(--font-size-xl);
      font-weight: var(--font-weight-bold);
      color: var(--color-text-primary);
      margin-top: var(--space-4);
      padding-top: var(--space-4);
      border-top: 1px solid var(--glass-border);
    }

    .row.total .value {
      color: var(--color-secondary);
    }

    .tax-note {
      font-size: var(--font-size-xs);
      color: var(--color-text-muted);
      text-align: right;
      margin-top: var(--space-1);
    }

    .checkout-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      width: 100%;
      margin-top: var(--space-6);
      padding: var(--space-4);
      background: var(--gradient-secondary);
      border: none;
      border-radius: var(--radius-md);
      color: var(--color-bg-primary);
      font-family: inherit;
      font-size: var(--font-size-base);
      font-weight: var(--font-weight-semibold);
      cursor: pointer;
      transition: all var(--transition-base);
    }

    .checkout-btn:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: var(--shadow-glow-secondary);
    }

    .checkout-btn:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .secure-note {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      margin-top: var(--space-4);
      font-size: var(--font-size-xs);
      color: var(--color-text-muted);
    }

    .sri-badge {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      margin-top: var(--space-4);
      padding: var(--space-3);
      background: rgba(76, 175, 80, 0.1);
      border: 1px solid rgba(76, 175, 80, 0.3);
      border-radius: var(--radius-md);
      font-size: var(--font-size-xs);
      color: var(--color-success);
    }
  `;

    constructor() {
        super();
        this.total = 0;
        this.itemCount = 0;
        this.processing = false;
    }

    async _checkout() {
        this.processing = true;
        this.dispatchEvent(new CustomEvent('checkout', { bubbles: true, composed: true }));
        // The parent will handle the actual checkout
        setTimeout(() => this.processing = false, 3000); // Fallback reset
    }

    render() {
        const subtotal = this.total / 1.15; // IVA 15%
        const iva = this.total - subtotal;

        return html`
      <div class="summary">
        <h3 class="title">Resumen del Pedido</h3>

        <div class="row">
          <span>Productos (${this.itemCount})</span>
          <span>${formatCurrency(subtotal)}</span>
        </div>

        <div class="row">
          <span>IVA (15%)</span>
          <span>${formatCurrency(iva)}</span>
        </div>

        <div class="row">
          <span>Envío</span>
          <span style="color: var(--color-success)">Gratis</span>
        </div>

        <div class="row total">
          <span>Total</span>
          <span class="value">${formatCurrency(this.total)}</span>
        </div>
        <p class="tax-note">IVA incluido</p>

        <button
          class="checkout-btn"
          ?disabled=${this.processing || this.itemCount === 0}
          @click=${this._checkout}
        >
          ${this.processing ? '⏳ Procesando...' : '✓ Confirmar Pedido'}
        </button>

        <p class="secure-note">🔒 Pago seguro con facturación electrónica</p>

        <div class="sri-badge">
          ✓ Factura SRI autorizada automáticamente
        </div>
      </div>
    `;
    }
}

customElements.define('cart-summary', CartSummary);
