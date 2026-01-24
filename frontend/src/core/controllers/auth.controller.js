/**
 * SomaTech Controllers - Auth Reactive Controller
 *
 * Lit ReactiveController for authentication state
 * Usage: this.auth = new AuthController(this);
 */
import { authService } from '../services/auth.service.js';
import { SomaToast } from '../components/soma-toast.js';

export class AuthController {
    /** @type {import('lit').ReactiveControllerHost} */
    host;

    /** Auth state */
    isLoggedIn = false;
    user = null;
    loading = false;

    constructor(host) {
        this.host = host;
        host.addController(this);
        this._handleAuthChange = this._handleAuthChange.bind(this);
    }

    hostConnected() {
        window.addEventListener('auth-changed', this._handleAuthChange);
        this._syncState();
    }

    hostDisconnected() {
        window.removeEventListener('auth-changed', this._handleAuthChange);
    }

    _handleAuthChange(e) {
        this.isLoggedIn = e.detail.isLoggedIn;
        this.user = e.detail.user;
        this.host.requestUpdate();
    }

    _syncState() {
        this.isLoggedIn = authService.isLoggedIn();
        this.user = authService.getUser();
        this.host.requestUpdate();
    }

    /**
     * Login
     */
    async login(email, password) {
        this.loading = true;
        this.host.requestUpdate();

        try {
            await authService.login(email, password);
            SomaToast.success('¡Bienvenido!');
            return true;
        } catch (err) {
            SomaToast.error(err.message || 'Error al iniciar sesión');
            return false;
        } finally {
            this.loading = false;
            this.host.requestUpdate();
        }
    }

    /**
     * Signup
     */
    async signup(data) {
        this.loading = true;
        this.host.requestUpdate();

        try {
            await authService.signup(data);
            SomaToast.success('¡Cuenta creada exitosamente!');
            return true;
        } catch (err) {
            SomaToast.error(err.message || 'Error al crear cuenta');
            return false;
        } finally {
            this.loading = false;
            this.host.requestUpdate();
        }
    }

    /**
     * Logout
     */
    logout() {
        authService.logout();
        SomaToast.info('Sesión cerrada');
    }
}
