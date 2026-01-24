/**
 * SomaTech Services - Auth API
 */
import { api } from './api.js';

const STORAGE_KEY = 'soma_partner_id';
const USER_KEY = 'soma_user';

class AuthService {
    constructor() {
        this._partnerId = localStorage.getItem(STORAGE_KEY);
        this._user = this._loadUser();
    }

    _loadUser() {
        try {
            const stored = localStorage.getItem(USER_KEY);
            return stored ? JSON.parse(stored) : null;
        } catch {
            return null;
        }
    }

    _saveUser(user) {
        this._user = user;
        localStorage.setItem(USER_KEY, JSON.stringify(user));
    }

    /**
     * Login user
     * @param {string} email - User email
     * @param {string} password - User password
     * @returns {Promise<Object>} User data with partner_id
     */
    async login(email, password) {
        const result = await api.post('/auth/login', { email, password });

        if (result.partner_id) {
            this._partnerId = result.partner_id;
            localStorage.setItem(STORAGE_KEY, result.partner_id);
            this._saveUser({
                partnerId: result.partner_id,
                name: result.name || email,
                email,
            });
        }

        // Dispatch global event
        window.dispatchEvent(new CustomEvent('auth-changed', {
            detail: { isLoggedIn: true, user: this._user }
        }));

        return result;
    }

    /**
     * Register new user
     * @param {Object} data - Registration data
     * @returns {Promise<Object>} User data with partner_id
     */
    async signup(data) {
        const result = await api.post('/auth/signup', data);

        if (result.partner_id) {
            this._partnerId = result.partner_id;
            localStorage.setItem(STORAGE_KEY, result.partner_id);
            this._saveUser({
                partnerId: result.partner_id,
                name: data.name,
                email: data.email,
            });
        }

        window.dispatchEvent(new CustomEvent('auth-changed', {
            detail: { isLoggedIn: true, user: this._user }
        }));

        return result;
    }

    /**
     * Logout current user
     */
    logout() {
        this._partnerId = null;
        this._user = null;
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem(USER_KEY);

        window.dispatchEvent(new CustomEvent('auth-changed', {
            detail: { isLoggedIn: false, user: null }
        }));
    }

    /**
     * Check if user is logged in
     * @returns {boolean}
     */
    isLoggedIn() {
        return !!this._partnerId;
    }

    /**
     * Get current partner ID
     * @returns {string|null}
     */
    getPartnerId() {
        return this._partnerId;
    }

    /**
     * Get current user
     * @returns {Object|null}
     */
    getUser() {
        return this._user;
    }
}

export const authService = new AuthService();
