/**
 * SomaTech Services - Products API
 */
import { api } from './api.js';

class ProductsService {
    /**
     * Fetch all products
     * @returns {Promise<Array>} Product list from Odoo
     */
    async getAll() {
        const response = await api.get('/products/');
        return response.products || response || [];
    }

    /**
     * Fetch single product by ID
     * @param {number} id - Product ID
     * @returns {Promise<Object>} Product details
     */
    async getById(id) {
        return api.get(`/products/${id}`);
    }

    /**
     * Search products
     * @param {string} query - Search term
     * @returns {Promise<Array>} Matching products
     */
    async search(query) {
        return api.get('/products/', { search: query });
    }
}

export const productsService = new ProductsService();
