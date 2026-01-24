/**
 * SomaTech Cart - Page
 * @element cart-page
 */
import { LitElement, html, css } from 'lit';
import { CartController } from '../../core/controllers/cart.controller.js';

export class CartPage extends LitElement {
    cart = new CartController(this);

    static styles = css`
    :host {
      display: block;
    }

    .page-title {
      font-size: var(--font-size-3xl);
      font-weight: var(--font-weight-bold);
      margin-bottom: var(--space-8);
      display: flex;
      align-items: center;
      gap: var(--space-3);
    }

    .cart-layout {
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: var(--space-8);
    }

    @media (max-width: 1024px) {
      .cart-layout {
        grid-template-columns: 1fr;
      }
    }

    .cart-items {
      display: flex;
      flex-direction: column;
      gap: var(--space-4);
    }

    .empty-cart {
      text-align: center;
      padding: var(--space-16);
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-xl);
    }

    .empty-cart .icon {
      font-size: 5rem;
      margin-bottom: var(--space-4);
      opacity: 0.4;
    }

    .empty-cart h3 {
      font-size: var(--font-size-xl);
      margin-bottom: var(--space-2);
    }

    .empty-cart p {
      color: var(--color-text-secondary);
      margin-bottom: var(--space-6);
    }

    .browse-btn {
      display: inline-flex;
      align-items: center;
      gap: var(--space-2);
      padding: var(--space-3) var(--space-6);
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

    .browse-btn:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-glow-primary);
    }

    .loading {
      display: flex;
      justify-content: center;
      padding: var(--space-16);
    }
  `;

    _navigate(view) {
        window.dispatchEvent(new CustomEvent('navigate', { detail: { view } }));
    }

    render() {
        if (this.cart.loading) {
            return html`
        <h1 class="page-title">🛒 Mi Carrito</h1>
        <div class="loading">
          <soma-spinner size="lg"></soma-spinner>
        </div>
      `;
        }

        if (this.cart.items.length === 0) {
            return html`
        <h1 class="page-title">🛒 Mi Carrito</h1>
        <div class="empty-cart">
          <div class="icon">🛒</div>
          <h3>Tu carrito está vacío</h3>
          <p>Agrega productos para comenzar tu compra.</p>
          <button class="browse-btn" @click=${() => this._navigate('catalog')}>
            📦 Ver Productos
          </button>
        </div>
      `;
        }

        return html`
      <h1 class="page-title">🛒 Mi Carrito (${this.cart.itemCount})</h1>
      <div class="cart-layout">
        <div class="cart-items">
          ${this.cart.items.map(item => html`
            <cart-item
              .item=${item}
              @remove=${() => this.cart.removeItem(item.id)}
            ></cart-item>
          `)}
        </div>
        <cart-summary
          .total=${this.cart.total}
          .itemCount=${this.cart.itemCount}
          @checkout=${() => this.cart.checkout()}
        ></cart-summary>
      </div>
    `;
    }
}

customElements.define('cart-page', CartPage);
