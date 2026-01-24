/**
 * SomaTech Store - Main Entry Point
 *
 * Bootstrap application and import all modules
 */

// Design System
import './core/design/tokens.css';
import './core/design/reset.css';
import './core/design/utilities.css';
import './core/design/animations.css';

// Shared Components
import './core/components/soma-button.js';
import './core/components/soma-card.js';
import './core/components/soma-input.js';
import './core/components/soma-modal.js';
import './core/components/soma-spinner.js';
import './core/components/soma-toast.js';
import './core/components/soma-skeleton.js';

// Feature Modules
import './features/shell/soma-app.js';
import './features/shell/soma-header.js';
import './features/shell/soma-footer.js';
import './features/catalog/catalog-page.js';
import './features/catalog/product-grid.js';
import './features/catalog/product-card.js';
import './features/cart/cart-page.js';
import './features/cart/cart-item.js';
import './features/cart/cart-summary.js';
import './features/auth/login-modal.js';

console.log('🚀 SomaTech Store v1.0 initialized');
console.log('📦 Lit Web Components + Vite');
console.log('🔗 Connected to Django Ninja → Odoo ERP');
