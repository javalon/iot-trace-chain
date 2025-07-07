import { Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';

export interface JwtPayload {
  email: string;
  name: string;
  role: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly tokenKey = 'token';

  /** Guarda el token en localStorage */
  setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  /** Obtiene el token JWT actual, si hay */
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  /** Elimina el token (logout) */
  clearToken(): void {
    localStorage.removeItem(this.tokenKey);
  }

  /** Retorna true si el usuario está autenticado */
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const { exp } = jwtDecode<{ exp: number }>(token);
      return exp * 1000 > Date.now(); // verifica que no esté vencido
    } catch {
      return false;
    }
  }

  isAdmin(): boolean {
    const userInfo = this.getUserInfo();
    return userInfo?.role === 'admin';
  }

  /** Decodifica el token JWT y retorna la información del usuario */
  getUserInfo(): JwtPayload | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      return jwtDecode<JwtPayload>(token);
    } catch {
      return null;
    }
  }
}