/**
 * SomaTech Shell - Footer
 * @element soma-footer
 */
import { LitElement, html, css } from 'lit';

export class SomaFooter extends LitElement {
    static styles = css`
    :host {
      display: block;
    }

    footer {
      padding: var(--space-8) var(--space-6);
      border-top: 1px solid var(--glass-border);
      background: rgba(0, 0, 0, 0.2);
    }

    .footer-content {
      max-width: var(--container-max);
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: var(--space-8);
    }

    .footer-section h4 {
      font-size: var(--font-size-sm);
      font-weight: var(--font-weight-semibold);
      color: var(--color-secondary);
      margin-bottom: var(--space-4);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .footer-section p,
    .footer-section a {
      font-size: var(--font-size-sm);
      color: var(--color-text-secondary);
      line-height: 1.8;
    }

    .footer-section a {
      display: block;
      transition: color var(--transition-fast);
    }

    .footer-section a:hover {
      color: var(--color-secondary);
    }

    .footer-bottom {
      max-width: var(--container-max);
      margin: var(--space-8) auto 0;
      padding-top: var(--space-6);
      border-top: 1px solid var(--glass-border);
      text-align: center;
      color: var(--color-text-muted);
      font-size: var(--font-size-sm);
    }

    .footer-bottom a {
      color: var(--color-secondary);
    }

    .sri-badge {
      display: inline-flex;
      align-items: center;
      gap: var(--space-2);
      margin-top: var(--space-2);
      padding: var(--space-2) var(--space-3);
      background: rgba(76, 175, 80, 0.1);
      border: 1px solid rgba(76, 175, 80, 0.3);
      border-radius: var(--radius-md);
      font-size: var(--font-size-xs);
      color: var(--color-success);
    }
  `;

    render() {
        return html`
      <footer>
        <div class="footer-content">
          <div class="footer-section">
            <h4>SomaTech Ecuador</h4>
            <p>Tecnología premium con facturación electrónica autorizada por el SRI.</p>
            <div class="sri-badge">
              ✓ Facturación Electrónica SRI
            </div>
          </div>

          <div class="footer-section">
            <h4>Tienda</h4>
            <a href="#" @click=${(e) => { e.preventDefault(); this._navigate('catalog'); }}>Catálogo</a>
            <a href="#">Ofertas</a>
            <a href="#">Nuevos Productos</a>
          </div>

          <div class="footer-section">
            <h4>Soporte</h4>
            <a href="#">Centro de Ayuda</a>
            <a href="#">Envíos y Devoluciones</a>
            <a href="#">Garantías</a>
          </div>

          <div class="footer-section">
            <h4>Contacto</h4>
            <p>📍 Quito, Ecuador</p>
            <p>📧 ventas@somatech.ec</p>
            <p>📞 +593 2 XXX-XXXX</p>
          </div>
        </div>

        <div class="footer-bottom">
          <p>© 2025 SomaTech Ecuador. Todos los derechos reservados.</p>
          <p>Powered by <a href="#">Odoo ERP</a> + <a href="#">Django Ninja</a> + <a href="#">Lit</a></p>
          <p>RUC: 1792XXXXXX001</p>
        </div>
      </footer>
    `;
    }

    _navigate(view) {
        window.dispatchEvent(new CustomEvent('navigate', { detail: { view } }));
    }
}

customElements.define('soma-footer', SomaFooter);
