/**
 * SomaTech Shell - Header Navigation
 * @element soma-header
 */
import { LitElement, html, css } from 'lit';

export class SomaHeader extends LitElement {
    static properties = {
        cartCount: { type: Number },
        isLoggedIn: { type: Boolean },
        userName: { type: String },
    };

    static styles = css`
    :host {
      display: block;
      position: sticky;
      top: 0;
      z-index: var(--z-sticky);
    }

    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: var(--space-4) var(--space-6);
      height: var(--header-height);
      background: rgba(15, 15, 35, 0.9);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--glass-border);
    }

    .logo {
      display: flex;
      align-items: center;
      gap: var(--space-3);
      cursor: pointer;
      transition: opacity var(--transition-fast);
    }

    .logo:hover {
      opacity: 0.8;
    }

    .logo-icon {
      width: 42px;
      height: 42px;
      background: var(--gradient-primary);
      border-radius: var(--radius-lg);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
    }

    .logo-text {
      font-size: var(--font-size-xl);
      font-weight: var(--font-weight-bold);
    }

    .logo-text span {
      color: var(--color-secondary);
    }

    nav {
      display: flex;
      align-items: center;
      gap: var(--space-3);
    }

    .nav-btn {
      display: flex;
      align-items: center;
      gap: var(--space-2);
      padding: var(--space-3) var(--space-5);
      background: transparent;
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      color: var(--color-text-primary);
      font-size: var(--font-size-sm);
      font-weight: var(--font-weight-medium);
      cursor: pointer;
      transition: all var(--transition-base);
    }

    .nav-btn:hover {
      background: var(--glass-bg);
      border-color: var(--color-border-hover);
    }

    .nav-btn.cart {
      position: relative;
    }

    .cart-badge {
      position: absolute;
      top: -8px;
      right: -8px;
      min-width: 20px;
      height: 20px;
      padding: 0 6px;
      background: var(--gradient-secondary);
      border-radius: var(--radius-full);
      font-size: var(--font-size-xs);
      font-weight: var(--font-weight-bold);
      color: var(--color-bg-primary);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .nav-btn.primary {
      background: var(--gradient-primary);
      border: none;
    }

    .nav-btn.primary:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-glow-primary);
    }

    .user-greeting {
      color: var(--color-text-secondary);
      font-size: var(--font-size-sm);
    }

    @media (max-width: 640px) {
      header { padding: var(--space-3) var(--space-4); }
      .logo-text { display: none; }
      .nav-btn span:not(.cart-badge) { display: none; }
      .nav-btn { padding: var(--space-3); }
    }
  `;

    constructor() {
        super();
        this.cartCount = 0;
        this.isLoggedIn = false;
        this.userName = '';
    }

    _navigate(view) {
        window.dispatchEvent(new CustomEvent('navigate', { detail: { view } }));
    }

    _showLogin() {
        window.dispatchEvent(new CustomEvent('show-login'));
    }

    render() {
        return html`
      <header>
        <div class="logo" @click=${() => this._navigate('catalog')}>
          <div class="logo-icon">🛒</div>
          <div class="logo-text">Soma<span>Tech</span></div>
        </div>

        <nav>
          <button class="nav-btn" @click=${() => this._navigate('catalog')}>
            📦 <span>Productos</span>
          </button>

          <button class="nav-btn cart" @click=${() => this._navigate('cart')}>
            🛒 <span>Carrito</span>
            ${this.cartCount > 0 ? html`
              <span class="cart-badge">${this.cartCount}</span>
            ` : ''}
          </button>

          ${this.isLoggedIn ? html`
            <span class="user-greeting">Hola, ${this.userName || 'Usuario'}</span>
          ` : html`
            <button class="nav-btn primary" @click=${this._showLogin}>
              🔐 <span>Ingresar</span>
            </button>
          `}
        </nav>
      </header>
    `;
    }
}

customElements.define('soma-header', SomaHeader);
