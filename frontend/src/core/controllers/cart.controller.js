/**
 * SomaTech Controllers - Cart Reactive Controller
 *
 * Lit ReactiveController for cart state management
 * Usage: this.cart = new CartController(this);
 */
import { cartService } from '../services/cart.service.js';
import { authService } from '../services/auth.service.js';
import { SomaToast } from '../components/soma-toast.js';

export class CartController {
    /** @type {import('lit').ReactiveControllerHost} */
    host;

    /** Cart state */
    items = [];
    total = 0;
    orderId = null;
    loading = false;
    itemCount = 0;

    constructor(host) {
        this.host = host;
        host.addController(this);
        this._handleCartUpdate = this._handleCartUpdate.bind(this);
        this._handleAuthChange = this._handleAuthChange.bind(this);
    }

    hostConnected() {
        window.addEventListener('cart-updated', this._handleCartUpdate);
        window.addEventListener('auth-changed', this._handleAuthChange);
        this.load();
    }

    hostDisconnected() {
        window.removeEventListener('cart-updated', this._handleCartUpdate);
        window.removeEventListener('auth-changed', this._handleAuthChange);
    }

    _handleCartUpdate() {
        this.load();
    }

    _handleAuthChange(e) {
        if (e.detail.isLoggedIn) {
            this.load();
        } else {
            this._reset();
        }
    }

    _reset() {
        this.items = [];
        this.total = 0;
        this.orderId = null;
        this.itemCount = 0;
        this.host.requestUpdate();
    }

    /**
     * Load cart from API
     */
    async load() {
        if (!authService.isLoggedIn()) {
            this._reset();
            return;
        }

        this.loading = true;
        this.host.requestUpdate();

        try {
            const cart = await cartService.getCart();
            this.items = cart.lines || [];
            this.total = cart.amount_total || 0;
            this.orderId = cart.order_id || null;
            this.itemCount = this.items.reduce((sum, item) => sum + (item.quantity || 1), 0);
        } catch (err) {
            console.error('Failed to load cart:', err);
            SomaToast.error('Error al cargar el carrito');
        } finally {
            this.loading = false;
            this.host.requestUpdate();
        }
    }

    /**
     * Add product to cart
     */
    async addItem(productId, quantity = 1) {
        if (!authService.isLoggedIn()) {
            SomaToast.warning('Debes iniciar sesión primero');
            window.dispatchEvent(new CustomEvent('show-login'));
            return false;
        }

        try {
            await cartService.addItem(productId, quantity);
            await this.load();
            SomaToast.success('Producto agregado al carrito');
            window.dispatchEvent(new CustomEvent('cart-updated'));
            return true;
        } catch (err) {
            SomaToast.error(err.message || 'Error al agregar producto');
            return false;
        }
    }

    /**
     * Update item quantity
     */
    async updateQuantity(lineId, quantity) {
        try {
            await cartService.updateQuantity(lineId, quantity);
            await this.load();
            window.dispatchEvent(new CustomEvent('cart-updated'));
        } catch (err) {
            SomaToast.error(err.message || 'Error al actualizar cantidad');
        }
    }

    /**
     * Remove item from cart
     */
    async removeItem(lineId) {
        try {
            await cartService.removeItem(lineId);
            await this.load();
            SomaToast.success('Producto eliminado');
            window.dispatchEvent(new CustomEvent('cart-updated'));
        } catch (err) {
            SomaToast.error(err.message || 'Error al eliminar producto');
        }
    }

    /**
     * Checkout
     */
    async checkout() {
        try {
            const result = await cartService.checkout();
            this._reset();
            window.dispatchEvent(new CustomEvent('cart-updated'));
            SomaToast.success(`¡Pedido confirmado! #${result.order_name || result.order_id}`);
            return result;
        } catch (err) {
            SomaToast.error(err.message || 'Error al confirmar pedido');
            throw err;
        }
    }
}
