/**
 * SomaTech Services - Cart API
 */
import { api } from './api.js';
import { authService } from './auth.service.js';

class CartService {
    /**
     * Get current cart
     * @returns {Promise<Object>} Cart with lines and total
     */
    async getCart() {
        const partnerId = authService.getPartnerId();
        if (!partnerId) {
            return { lines: [], amount_total: 0, order_id: null };
        }
        return api.get('/cart/', { partner_id: partnerId });
    }

    /**
     * Add item to cart
     * @param {number} productId - Odoo product ID
     * @param {number} quantity - Quantity to add
     * @returns {Promise<Object>} Updated cart
     */
    async addItem(productId, quantity = 1) {
        const partnerId = authService.getPartnerId();
        if (!partnerId) {
            throw new Error('Debes iniciar sesión para agregar al carrito');
        }
        return api.post(`/cart/add?partner_id=${partnerId}`, {
            product_id: productId,
            quantity,
        });
    }

    /**
     * Update item quantity
     * @param {number} lineId - Order line ID
     * @param {number} quantity - New quantity
     * @returns {Promise<Object>} Updated cart
     */
    async updateQuantity(lineId, quantity) {
        const partnerId = authService.getPartnerId();
        return api.put(`/cart/line/${lineId}?partner_id=${partnerId}`, {
            quantity,
        });
    }

    /**
     * Remove item from cart
     * @param {number} lineId - Order line ID
     * @returns {Promise<Object>} Updated cart
     */
    async removeItem(lineId) {
        const partnerId = authService.getPartnerId();
        return api.delete(`/cart/line/${lineId}?partner_id=${partnerId}`);
    }

    /**
     * Checkout - confirm order
     * @returns {Promise<Object>} Order confirmation
     */
    async checkout() {
        const partnerId = authService.getPartnerId();
        if (!partnerId) {
            throw new Error('Debes iniciar sesión para realizar el pedido');
        }
        return api.post('/cart/checkout', { partner_id: partnerId });
    }

    /**
     * Clear cart
     * @returns {Promise<void>}
     */
    async clear() {
        const partnerId = authService.getPartnerId();
        return api.delete(`/cart/?partner_id=${partnerId}`);
    }
}

export const cartService = new CartService();
