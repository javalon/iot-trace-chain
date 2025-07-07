import { CanActivate, Router } from '@angular/router';
import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): boolean {
    if (this.auth.isAuthenticated()) {
      return true;
    }
    this.auth.clearToken(); // Limpia el token si está vencido o corrupto
    this.router.navigate(['/login']); // O la ruta de inicio que prefieras
    return false;
  }
}