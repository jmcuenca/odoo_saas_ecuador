/**
 * SomaTech Shell - Main App Container
 * @element soma-app
 */
import { LitElement, html, css } from 'lit';
import { CartController } from '../../core/controllers/cart.controller.js';
import { AuthController } from '../../core/controllers/auth.controller.js';

export class SomaApp extends LitElement {
    static properties = {
        view: { type: String },
        showLogin: { type: Boolean, state: true },
    };

    // Reactive Controllers
    cart = new CartController(this);
    auth = new AuthController(this);

    static styles = css`
    :host {
      display: block;
      min-height: 100vh;
    }

    .app {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    main {
      flex: 1;
      padding: var(--space-6) var(--space-4);
      max-width: var(--container-max);
      margin: 0 auto;
      width: 100%;
    }

    .page-enter {
      animation: fadeIn 0.3s ease forwards;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  `;

    constructor() {
        super();
        this.view = 'catalog';
        this.showLogin = false;

        // Global event listeners
        window.addEventListener('navigate', (e) => this._navigate(e.detail.view));
        window.addEventListener('show-login', () => this.showLogin = true);
    }

    _navigate(view) {
        this.view = view;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    _renderPage() {
        switch (this.view) {
            case 'cart':
                return html`<cart-page class="page-enter"></cart-page>`;
            case 'catalog':
            default:
                return html`<catalog-page class="page-enter"></catalog-page>`;
        }
    }

    render() {
        return html`
      <div class="app">
        <soma-header
          .cartCount=${this.cart.itemCount}
          .isLoggedIn=${this.auth.isLoggedIn}
          .userName=${this.auth.user?.name}
        ></soma-header>

        <main>
          ${this._renderPage()}
        </main>

        <soma-footer></soma-footer>

        <login-modal
          ?open=${this.showLogin}
          @close=${() => this.showLogin = false}
        ></login-modal>
      </div>
    `;
    }
}

customElements.define('soma-app', SomaApp);
