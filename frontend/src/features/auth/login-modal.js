/**
 * SomaTech Auth - Login Modal
 * @element login-modal
 */
import { LitElement, html, css } from 'lit';
import { AuthController } from '../../core/controllers/auth.controller.js';

export class LoginModal extends LitElement {
    static properties = {
        open: { type: Boolean, reflect: true },
        mode: { type: String, state: true }, // 'login' | 'signup'
    };

    auth = new AuthController(this);

    static styles = css`
    :host {
      display: contents;
    }

    .backdrop {
      position: fixed;
      inset: 0;
      z-index: var(--z-modal-backdrop);
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--space-4);
      opacity: 0;
      visibility: hidden;
      transition: all var(--transition-base);
    }

    :host([open]) .backdrop {
      opacity: 1;
      visibility: visible;
    }

    .modal {
      width: 100%;
      max-width: 420px;
      background: var(--color-bg-secondary);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-xl);
      overflow: hidden;
      transform: scale(0.95) translateY(20px);
      transition: transform var(--transition-base);
    }

    :host([open]) .modal {
      transform: scale(1) translateY(0);
    }

    .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: var(--space-5) var(--space-6);
      border-bottom: 1px solid var(--glass-border);
    }

    .title {
      font-size: var(--font-size-xl);
      font-weight: var(--font-weight-semibold);
    }

    .close-btn {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      border: none;
      border-radius: var(--radius-md);
      color: var(--color-text-muted);
      font-size: 1.25rem;
      cursor: pointer;
      transition: all var(--transition-fast);
    }

    .close-btn:hover {
      background: var(--glass-bg);
      color: var(--color-text-primary);
    }

    .body {
      padding: var(--space-6);
    }

    .form {
      display: flex;
      flex-direction: column;
      gap: var(--space-4);
    }

    .submit-btn {
      margin-top: var(--space-2);
      padding: var(--space-4);
      background: var(--gradient-primary);
      border: none;
      border-radius: var(--radius-md);
      color: white;
      font-family: inherit;
      font-size: var(--font-size-base);
      font-weight: var(--font-weight-semibold);
      cursor: pointer;
      transition: all var(--transition-base);
    }

    .submit-btn:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: var(--shadow-glow-primary);
    }

    .submit-btn:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .switch-mode {
      text-align: center;
      margin-top: var(--space-4);
      font-size: var(--font-size-sm);
      color: var(--color-text-secondary);
    }

    .switch-mode button {
      background: none;
      border: none;
      color: var(--color-secondary);
      font-family: inherit;
      font-size: inherit;
      cursor: pointer;
      text-decoration: underline;
    }

    .switch-mode button:hover {
      color: var(--color-secondary-400);
    }
  `;

    constructor() {
        super();
        this.open = false;
        this.mode = 'login';
    }

    _close() {
        this.dispatchEvent(new CustomEvent('close', { bubbles: true, composed: true }));
    }

    _handleBackdrop(e) {
        if (e.target === e.currentTarget) {
            this._close();
        }
    }

    async _handleSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);

        if (this.mode === 'login') {
            const success = await this.auth.login(
                formData.get('email'),
                formData.get('password')
            );
            if (success) this._close();
        } else {
            const success = await this.auth.signup({
                name: formData.get('name'),
                email: formData.get('email'),
                password: formData.get('password'),
                vat: formData.get('vat') || null,
            });
            if (success) this._close();
        }
    }

    _switchMode() {
        this.mode = this.mode === 'login' ? 'signup' : 'login';
    }

    render() {
        return html`
      <div class="backdrop" @click=${this._handleBackdrop}>
        <div class="modal">
          <header class="header">
            <h2 class="title">${this.mode === 'login' ? 'Iniciar Sesión' : 'Crear Cuenta'}</h2>
            <button class="close-btn" @click=${this._close}>✕</button>
          </header>

          <div class="body">
            <form class="form" @submit=${this._handleSubmit}>
              ${this.mode === 'signup' ? html`
                <soma-input
                  name="name"
                  label="Nombre Completo"
                  placeholder="Juan Pérez"
                  required
                ></soma-input>
              ` : ''}

              <soma-input
                name="email"
                type="email"
                label="Correo Electrónico"
                placeholder="tu@email.com"
                required
              ></soma-input>

              <soma-input
                name="password"
                type="password"
                label="Contraseña"
                placeholder="••••••••"
                required
              ></soma-input>

              ${this.mode === 'signup' ? html`
                <soma-input
                  name="vat"
                  label="RUC / Cédula (opcional)"
                  placeholder="1712345678001"
                ></soma-input>
              ` : ''}

              <button
                type="submit"
                class="submit-btn"
                ?disabled=${this.auth.loading}
              >
                ${this.auth.loading ? '⏳ Procesando...' :
                (this.mode === 'login' ? '🔐 Ingresar' : '✓ Crear Cuenta')}
              </button>
            </form>

            <div class="switch-mode">
              ${this.mode === 'login' ? html`
                ¿No tienes cuenta? <button @click=${this._switchMode}>Regístrate</button>
              ` : html`
                ¿Ya tienes cuenta? <button @click=${this._switchMode}>Inicia Sesión</button>
              `}
            </div>
          </div>
        </div>
      </div>
    `;
    }
}

customElements.define('login-modal', LoginModal);
